"""Data models for RakshaScan Authoritative Verification Architecture."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    """Rigorous verification states.

    - VERIFIED: Authoritative source provides evidence supporting the claim.
    - CONTRADICTORY: Authoritative source provides evidence inconsistent with the claim.
    - NOT_FOUND: Authoritative source was successfully queried, but record was not found (NOT automatically fraud).
    - UNKNOWN: Insufficient information to determine the result (NOT automatically safe).
    - UNAVAILABLE: Authoritative source could not be reached or queried successfully (NOT not-found).
    """

    VERIFIED = "VERIFIED"
    CONTRADICTORY = "CONTRADICTORY"
    NOT_FOUND = "NOT_FOUND"
    UNKNOWN = "UNKNOWN"
    UNAVAILABLE = "UNAVAILABLE"


class VerificationResult(BaseModel):
    """Structured result of an authoritative verification inquiry.

    Guarantees strict provenance tracking and non-prejudicial explanations.
    """

    id: str = Field(description="Unique verification check identifier")
    claim_id: Optional[str] = Field(default=None, description="ID of the evaluated claim if linked")
    reference_id: Optional[str] = Field(default=None, description="ID of the evaluated regulatory reference if linked")
    status: VerificationStatus = Field(description="Verification state")
    source_name: str = Field(description="Name of the authoritative registry or demo provider")
    source_url: Optional[str] = Field(default=None, description="Official portal or verification endpoint URL")
    checked_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of verification check",
    )
    verification_method: str = Field(description="Method used: DEMO_REGISTRY_LOOKUP, DIRECT_API, etc.")
    matched_entity: Optional[str] = Field(default=None, description="Entity name recorded in authoritative registry")
    matched_registration: Optional[str] = Field(default=None, description="Registration number in registry")
    evidence: str = Field(description="Factual evidence string from the source")
    reason: str = Field(description="Objective, non-prejudicial explanation of the status")
    is_demo: bool = Field(default=False, description="True if derived from demonstration/fictional test data")
