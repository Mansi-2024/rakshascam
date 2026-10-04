"""Data models for normalized analysis input ingestion in RakshaScan Phase 8.

Supports ingestion from multiple distinct surfaces (Website URL, User-submitted Message,
Screenshot OCR) while standardizing data for the shared structured intelligence pipeline.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AnalysisInputType(str, Enum):
    """Supported input ingestion channels."""
    URL = "URL"
    MESSAGE = "MESSAGE"
    SCREENSHOT = "SCREENSHOT"


class NormalizedAnalysisInput(BaseModel):
    """Normalized analysis input abstraction consumed by the unified intelligence pipeline."""
    input_type: AnalysisInputType
    source_text: Optional[str] = Field(
        default=None,
        description="Original raw text submitted by the user or extracted prior to normalization.",
    )
    source_url: Optional[str] = Field(
        default=None,
        description="Source target URL if analyzing a website or pseudo-URL scheme for tracing.",
    )
    extracted_text: str = Field(
        ...,
        description="Normalized text body ready for entity, claim, and signal extraction.",
    )
    source_type: str = Field(
        default="PAGE_TEXT",
        description="Provenance source label for generated evidence objects (e.g. PAGE_TEXT, USER_SUBMITTED_MESSAGE, SCREENSHOT_OCR).",
    )
    detected_urls: List[str] = Field(
        default_factory=list,
        description="Structured URLs discovered inside message or screenshot text (not automatically crawled).",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Supplemental ingestion metadata (e.g. OCR confidence, image dimensions, character count).",
    )
