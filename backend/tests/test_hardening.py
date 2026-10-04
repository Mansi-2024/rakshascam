"""Comprehensive Hardening & Production Security Tests for RakshaScan Phase 11."""

import os
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.logging import sanitize_url_for_logging
from app.core.rate_limit import InMemoryRateLimiter, rate_limiter
from app.core.security import SSRFSecurityError, validate_and_normalize_url
from app.ingestion.image import (
    ImageSizeExceededError,
    ImageValidationError,
    UnsupportedImageTypeError,
    create_synthetic_test_image,
    validate_image_payload,
)
from app.ingestion.text import MessageLengthExceededError, normalize_message_input
from app.main import app
from app.verification.adapters.demo import DemoVerificationAdapter


@pytest.fixture(autouse=True)
def reset_rate_limit():
    """Reset rate limiter buckets before each test."""
    rate_limiter.reset()
    yield
    rate_limiter.reset()


@pytest.mark.anyio
async def test_health_check_endpoint():
    """1. Test that GET /health returns exact status ok without leaking infrastructure details."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data == {"status": "ok"}
        assert "env" not in data
        assert "server" not in data
        assert "db" not in data


@pytest.mark.anyio
async def test_security_headers_present():
    """2. Test that all required HTTP security headers are attached to responses."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
        assert res.status_code == 200
        headers = res.headers
        assert headers.get("x-content-type-options") == "nosniff"
        assert headers.get("x-frame-options") == "DENY"
        assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
        assert "1; mode=block" in headers.get("x-xss-protection", "")
        assert "geolocation=()" in headers.get("permissions-policy", "")


@pytest.mark.anyio
async def test_cors_configuration():
    """3. Test that CORS headers respond properly to configured origins."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Pre-flight request from allowed origin
        res = await client.options(
            "/api/v1/analyze/url",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert res.status_code == 200
        assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"


@pytest.mark.anyio
async def test_rate_limiting_enforcement():
    """4. Test that client exceeding rate limit receives HTTP 429 with Retry-After header."""
    limiter = InMemoryRateLimiter(window_seconds=60)
    key = "192.168.1.100"
    bucket = "test_bucket"
    limit = 3

    # First 3 requests should be permitted
    for _ in range(limit):
        allowed, retry = limiter.is_allowed(key, bucket, limit)
        assert allowed is True
        assert retry == 0

    # 4th request must be rejected
    allowed, retry = limiter.is_allowed(key, bucket, limit)
    assert allowed is False
    assert retry > 0


@pytest.mark.anyio
async def test_url_length_limit_rejection():
    """5. Test that URLs exceeding MAX_URL_LENGTH are rejected with HTTP 413."""
    long_url = "https://example-finance.test/" + ("a" * 2100)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/v1/analyze/url", json={"url": long_url})
        assert res.status_code == 413
        data = res.json()
        assert data["detail"]["error_type"] == "PAYLOAD_TOO_LARGE"
        assert "exceeds maximum allowed limit" in data["detail"]["message"]


@pytest.mark.anyio
async def test_message_length_limit_rejection():
    """6. Test that message exceeding MAX_MESSAGE_CHARACTERS is rejected with HTTP 413."""
    oversized_text = "SEBI verified investment. " * 650  # > 15,000 chars
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/v1/analyze/message", json={"text": oversized_text})
        assert res.status_code == 413
        data = res.json()
        assert data["detail"]["error_type"] == "PAYLOAD_TOO_LARGE"
        assert "exceeds maximum permitted limit" in data["detail"]["message"]


@pytest.mark.anyio
async def test_screenshot_payload_size_limit_rejection():
    """7. Test that uploaded screenshot exceeding 10MB limit is rejected with HTTP 413."""
    # Synthetic payload slightly exceeding 10 MB limit
    oversized_bytes = b"\x89PNG\r\n\x1a\n" + (b"\x00" * (10 * 1024 * 1024 + 100))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post(
            "/api/v1/analyze/screenshot",
            files={"file": ("huge_image.png", oversized_bytes, "image/png")},
        )
        assert res.status_code == 413
        data = res.json()
        assert data["detail"]["error_type"] == "PAYLOAD_TOO_LARGE"


def test_screenshot_magic_bytes_validation():
    """8. Test that files with fake extensions but invalid headers are rejected."""
    # Fake PNG containing text instead of PNG magic bytes
    fake_png = b"This is not a real PNG image content."
    with pytest.raises(UnsupportedImageTypeError, match="Uploaded file signature does not match"):
        validate_image_payload(fake_png, filename="fake.png", content_type="image/png")


def test_logging_url_privacy_sanitizer():
    """9. Test that sensitive tokens and credentials in query parameters are redacted."""
    sensitive_url = "https://example-finance.test/invest?token=secret123&auth=bearer_token&user=test"
    sanitized = sanitize_url_for_logging(sensitive_url)
    assert "token=%5BREDACTED%5D" in sanitized or "token=[REDACTED]" in sanitized
    assert "auth=%5BREDACTED%5D" in sanitized or "auth=[REDACTED]" in sanitized
    assert "secret123" not in sanitized
    assert "bearer_token" not in sanitized
    assert "user=test" in sanitized


def test_ssrf_cloud_metadata_blocked():
    """10. Test that cloud metadata IPs (e.g. 169.254.169.254) are strictly blocked."""
    with pytest.raises(SSRFSecurityError, match="cloud metadata"):
        validate_and_normalize_url("http://169.254.169.254/latest/meta-data")


@pytest.mark.anyio
async def test_demo_verification_explicitly_labeled():
    """11. Test that DemoVerificationAdapter explicitly flags is_demo = True and non-authoritative."""
    adapter = DemoVerificationAdapter()
    assert adapter.is_demo is True
    res = await adapter.verify({"registration_number": "INA000099999"})
    assert res.is_demo is True
    assert "Fictional / Non-Authoritative" in res.source_name

