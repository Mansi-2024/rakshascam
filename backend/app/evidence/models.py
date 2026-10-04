"""Evidence data models for RakshaScan Phase 5."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class EvidenceRecord(BaseModel):
    """Traceable, immutable record of an observed signal or verification artifact.

    Preserves original text without lossy summarization.
    """

    evidence_id: str = Field(description="Unique deterministic or generated evidence identifier")
    source_type: str = Field(
        default="PAGE_TEXT",
        description="Source classification: PAGE_TEXT, METADATA, REGISTRY_VERIFICATION, LINK, DOMAIN",
    )
    source_url: str = Field(description="URL or endpoint from which this evidence was collected")
    extracted_text: str = Field(description="Exact observed text from the source without alteration")
    context: str = Field(description="Surrounding text excerpt or contextual container")
    extraction_method: str = Field(
        description="Extraction approach: REGULATORY_PATTERN, FINANCIAL_PATTERN, ENTITY_PATTERN, DIRECT_API, etc."
    )
    related_claim_id: Optional[str] = Field(default=None, description="Linked claim ID if applicable")
    related_entity_id: Optional[str] = Field(default=None, description="Linked entity ID if applicable")
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC creation timestamp",
    )


class EvidenceSummary(BaseModel):
    """Aggregated quantitative metrics for the evidence foundation."""

    total_evidence_count: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    contradictory_claims: int = 0
    unknown_claims: int = 0
