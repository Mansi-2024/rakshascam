"""Message text ingestion and normalization service for RakshaScan Phase 8.

Validates pasted/copied financial messages, chat logs, and promotional snippets,
enforcing length boundaries and safe normalization without altering substantive meaning.
"""

import re
from typing import List, Tuple
from app.core.config import settings
from app.ingestion.models import AnalysisInputType, NormalizedAnalysisInput


MAX_MESSAGE_CHARACTERS = settings.MAX_MESSAGE_CHARACTERS
URL_EXTRACT_REGEX = re.compile(
    r"(?:https?://[a-zA-Z0-9.-]+(?::\d+)?(?:/[^\s<>\"]*)?|www\.[a-zA-Z0-9.-]+(?:/[^\s<>\"]*)?)",
    re.IGNORECASE,
)


class MessageValidationError(ValueError):
    """Raised when user-submitted message content fails validation."""
    pass


class MessageLengthExceededError(MessageValidationError):
    """Raised when user-submitted message exceeds character limit."""
    pass


def extract_urls_from_text(text: str) -> List[str]:
    """Extracts unique HTTP/HTTPS/WWW URLs without performing automatic crawling."""
    found: List[str] = []
    seen = set()
    for match in URL_EXTRACT_REGEX.finditer(text):
        raw_u = match.group(0).rstrip(".,;:)\"'!?")
        if raw_u.startswith("www."):
            raw_u = f"https://{raw_u}"
        if raw_u not in seen:
            seen.add(raw_u)
            found.append(raw_u)
    return found


def normalize_whitespace_safely(text: str) -> str:
    """Safely normalizes whitespace and removes hazardous control characters."""
    # Strip dangerous ASCII control chars (null bytes, bell, escape) but preserve \n, \r, \t
    cleaned = "".join(
        ch for ch in text if ch in ("\n", "\r", "\t") or (ord(ch) >= 32 and ord(ch) != 127)
    )
    # Normalize multiple blank lines to at most two
    cleaned = re.sub(r"\n\s*\n\s*\n+", "\n\n", cleaned)
    # Strip leading and trailing whitespace
    return cleaned.strip()


def normalize_message_input(raw_text: str) -> NormalizedAnalysisInput:
    """Validates and normalizes user-submitted message text into a standard analysis input.

    Raises:
        MessageValidationError: If text is empty or exceeds character constraints.
    """
    if not raw_text or not raw_text.strip():
        raise MessageValidationError(
            "Message text cannot be empty or contain only whitespace. Please provide message content to analyze."
        )

    if len(raw_text) > MAX_MESSAGE_CHARACTERS:
        raise MessageLengthExceededError(
            f"Message text exceeds maximum permitted limit of {MAX_MESSAGE_CHARACTERS} characters "
            f"(received {len(raw_text)} characters)."
        )

    clean_text = normalize_whitespace_safely(raw_text)
    if not clean_text:
        raise MessageValidationError(
            "Message text contains only control or non-printable characters."
        )

    detected_urls = extract_urls_from_text(clean_text)

    return NormalizedAnalysisInput(
        input_type=AnalysisInputType.MESSAGE,
        source_text=raw_text,
        source_url="message://submitted",
        extracted_text=clean_text,
        source_type="USER_SUBMITTED_MESSAGE",
        detected_urls=detected_urls,
        metadata={
            "raw_character_count": len(raw_text),
            "normalized_character_count": len(clean_text),
            "detected_url_count": len(detected_urls),
        },
    )
