"""Comprehensive unit and integration tests for RakshaScan Phase 8 Multi-Input Ingestion.

Validates:
1. Message analysis (valid, empty, oversized, financial claims, urgency, deposit, withdrawal)
2. Message evidence traceability, trust chain, and scam journey integration
3. Screenshot OCR analysis (PNG, JPEG, unsupported types, oversized payload)
4. OCR evidence creation, pipeline flow, trust chain, scam journey, and privacy guarantees
5. URL extraction from text without automated recursive crawling
"""

import os
import pytest
from httpx import ASGITransport, AsyncClient

from app.ingestion.image import (
    ALLOWED_MIME_TYPES,
    MAX_IMAGE_BYTES,
    ImageValidationError,
    create_synthetic_test_image,
    process_screenshot_input,
)
from app.ingestion.models import AnalysisInputType
from app.ingestion.text import (
    MAX_MESSAGE_CHARACTERS,
    MessageValidationError,
    extract_urls_from_text,
    normalize_message_input,
)
from app.main import app
from app.services.unified_analyzer import (
    analyze_message_service,
    analyze_screenshot_service,
)
from app.trust_chain.models import TrustChainStatus


# =========================================================================
# MESSAGE INGESTION & PIPELINE TESTS
# =========================================================================

DEMO_SUSPICIOUS_MESSAGE = (
    "URGENT: SEBI approved guaranteed investment opportunity. "
    "Earn 25% monthly with zero risk. "
    "Only 10 investor slots remaining. "
    "Deposit ₹20,000 today to activate your account. "
    "To withdraw your profit, pay a refundable processing tax. "
    "Visit https://example-finance.test for VIP access."
)


def test_normalize_message_valid():
    """1. Test valid message normalization."""
    raw = "   SEBI approved guaranteed return of 30% monthly. Join today!   "
    normalized = normalize_message_input(raw)
    assert normalized.input_type == AnalysisInputType.MESSAGE
    assert normalized.source_type == "USER_SUBMITTED_MESSAGE"
    assert "SEBI approved guaranteed return" in normalized.extracted_text
    assert normalized.source_text == raw


def test_normalize_message_empty_rejected():
    """2. Test empty and whitespace-only message rejection."""
    with pytest.raises(MessageValidationError, match="empty or contain only whitespace"):
        normalize_message_input("")

    with pytest.raises(MessageValidationError, match="empty or contain only whitespace"):
        normalize_message_input("    \n\t   ")


def test_normalize_message_oversized_rejected():
    """3. Test rejection of messages exceeding maximum character limit."""
    oversized = "A" * (MAX_MESSAGE_CHARACTERS + 10)
    with pytest.raises(MessageValidationError, match="exceeds maximum permitted limit"):
        normalize_message_input(oversized)


@pytest.mark.anyio
async def test_message_financial_claim_extraction():
    """4. Test financial claim extraction from message."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    assert resp.input.input_type == "MESSAGE"

    claim_types = [fc.claim_type for fc in resp.financial_claims]
    assert "GUARANTEED_RETURN" in claim_types or any("guaranteed" in fc.claim_text.lower() for fc in resp.financial_claims)
    assert "RISK_FREE" in claim_types or any("zero risk" in fc.claim_text.lower() for fc in resp.financial_claims)
    assert "HIGH_RETURN" in claim_types or any("25%" in fc.claim_text.lower() for fc in resp.financial_claims)


@pytest.mark.anyio
async def test_message_urgency_extraction():
    """5. Test urgency and pressure cue extraction from message."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    sig_titles = [s.title.lower() for s in resp.risk_signals]
    has_urgency = any("urgency" in t or "pressure" in t for t in sig_titles)
    has_urgency_claim = any(fc.claim_type in ["URGENCY", "LIMITED_TIME", "ACT_NOW"] for fc in resp.financial_claims)
    assert has_urgency or has_urgency_claim


@pytest.mark.anyio
async def test_message_deposit_pressure_extraction():
    """6. Test deposit pressure extraction from message."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    sig_titles = [s.title.lower() for s in resp.risk_signals]
    has_deposit = any("deposit" in t for t in sig_titles)
    has_deposit_claim = any(fc.claim_type == "DEPOSIT_PRESSURE" for fc in resp.financial_claims)
    assert has_deposit or has_deposit_claim


@pytest.mark.anyio
async def test_message_withdrawal_fee_extraction():
    """7. Test withdrawal fee / processing tax extraction from message."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    sig_titles = [s.title.lower() for s in resp.risk_signals]
    has_withdrawal = any("withdrawal" in t or "fee" in t for t in sig_titles)
    has_withdrawal_claim = any(fc.claim_type in ["WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT"] for fc in resp.financial_claims)
    assert has_withdrawal or has_withdrawal_claim


@pytest.mark.anyio
async def test_message_evidence_traceability():
    """8. Test that all evidence objects generated from message have USER_SUBMITTED_MESSAGE source_type."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    assert len(resp.evidence) > 0
    for ev in resp.evidence:
        assert ev.source_type == "USER_SUBMITTED_MESSAGE"
        assert ev.source_url == "message://submitted"


@pytest.mark.anyio
async def test_message_trust_chain_integration():
    """9. Test Trust Chain graph generation from message input."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    assert resp.trust_chain is not None
    assert len(resp.trust_chain.nodes) == 8
    assert len(resp.trust_chain.relationships) == 7

    # Since the message contains a link (https://example-finance.test), website node is populated
    website_node = next(n for n in resp.trust_chain.nodes if n.node_type == "WEBSITE")
    assert "example-finance.test" in website_node.value

    # When message contains NO website link:
    no_link_msg = "Guaranteed 40% returns every week. Send money to account 12345."
    resp_no_link = await analyze_message_service(no_link_msg)
    website_node_no_link = next(n for n in resp_no_link.trust_chain.nodes if n.node_type == "WEBSITE")
    assert website_node_no_link.status == TrustChainStatus.NOT_OBSERVED.value


@pytest.mark.anyio
async def test_message_scam_journey_integration():
    """10. Test Scam Journey stage construction from message input."""
    resp = await analyze_message_service(DEMO_SUSPICIOUS_MESSAGE)
    assert resp.scam_journey is not None
    assert len(resp.scam_journey.stages) == 6
    assert resp.scam_journey.confidence in ["MEDIUM", "HIGH"]
    assert "mandatory" in resp.scam_journey.disclaimer.lower() or "reconstructed pattern" in resp.scam_journey.disclaimer.lower()


# =========================================================================
# SCREENSHOT / OCR INGESTION & PIPELINE TESTS
# =========================================================================

def test_screenshot_valid_png():
    """11. Test valid PNG screenshot processing with metadata OCR."""
    png_bytes = create_synthetic_test_image(
        text="SEBI approved guaranteed wealth advisors. Zero risk. Deposit 50000.",
        format_type="PNG",
    )
    normalized = process_screenshot_input(png_bytes, filename="chat.png", content_type="image/png")
    assert normalized.input_type == AnalysisInputType.SCREENSHOT
    assert normalized.source_type == "SCREENSHOT_OCR"
    assert "guaranteed wealth advisors" in normalized.extracted_text
    assert normalized.metadata["format"] == "PNG"
    assert "ocr_uncertainty" in normalized.metadata


def test_screenshot_valid_jpeg():
    """12. Test valid JPEG screenshot processing."""
    jpeg_bytes = create_synthetic_test_image(
        text="Sample promotional leaflet",
        format_type="JPEG",
    )
    normalized = process_screenshot_input(jpeg_bytes, filename="ad.jpg", content_type="image/jpeg")
    assert normalized.input_type == AnalysisInputType.SCREENSHOT
    assert normalized.metadata["format"] == "JPEG"


def test_screenshot_unsupported_mime_rejected():
    """13. Test rejection of unsupported MIME types or extensions."""
    fake_exe = b"MZ\x90\x00\x03\x00\x00\x00"
    with pytest.raises(ImageValidationError, match="Unsupported content type|Unsupported file extension"):
        process_screenshot_input(fake_exe, filename="malware.exe", content_type="application/octet-stream")


def test_screenshot_oversized_rejected():
    """14. Test rejection of oversized image payloads (> 10MB)."""
    oversized_bytes = b"\x00" * (MAX_IMAGE_BYTES + 50)
    with pytest.raises(ImageValidationError, match="exceeds the maximum limit"):
        process_screenshot_input(oversized_bytes, filename="huge.png", content_type="image/png")


@pytest.mark.anyio
async def test_screenshot_ocr_evidence_creation():
    """15. Test that screenshot OCR creates evidence with source_type == 'SCREENSHOT_OCR'."""
    png_bytes = create_synthetic_test_image(
        text="Exclusive SEBI registered investment firm. Double your money in 60 days.",
        format_type="PNG",
    )
    resp = await analyze_screenshot_service(png_bytes, filename="test_ocr.png", content_type="image/png")
    assert resp.input.input_type == "SCREENSHOT"
    assert len(resp.evidence) > 0

    ocr_ev = resp.evidence[0]
    assert ocr_ev.source_type == "SCREENSHOT_OCR"
    assert ocr_ev.source_url == "screenshot://submitted"
    assert "Double your money" in ocr_ev.extracted_text or "Exclusive SEBI" in ocr_ev.extracted_text


@pytest.mark.anyio
async def test_screenshot_pipeline_flow():
    """16. Test that OCR text enters the structured intelligence, risk assessment, and verification pipeline."""
    png_bytes = create_synthetic_test_image(
        text="SEBI approved investment. Guaranteed 40% monthly returns. Deposit ₹10,000 immediately.",
        format_type="PNG",
    )
    resp = await analyze_screenshot_service(png_bytes, filename="screenshot.png", content_type="image/png")
    assert resp.assessment is not None
    assert resp.assessment.overall_level in ["HIGH_CONCERN", "MODERATE_CONCERN"]
    assert len(resp.risk_signals) > 0


def test_screenshot_no_permanent_storage():
    """17. Test that processing does not leave permanent image files on disk."""
    png_bytes = create_synthetic_test_image(
        text="Temporary in-memory test artifact.",
        format_type="PNG",
    )
    initial_files = set(os.listdir("."))
    _ = process_screenshot_input(png_bytes, filename="temp_check.png", content_type="image/png")
    current_files = set(os.listdir("."))
    # No new file should have been written to the current working directory
    assert current_files == initial_files


@pytest.mark.anyio
async def test_screenshot_trust_chain_and_journey_integration():
    """18. Test Trust Chain and Scam Journey generation from screenshot OCR."""
    png_bytes = create_synthetic_test_image(
        text="Dr. Sharma Advisors Pvt Ltd. Guaranteed 30% return. Deposit now.",
        format_type="PNG",
    )
    resp = await analyze_screenshot_service(png_bytes, filename="ad_card.png", content_type="image/png")
    assert resp.trust_chain is not None
    assert len(resp.trust_chain.nodes) == 8
    assert resp.scam_journey is not None
    assert len(resp.scam_journey.stages) == 6


# =========================================================================
# URL EXTRACTION WITHOUT AUTO-CRAWLING TEST
# =========================================================================

def test_url_extraction_without_auto_crawl():
    """19. Test that URLs in message are extracted as structured links without automated crawling."""
    msg = "Check our portal at https://unauthorized-portal.example/login and telegram https://t.me/vipclub"
    urls = extract_urls_from_text(msg)
    assert "https://unauthorized-portal.example/login" in urls
    assert "https://t.me/vipclub" in urls


# =========================================================================
# FASTAPI ENDPOINT INTEGRATION TESTS
# =========================================================================

@pytest.mark.anyio
async def test_api_message_endpoint():
    """20. Test POST /api/v1/analyze/message HTTP endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Valid message
        res = await client.post(
            "/api/v1/analyze/message",
            json={"text": "SEBI approved advisory. 25% guaranteed monthly. Deposit ₹10,000."},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["input"]["input_type"] == "MESSAGE"
        assert len(data["risk_signals"]) > 0
        assert data["trust_chain"] is not None
        assert data["scam_journey"] is not None

        # Empty message
        err_res = await client.post(
            "/api/v1/analyze/message",
            json={"text": "   "},
        )
        assert err_res.status_code == 400
        err_data = err_res.json()
        assert err_data["detail"]["error_type"] == "MESSAGE_VALIDATION_ERROR"


@pytest.mark.anyio
async def test_api_screenshot_endpoint():
    """21. Test POST /api/v1/analyze/screenshot HTTP endpoint with multipart upload."""
    png_bytes = create_synthetic_test_image(
        text="SEBI authorized portal with zero risk guaranteed return.",
        format_type="PNG",
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Valid PNG upload
        res = await client.post(
            "/api/v1/analyze/screenshot",
            files={"file": ("screenshot.png", png_bytes, "image/png")},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["input"]["input_type"] == "SCREENSHOT"
        assert data["trust_chain"] is not None
        assert data["scam_journey"] is not None

        # Invalid extension / content type
        invalid_res = await client.post(
            "/api/v1/analyze/screenshot",
            files={"file": ("payload.exe", b"MZ12345", "application/octet-stream")},
        )
        assert invalid_res.status_code == 400
        err_data = invalid_res.json()
        assert err_data["detail"]["error_type"] == "IMAGE_VALIDATION_ERROR"
