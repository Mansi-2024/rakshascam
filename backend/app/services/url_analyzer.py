"""Safe URL Analyzer Service.

Applies SSRF protections, enforces connection/size limits, performs safe
HTTP retrieval, and dispatches comprehensive Phase 2 & Phase 3 structured extraction.
"""

from datetime import datetime, timezone
import time
from typing import Optional
from urllib.parse import urljoin

import httpx

from app.core.config import settings
from app.core.security import (
    SSRFSecurityError,
    URLValidationError,
    is_fictional_demo_host,
    validate_and_normalize_url,
)
from app.evidence.engine import EvidenceEngine
from app.evidence.models import EvidenceRecord
from app.risk.engine import RiskAssessmentEngine
from app.schemas.analysis import (
    AnalysisMetadataModel,
    AssessmentModel,
    ContactSignalsModel,
    DetectedReferencesModel,
    EvidenceSummaryModel,
    FetchResultModel,
    PageModel,
    RiskSignalModel,
    URLAnalysisResponse,
    URLInputModel,
    VerificationResultModel,
)
from app.services.html_extractor import extract_comprehensive_analysis
from app.verification.engine import VerificationEngine
from app.trust_chain.builder import TrustChainBuilder
from app.journey.builder import ScamJourneyBuilder
from app.response.engine import SafeResponseEngine


class FetchError(Exception):
    """Base exception for HTTP fetch failures."""
    pass


class ResponseTooLargeError(FetchError):
    """Raised when remote response exceeds maximum allowed size."""
    pass


class RedirectLimitExceededError(FetchError):
    """Raised when redirects exceed maximum permitted hops."""
    pass


class UnsupportedContentTypeError(FetchError):
    """Raised when remote content is not acceptable HTML."""
    pass


FICTIONAL_DEMO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Example Wealth Advisors | High Yield Investment Opportunities</title>
  <meta name="description" content="Exclusive private wealth advisory offering guaranteed returns and pre-IPO allocations under SEBI authorization.">
  <link rel="canonical" href="https://example-finance.test">
</head>
<body>
  <header>
    <h1>Example Wealth Advisors Private Limited</h1>
    <p class="leadership">Chief Strategist: Dr. R. Sharma</p>
    <nav>
      <a href="/about">About Us</a>
      <a href="/plans">Investment Plans</a>
      <a href="https://external-brokerage.example/portal">Partner Portal</a>
    </nav>
  </header>
  <main>
    <h2>Guaranteed 35% Monthly Returns with Principal Protection</h2>
    <p>
      Join our premier institutional wealth circle. We provide guaranteed profit and risk-free investment opportunities for serious high-net-worth investors. Act now—this is a limited time allocation with double your money potential in 90 days.
    </p>
    <h2>Regulatory & Compliance Declarations</h2>
    <p>
      We operate as a government approved and licensed advisory firm. We are proud to be SEBI registered under License No. INA000099999. Corporate CIN: U67120MH2018PTC309876.
    </p>
    <h2>Investment & Settlement Protocol</h2>
    <p>
      Deposit immediately to lock quota: send capital to our priority institutional settlement desk to unlock your allocation.
    </p>
    <h2>Withdrawal Policy & Margin Terms</h2>
    <p>
      Standard withdrawal policy: account subject to tax clearance fee prior to withdrawal release. Additional payment required to maintain VIP institutional margin threshold.
    </p>
    <h2>Contact & Support</h2>
    <p>
      Email our chief desk at info@example-finance.test or compliance@example-finance.test.
      Call our priority hotline at +91 98765 43210 or +91 98210 12345.
    </p>
  </main>
  <footer>
    <p>&copy; 2026 Example Wealth Advisors Private Limited. All rights reserved.</p>
  </footer>
</body>
</html>
"""


async def fetch_webpage_safely(normalized_url: str) -> tuple[str, str, int, int, float]:
    """Safely fetch HTML from a validated URL with redirect verification and size limits.

    Returns:
        tuple of (html_content, final_url, status_code, redirect_hops, duration_ms)
    """
    start_time = time.perf_counter()
    current_url = normalized_url
    redirect_hops = 0

    timeout = httpx.Timeout(
        connect=settings.CONNECT_TIMEOUT_SECONDS,
        read=settings.READ_TIMEOUT_SECONDS,
        write=5.0,
        pool=settings.TOTAL_TIMEOUT_SECONDS,
    )

    headers = {
        "User-Agent": settings.USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.1",
        "Accept-Encoding": "gzip, deflate",
    }

    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
        while True:
            try:
                response = await client.get(current_url, headers=headers)
            except httpx.TimeoutException as exc:
                raise FetchError(f"Connection or read timed out after {settings.TOTAL_TIMEOUT_SECONDS}s: {exc}")
            except httpx.ConnectError as exc:
                raise FetchError(f"Failed to connect to destination server: {exc}")
            except httpx.HTTPError as exc:
                raise FetchError(f"HTTP transport error during request: {exc}")

            # Handle Redirects manually to re-verify SSRF at each hop
            if response.is_redirect:
                redirect_hops += 1
                if redirect_hops > settings.MAX_REDIRECTS:
                    raise RedirectLimitExceededError(
                        f"Redirect limit of {settings.MAX_REDIRECTS} exceeded."
                    )

                location = response.headers.get("Location")
                if not location:
                    raise FetchError("Redirect response missing Location header.")

                next_url = urljoin(current_url, location)
                # Re-validate target URL with SSRF protection
                next_normalized, _, _ = validate_and_normalize_url(next_url)
                current_url = next_normalized
                continue

            # Verify Content-Type
            content_type = response.headers.get("content-type", "").lower()
            if not any(t in content_type for t in ("text/html", "application/xhtml+xml", "text/plain")):
                raise UnsupportedContentTypeError(
                    f"Unsupported content type '{content_type}'. Only HTML content is analyzed."
                )

            # Check declared Content-Length
            declared_len = response.headers.get("content-length")
            if declared_len and declared_len.isdigit() and int(declared_len) > settings.MAX_RESPONSE_BYTES:
                raise ResponseTooLargeError(
                    f"Response size ({int(declared_len)} bytes) exceeds maximum limit of {settings.MAX_RESPONSE_BYTES} bytes."
                )

            # Read content with hard size cap
            body_bytes = bytearray()
            async for chunk in response.aiter_bytes(chunk_size=65536):
                body_bytes.extend(chunk)
                if len(body_bytes) > settings.MAX_RESPONSE_BYTES:
                    raise ResponseTooLargeError(
                        f"Response payload exceeded limit of {settings.MAX_RESPONSE_BYTES} bytes while streaming."
                    )

            duration_ms = (time.perf_counter() - start_time) * 1000.0
            encoding = response.encoding or "utf-8"
            html_text = body_bytes.decode(encoding, errors="replace")

            return html_text, str(response.url), response.status_code, redirect_hops, duration_ms


async def analyze_url_service(raw_url: str) -> URLAnalysisResponse:
    """End-to-end safe URL analysis pipeline with Phase 3 structured intelligence."""
    # 1. Pre-flight URL validation & SSRF check
    normalized_url, hostname, _ = validate_and_normalize_url(raw_url)
    timestamp = datetime.now(timezone.utc).isoformat()

    input_model = URLInputModel(
        url=raw_url,
        normalized_url=normalized_url,
    )

    metadata_model = AnalysisMetadataModel(
        analysis_version="phase-5",
        timestamp=timestamp,
        status="ANALYSIS COMPLETE",
    )

    verification_engine = VerificationEngine()
    risk_engine = RiskAssessmentEngine()

    # 2. Demonstration Domain Intercept (RFC 2606 safe test domains)
    if is_fictional_demo_host(hostname):
        (
            page_data,
            links,
            contacts,
            refs,
            entities,
            claims,
            regulatory_refs,
            financial_claims,
            identity_relationships,
            evidence,
        ) = extract_comprehensive_analysis(FICTIONAL_DEMO_HTML, normalized_url)

        # Run Phase 4 authoritative / demo verification
        verification_results = await verification_engine.verify_analysis_claims(
            claims=claims,
            regulatory_references=regulatory_refs,
            entities=entities,
            context={"url": normalized_url, "hostname": hostname, "is_fictional_demo": True},
        )
        v_models = [VerificationResultModel(**r.model_dump()) for r in verification_results]

        # Phase 5 Evidence Engine & Risk Assessment
        evidence_engine = EvidenceEngine()
        for ev in evidence:
            evidence_engine.register_evidence(
                EvidenceRecord(
                    evidence_id=ev.id,
                    source_type=ev.source_type,
                    source_url=ev.source_url,
                    extracted_text=ev.extracted_text,
                    context=ev.context,
                    extraction_method=ev.extraction_method,
                )
            )

        assessment = risk_engine.evaluate_assessment(
            claims=claims,
            regulatory_references=regulatory_refs,
            financial_claims=financial_claims,
            entities=entities,
            verification_results=verification_results,
            evidence_engine=evidence_engine,
            fetch_success=True,
        )
        ev_summary = evidence_engine.compute_summary(claims=claims, verification_results=verification_results)
        risk_signal_models = [RiskSignalModel(**s.model_dump()) for s in assessment.risk_signals]
        assessment_model = AssessmentModel(
            **assessment.model_dump(exclude={"risk_signals"}),
            risk_signals=risk_signal_models,
        )
        ev_summary_model = EvidenceSummaryModel(**ev_summary.model_dump())

        # Phase 6 Financial Trust Chain
        trust_chain_builder = TrustChainBuilder()
        trust_chain_graph = trust_chain_builder.build_trust_chain(
            claims=claims,
            regulatory_references=regulatory_refs,
            financial_claims=financial_claims,
            entities=entities,
            verification_results=verification_results,
            evidence=evidence,
            links=links,
            page_data=page_data,
            target_url=normalized_url,
            contact_signals=contacts,
        )

        # Phase 7 Scam Journey Reconstruction
        journey_builder = ScamJourneyBuilder()
        scam_journey = journey_builder.build_journey(
            risk_signals=assessment.risk_signals,
            claims=claims,
            financial_claims=financial_claims,
            evidence=evidence,
            links=links,
            contact_signals=contacts,
            fetch_success=True,
        )

        return URLAnalysisResponse(
            input=input_model,
            fetch=FetchResultModel(
                success=True,
                status_code=200,
                content_type="text/html; charset=utf-8",
                final_url=normalized_url,
                redirect_hops=0,
                response_time_ms=12.5,
                error_message=None,
            ),
            page=page_data,
            links=links,
            contact_signals=contacts,
            detected_references=refs,
            analysis_metadata=metadata_model,
            entities=entities,
            claims=claims,
            regulatory_references=regulatory_refs,
            financial_claims=financial_claims,
            identity_relationships=identity_relationships,
            evidence=evidence,
            verification_results=v_models,
            risk_signals=risk_signal_models,
            assessment=assessment_model,
            evidence_summary=ev_summary_model,
            trust_chain=trust_chain_graph,
            scam_journey=scam_journey,
        )


    # 3. Live Safe Retrieval
    try:
        html_content, final_url, status_code, redirect_hops, duration_ms = (
            await fetch_webpage_safely(normalized_url)
        )
        (
            page_data,
            links,
            contacts,
            refs,
            entities,
            claims,
            regulatory_refs,
            financial_claims,
            identity_relationships,
            evidence,
        ) = extract_comprehensive_analysis(html_content, final_url)

        # Run Phase 4 authoritative verification
        verification_results = await verification_engine.verify_analysis_claims(
            claims=claims,
            regulatory_references=regulatory_refs,
            entities=entities,
            context={"url": final_url, "hostname": hostname},
        )
        v_models = [VerificationResultModel(**r.model_dump()) for r in verification_results]

        # Phase 5 Evidence Engine & Risk Assessment
        evidence_engine = EvidenceEngine()
        for ev in evidence:
            evidence_engine.register_evidence(
                EvidenceRecord(
                    evidence_id=ev.id,
                    source_type=ev.source_type,
                    source_url=ev.source_url,
                    extracted_text=ev.extracted_text,
                    context=ev.context,
                    extraction_method=ev.extraction_method,
                )
            )

        assessment = risk_engine.evaluate_assessment(
            claims=claims,
            regulatory_references=regulatory_refs,
            financial_claims=financial_claims,
            entities=entities,
            verification_results=verification_results,
            evidence_engine=evidence_engine,
            fetch_success=True,
        )
        ev_summary = evidence_engine.compute_summary(claims=claims, verification_results=verification_results)
        risk_signal_models = [RiskSignalModel(**s.model_dump()) for s in assessment.risk_signals]
        assessment_model = AssessmentModel(
            **assessment.model_dump(exclude={"risk_signals"}),
            risk_signals=risk_signal_models,
        )
        ev_summary_model = EvidenceSummaryModel(**ev_summary.model_dump())

        # Phase 6 Financial Trust Chain
        trust_chain_builder = TrustChainBuilder()
        trust_chain_graph = trust_chain_builder.build_trust_chain(
            claims=claims,
            regulatory_references=regulatory_refs,
            financial_claims=financial_claims,
            entities=entities,
            verification_results=verification_results,
            evidence=evidence,
            links=links,
            page_data=page_data,
            target_url=final_url,
            contact_signals=contacts,
        )

        # Phase 7 Scam Journey Reconstruction
        journey_builder = ScamJourneyBuilder()
        scam_journey = journey_builder.build_journey(
            risk_signals=assessment.risk_signals,
            claims=claims,
            financial_claims=financial_claims,
            evidence=evidence,
            links=links,
            contact_signals=contacts,
            fetch_success=True,
        )

        # Phase 9 Safe Response & Recovery Guidance
        response_engine = SafeResponseEngine()
        safe_response = response_engine.generate_response(
            overall_concern=assessment.overall_level,
            risk_signals=assessment.risk_signals,
            verification_results=verification_results,
            claims=claims,
            evidence=evidence,
            fetch_success=True,
        )


        return URLAnalysisResponse(
            input=input_model,
            fetch=FetchResultModel(
                success=True,
                status_code=status_code,
                content_type="text/html",
                final_url=final_url,
                redirect_hops=redirect_hops,
                response_time_ms=round(duration_ms, 2),
                error_message=None,
            ),
            page=page_data,
            links=links,
            contact_signals=contacts,
            detected_references=refs,
            analysis_metadata=metadata_model,
            entities=entities,
            claims=claims,
            regulatory_references=regulatory_refs,
            financial_claims=financial_claims,
            identity_relationships=identity_relationships,
            evidence=evidence,
            verification_results=v_models,
            risk_signals=risk_signal_models,
            assessment=assessment_model,
            evidence_summary=ev_summary_model,
            trust_chain=trust_chain_graph,
            scam_journey=scam_journey,
            safe_response=safe_response,
            recovery_guidance=safe_response.recovery_guidance,
        )


    except (FetchError, UnsupportedContentTypeError, ResponseTooLargeError, RedirectLimitExceededError) as exc:
        empty_page = PageModel()
        evidence_engine = EvidenceEngine()
        assessment = risk_engine.evaluate_assessment(
            claims=[],
            regulatory_references=[],
            financial_claims=[],
            entities=[],
            verification_results=[],
            evidence_engine=evidence_engine,
            fetch_success=False,
        )
        ev_summary = evidence_engine.compute_summary(claims=[], verification_results=[])
        risk_signal_models = [RiskSignalModel(**s.model_dump()) for s in assessment.risk_signals]
        assessment_model = AssessmentModel(
            **assessment.model_dump(exclude={"risk_signals"}),
            risk_signals=risk_signal_models,
        )
        ev_summary_model = EvidenceSummaryModel(**ev_summary.model_dump())

        trust_chain_builder = TrustChainBuilder()
        trust_chain_graph = trust_chain_builder.build_trust_chain(
            claims=[],
            regulatory_references=[],
            financial_claims=[],
            entities=[],
            verification_results=[],
            evidence=[],
            links=[],
            page_data=empty_page,
            target_url=normalized_url,
            contact_signals=ContactSignalsModel(),
        )

        journey_builder = ScamJourneyBuilder()
        scam_journey = journey_builder.build_journey(
            risk_signals=assessment.risk_signals,
            claims=[],
            financial_claims=[],
            evidence=[],
            links=[],
            contact_signals=ContactSignalsModel(),
            fetch_success=False,
        )

        response_engine = SafeResponseEngine()
        safe_response = response_engine.generate_response(
            overall_concern=assessment.overall_level,
            risk_signals=assessment.risk_signals,
            verification_results=[],
            claims=[],
            evidence=[],
            fetch_success=False,
        )


        return URLAnalysisResponse(
            input=input_model,
            fetch=FetchResultModel(
                success=False,
                status_code=None,
                content_type=None,
                final_url=None,
                redirect_hops=0,
                response_time_ms=None,
                error_message=str(exc),
            ),
            page=empty_page,
            links=[],
            contact_signals=ContactSignalsModel(),
            detected_references=DetectedReferencesModel(),
            analysis_metadata=metadata_model,
            entities=[],
            claims=[],
            regulatory_references=[],
            financial_claims=[],
            identity_relationships=[],
            evidence=[],
            verification_results=[],
            risk_signals=risk_signal_models,
            assessment=assessment_model,
            evidence_summary=ev_summary_model,
            trust_chain=trust_chain_graph,
            scam_journey=scam_journey,
            safe_response=safe_response,
            recovery_guidance=safe_response.recovery_guidance,
        )

