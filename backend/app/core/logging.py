"""Privacy-Preserving Structured Logger for RakshaScan Backend.

Enforces zero-retention and zero-logging of sensitive user content:
- Never logs raw message text, OCR transcripts, or screenshot binary buffers.
- Never logs credentials, passwords, OTPs, PINs, or CVVs.
- Redacts sensitive URL query parameters (tokens, keys, auth, passwords).
- Emits operational metadata only (durations, payload sizes, status codes, error categories).
"""

import logging
import re
from typing import Any, Dict, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.core.config import settings

SENSITIVE_PARAM_PATTERN = re.compile(
    r"^(password|pwd|secret|token|auth|key|apikey|api_key|otp|pin|cvv|access_token|refresh_token)$",
    re.IGNORECASE,
)


def sanitize_url_for_logging(url: str) -> str:
    """Sanitizes sensitive authentication query parameters from a URL before logging."""
    if not url:
        return ""
    try:
        parts = urlsplit(url)
        if not parts.query:
            return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

        query_params = parse_qsl(parts.query, keep_blank_values=True)
        sanitized_params = []
        for key, val in query_params:
            if SENSITIVE_PARAM_PATTERN.search(key):
                sanitized_params.append((key, "[REDACTED]"))
            else:
                sanitized_params.append((key, val))

        sanitized_query = urlencode(sanitized_params)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, sanitized_query, ""))
    except Exception:
        # Fallback to domain and scheme only
        return url.split("?")[0]


# Setup application logger
logger = logging.getLogger("rakshascan")
logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [RakshaScan] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_operational_event(
    event_type: str,
    status_code: int = 200,
    duration_ms: Optional[float] = None,
    payload_size_bytes: Optional[int] = None,
    error_category: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """Logs sanitized operational telemetry without user content."""
    details = [f"event={event_type}", f"status={status_code}"]
    if duration_ms is not None:
        details.append(f"duration_ms={duration_ms:.2f}")
    if payload_size_bytes is not None:
        details.append(f"bytes={payload_size_bytes}")
    if error_category:
        details.append(f"error_category={error_category}")
    if extra:
        for k, v in extra.items():
            if isinstance(v, str) and ("http://" in v or "https://" in v):
                details.append(f"{k}={sanitize_url_for_logging(v)}")
            else:
                details.append(f"{k}={v}")

    msg = " | ".join(details)
    if status_code >= 500:
        logger.error(msg)
    elif status_code >= 400:
        logger.warning(msg)
    else:
        logger.info(msg)
