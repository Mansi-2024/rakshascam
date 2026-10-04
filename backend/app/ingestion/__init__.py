"""RakshaScan Ingestion Package (Phase 8).

Standardizes multi-input ingestion (Website URL, User-submitted Message, Screenshot OCR)
into a unified normalized analysis input model for the structured intelligence pipeline.
"""

from app.ingestion.models import AnalysisInputType, NormalizedAnalysisInput
from app.ingestion.text import (
    MAX_MESSAGE_CHARACTERS,
    MessageValidationError,
    extract_urls_from_text,
    normalize_message_input,
    normalize_whitespace_safely,
)
from app.ingestion.image import (
    ImageValidationError,
    OCR_UNCERTAINTY_DISCLAIMER,
    create_synthetic_test_image,
    process_screenshot_input,
)

__all__ = [
    "AnalysisInputType",
    "NormalizedAnalysisInput",
    "MAX_MESSAGE_CHARACTERS",
    "MessageValidationError",
    "extract_urls_from_text",
    "normalize_message_input",
    "normalize_whitespace_safely",
    "ImageValidationError",
    "OCR_UNCERTAINTY_DISCLAIMER",
    "create_synthetic_test_image",
    "process_screenshot_input",
]
