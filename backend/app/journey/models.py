"""Data models for RakshaScan Scam Journey Reconstruction."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

MANDATORY_JOURNEY_DISCLAIMER = (
    "This represents a reconstructed pattern, not a determination that a specific case is fraudulent."
)


class StageType(str, Enum):
    INITIAL_CONTACT = "INITIAL_CONTACT"
    FINANCIAL_CLAIM = "FINANCIAL_CLAIM"
    WEBSITE = "WEBSITE"
    COMMUNICATION_CHANNEL = "COMMUNICATION_CHANNEL"
    DEPOSIT_REQUEST = "DEPOSIT_REQUEST"
    WITHDRAWAL_ISSUE = "WITHDRAWAL_ISSUE"


class StageStatus(str, Enum):
    OBSERVED = "OBSERVED"
    SUSPECTED = "SUSPECTED"
    NOT_OBSERVED = "NOT_OBSERVED"
    UNKNOWN = "UNKNOWN"


class JourneyConfidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ScamJourneyStage(BaseModel):
    stage_id: str
    order: int  # 1 to 6
    stage_type: str  # INITIAL_CONTACT, FINANCIAL_CLAIM, WEBSITE, COMMUNICATION_CHANNEL, DEPOSIT_REQUEST, WITHDRAWAL_ISSUE
    title: str
    description: str
    status: str  # OBSERVED, SUSPECTED, NOT_OBSERVED, UNKNOWN
    evidence_ids: List[str] = Field(default_factory=list)
    signal_ids: List[str] = Field(default_factory=list)
    confidence: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    why_present: str = ""
    uncertainty: Optional[str] = None


class ScamJourney(BaseModel):
    journey_id: str
    pattern_title: str = "Possible scam journey pattern"
    confidence: str = "MEDIUM"  # LOW, MEDIUM, HIGH (Reflects evidence reconstruction completeness, NOT fraud probability)
    stages: List[ScamJourneyStage] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    uncertainty_notes: List[str] = Field(default_factory=list)
    disclaimer: str = MANDATORY_JOURNEY_DISCLAIMER
    summary_text: str = ""
