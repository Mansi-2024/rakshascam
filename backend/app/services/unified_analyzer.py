"""Unified Structured Intelligence Service for RakshaScan Phase 8.

Consumes NormalizedAnalysisInput from any ingestion channel (Message, Screenshot, URL)
and orchestrates the shared intelligence pipeline:
Extraction -> Verification -> Evidence -> Risk Assessment -> Trust Chain -> Scam Journey.
"""

from datetime import datetime, timezone
from typing import Optional

from app.evidence.engine import EvidenceEngine
from app.evidence.models import EvidenceRecord
from app.ingestion.image import process_screenshot_input
from app.ingestion.models import AnalysisInputType, NormalizedAnalysisInput
from app.ingestion.text import normalize_message_input
from app.journey.builder import ScamJourneyBuilder
from app.risk.engine import RiskAssessmentEngine
from app.schemas.analysis import (
    AnalysisMetadataModel,
    AssessmentModel,
    EvidenceSummaryModel,
    FetchResultModel,
    RiskSignalModel,
    URLAnalysisResponse,
    URLInputModel,
    VerificationResultModel,
)
from app.services.html_extractor import extract_comprehensive_analysis
from app.trust_chain.builder import TrustChainBuilder
from app.verification.engine import VerificationEngine
from app.response.engine import SafeResponseEngine


async def analyze_normalized_input(
    normalized: NormalizedAnalysisInput,
) -> URLAnalysisResponse:
    """Executes the shared structured intelligence pipeline on normalized analysis input."""
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Structured Intelligence Extraction
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
    ) = extract_comprehensive_analysis(
        html_content=normalized.extracted_text,
        base_url=normalized.source_url or "",
        default_source_type=normalized.source_type,
        input_type=normalized.input_type.value,
    )

    # 2. Authoritative Regulatory Verification
    verification_engine = VerificationEngine()
    verification_results = await verification_engine.verify_analysis_claims(
        claims=claims,
        regulatory_references=regulatory_refs,
        entities=entities,
        context={
            "url": normalized.source_url or "",
            "hostname": "",
            "input_type": normalized.input_type.value,
        },
    )
    v_models = [VerificationResultModel(**r.model_dump()) for r in verification_results]

    # 3. Evidence Engine & Provenance Registration
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

    # 4. Evidence-Backed Risk Assessment
    risk_engine = RiskAssessmentEngine()
    assessment = risk_engine.evaluate_assessment(
        claims=claims,
        regulatory_references=regulatory_refs,
        financial_claims=financial_claims,
        entities=entities,
        verification_results=verification_results,
        evidence_engine=evidence_engine,
        fetch_success=True,
    )
    ev_summary = evidence_engine.compute_summary(
        claims=claims, verification_results=verification_results
    )
    risk_signal_models = [
        RiskSignalModel(**s.model_dump()) for s in assessment.risk_signals
    ]
    assessment_model = AssessmentModel(
        **assessment.model_dump(exclude={"risk_signals"}),
        risk_signals=risk_signal_models,
    )
    ev_summary_model = EvidenceSummaryModel(**ev_summary.model_dump())

    # 5. Financial Trust Chain
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
        target_url=normalized.source_url or "",
        contact_signals=contacts,
    )

    # 6. Scam Journey Reconstruction
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

    # 7. Safe Response & Recovery Guidance
    response_engine = SafeResponseEngine()
    safe_response = response_engine.generate_response(
        overall_concern=assessment.overall_level,
        risk_signals=assessment.risk_signals,
        verification_results=verification_results,
        claims=claims,
        evidence=evidence,
        fetch_success=True,
    )


    ocr_uncertainty = (
        normalized.metadata.get("ocr_uncertainty")
        if normalized.input_type == AnalysisInputType.SCREENSHOT
        else None
    )

    input_model = URLInputModel(
        url=normalized.source_url or f"{normalized.input_type.value.lower()}://submitted",
        normalized_url=normalized.source_url or f"{normalized.input_type.value.lower()}://submitted",
        input_type=normalized.input_type.value,
    )

    metadata_model = AnalysisMetadataModel(
        analysis_version="phase-9",
        timestamp=timestamp,
        status="ANALYSIS COMPLETE",
        input_source=normalized.source_type,
        ocr_uncertainty_note=ocr_uncertainty,
    )

    content_type_str = (
        "text/plain; charset=utf-8"
        if normalized.input_type == AnalysisInputType.MESSAGE
        else f"image/{normalized.metadata.get('format', 'PNG').lower()}; ocr"
        if normalized.input_type == AnalysisInputType.SCREENSHOT
        else "text/html"
    )

    return URLAnalysisResponse(
        input=input_model,
        fetch=FetchResultModel(
            success=True,
            status_code=200,
            content_type=content_type_str,
            final_url=normalized.source_url,
            redirect_hops=0,
            response_time_ms=10.0,
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



async def analyze_message_service(raw_text: str) -> URLAnalysisResponse:
    """End-to-end service for analyzing copied or pasted financial messages."""
    normalized_input = normalize_message_input(raw_text)
    return await analyze_normalized_input(normalized_input)


async def analyze_screenshot_service(
    file_bytes: bytes,
    filename: Optional[str] = "screenshot.png",
    content_type: Optional[str] = "image/png",
) -> URLAnalysisResponse:
    """End-to-end service for analyzing uploaded screenshot images with local OCR."""
    normalized_input = process_screenshot_input(
        file_bytes=file_bytes,
        filename=filename,
        content_type=content_type,
    )
    return await analyze_normalized_input(normalized_input)
