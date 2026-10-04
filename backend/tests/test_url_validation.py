"""Unit tests for URL validation, SSRF filtering, redirect limits, and response constraints."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from app.core.security import (
    SSRFSecurityError,
    URLValidationError,
    validate_and_normalize_url,
)
from app.services.url_analyzer import (
    RedirectLimitExceededError,
    ResponseTooLargeError,
    fetch_webpage_safely,
)


def test_valid_https_url():
    """1. Test that valid HTTPS URLs normalize properly."""
    # We use example-finance.test which is defined in RFC 2606 demo domains
    norm, host, ips = validate_and_normalize_url("https://example-finance.test/invest")
    assert norm == "https://example-finance.test/invest"
    assert host == "example-finance.test"
    assert len(ips) > 0


def test_valid_http_url():
    """2. Test that valid HTTP URLs normalize properly."""
    norm, host, ips = validate_and_normalize_url("http://example-finance.test:80/portal")
    assert norm == "http://example-finance.test:80/portal"
    assert host == "example-finance.test"
    assert len(ips) > 0


def test_javascript_url_rejection():
    """3. Test that javascript: scheme URLs are strictly rejected."""
    with pytest.raises(URLValidationError, match="disallowed"):
        validate_and_normalize_url("javascript:alert(document.domain)")


def test_file_url_rejection():
    """4. Test that file: scheme URLs are strictly rejected."""
    with pytest.raises(URLValidationError, match="disallowed"):
        validate_and_normalize_url("file:///etc/passwd")


def test_localhost_rejection():
    """5. Test that localhost targets are strictly blocked."""
    with pytest.raises(SSRFSecurityError, match="prohibited"):
        validate_and_normalize_url("http://localhost:8080/admin")

    with pytest.raises(SSRFSecurityError, match="prohibited"):
        validate_and_normalize_url("http://app.localhost/status")


def test_private_ip_rejection():
    """6. Test that private RFC 1918 IP addresses are rejected."""
    with pytest.raises(SSRFSecurityError, match="private"):
        validate_and_normalize_url("http://192.168.1.1/router")

    with pytest.raises(SSRFSecurityError, match="private"):
        validate_and_normalize_url("http://10.0.0.5:8000/internal")

    with pytest.raises(SSRFSecurityError, match="private"):
        validate_and_normalize_url("http://172.16.0.10/")


def test_loopback_rejection():
    """7. Test that loopback IPv4 and IPv6 addresses are blocked."""
    with pytest.raises(SSRFSecurityError, match="loopback"):
        validate_and_normalize_url("http://127.0.0.1:3000")

    with pytest.raises(SSRFSecurityError, match="loopback"):
        validate_and_normalize_url("http://127.0.0.254")

    with pytest.raises(SSRFSecurityError, match="loopback"):
        validate_and_normalize_url("http://[::1]/")


def test_oversized_response_handling():
    """8. Test that responses declaring or streaming > 5MB are halted."""
    async def _run():
        mock_resp = MagicMock()
        mock_resp.is_redirect = False
        mock_resp.headers = {
            "content-type": "text/html",
            "content-length": str(6 * 1024 * 1024),  # 6 MB
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_resp

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            with pytest.raises(ResponseTooLargeError, match="exceeds maximum limit"):
                await fetch_webpage_safely("https://example-finance.test/large-file")

    asyncio.run(_run())


def test_redirect_limit():
    """9. Test that exceeding 3 redirects raises RedirectLimitExceededError."""
    async def _run():
        redirect_resp = MagicMock()
        redirect_resp.is_redirect = True
        redirect_resp.headers = {"Location": "https://example-finance.test/hop"}

        mock_client = AsyncMock()
        mock_client.get.return_value = redirect_resp

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client_cls.return_value.__aenter__.return_value = mock_client
            with pytest.raises(RedirectLimitExceededError, match="Redirect limit of 3 exceeded"):
                await fetch_webpage_safely("https://example-finance.test/redirect-loop")

    asyncio.run(_run())
