"""Risk and Assessment data models for RakshaScan Phase 5."""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskCategory(str, Enum):
    IDENTITY = "IDENTITY"
    REGULATORY = "REGULATORY"
    FINANCIAL = "FINANCIAL"
    MANIPULATION = "MANIPULATION"
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ConcernLevel(str, Enum):
    LOW_CONCERN = "LOW_CONCERN"
    MODERATE_CONCERN = "MODERATE_CONCERN"
    HIGH_CONCERN = "HIGH_CONCERN"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class RiskSignal(BaseModel):
    """An evidence-backed risk signal.

    Every risk signal must point to original observations, evidence objects,
    and verification results.
    """

    signal_id: str = Field(description="Unique risk signal identifier")
    category: RiskCategory = Field(description="Functional risk domain")
    severity: RiskSeverity = Field(description="Severity of the detected pattern (LOW, MEDIUM, HIGH)")
    title: str = Field(description="Concise, factual signal heading")
    description: str = Field(description="Detailed objective description of the detected signal")
    evidence_ids: List[str] = Field(default_factory=list, description="IDs of supporting EvidenceRecord objects")
    claim_ids: List[str] = Field(default_factory=list, description="IDs of linked ClaimModel objects")
    verification_ids: List[str] = Field(default_factory=list, description="IDs of linked VerificationResult objects")
    confidence: RiskSeverity = Field(
        default=RiskSeverity.HIGH,
        description="Confidence in signal detection accuracy (NOT probability of fraud)",
    )
    source: str = Field(default="page_analysis", description="Origin of the finding")
    explanation: str = Field(description="Plain-language explanation of why this signal was raised")
    uncertainty: Optional[str] = Field(
        default=None,
        description="Explicit caveats regarding what is not known or verified",
    )


class Assessment(BaseModel):
    """Overall evidence-based assessment synthesis.

    Combines risk signals, verification statistics, and explicit uncertainty notes.
    Never produces an opaque score or legal fraud verdict.
    """

    assessment_id: str = Field(description="Unique assessment identifier")
    overall_level: ConcernLevel = Field(
        description="Evidence-based concern classification: LOW_CONCERN, MODERATE_CONCERN, HIGH_CONCERN, INSUFFICIENT_EVIDENCE"
    )
    summary: str = Field(description="High-level factual summary of findings")
    risk_signals: List[RiskSignal] = Field(default_factory=list, description="Deduplicated risk signals")
    evidence_count: int = Field(default=0, description="Total count of supporting evidence items")
    verified_claim_count: int = Field(default=0, description="Claims substantiated by authoritative records")
    unverified_claim_count: int = Field(default=0, description="Claims unconfirmed due to missing/unavailable records")
    contradictory_claim_count: int = Field(default=0, description="Claims conflicting with official records")
    unknown_claim_count: int = Field(default=0, description="Claims lacking verifiable specifics")
    uncertainty_notes: List[str] = Field(default_factory=list, description="Explicit statements of uncertainty")
    safe_next_steps: List[str] = Field(default_factory=list, description="Context-specific defensive steps")
    generated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of assessment generation",
    )
