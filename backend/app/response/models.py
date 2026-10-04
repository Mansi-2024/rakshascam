from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ResponseMode(str, Enum):
    PRE_TRANSACTION = "PRE_TRANSACTION"
    SUSPICIOUS_CONTENT = "SUSPICIOUS_CONTENT"
    POSSIBLE_ACTIVE_SCAM = "POSSIBLE_ACTIVE_SCAM"
    POST_INCIDENT = "POST_INCIDENT"
    INFORMATIONAL = "INFORMATIONAL"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class ActionState(str, Enum):
    SAFE_TO_CONTINUE_WITH_VERIFICATION = "SAFE_TO_CONTINUE_WITH_VERIFICATION"
    PAUSE_AND_VERIFY = "PAUSE_AND_VERIFY"
    HIGH_CAUTION = "HIGH_CAUTION"
    POST_INCIDENT_GUIDANCE = "POST_INCIDENT_GUIDANCE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class SafeActionType(str, Enum):
    PAUSE = "PAUSE"
    VERIFY = "VERIFY"
    DO_NOT_SHARE_CREDENTIALS = "DO_NOT_SHARE_CREDENTIALS"
    DO_NOT_INSTALL_UNKNOWN_APP = "DO_NOT_INSTALL_UNKNOWN_APP"
    DO_NOT_SEND_ADDITIONAL_MONEY = "DO_NOT_SEND_ADDITIONAL_MONEY"
    PRESERVE_EVIDENCE = "PRESERVE_EVIDENCE"
    CONTACT_OFFICIAL_CHANNEL = "CONTACT_OFFICIAL_CHANNEL"
    REPORT = "REPORT"
    CONTACT_BANK_OR_PAYMENT_PROVIDER = "CONTACT_BANK_OR_PAYMENT_PROVIDER"
    MONITOR = "MONITOR"
    SEEK_HUMAN_ASSISTANCE = "SEEK_HUMAN_ASSISTANCE"


class ActionRecommendation(BaseModel):
    action: SafeActionType
    title: str
    explanation: str
    reason: str
    evidence_ids: List[str] = Field(default_factory=list)
    verification_ids: List[str] = Field(default_factory=list)
    priority: int = 1


class IncidentEventType(str, Enum):
    FIRST_CONTACT = "FIRST_CONTACT"
    CLAIM_RECEIVED = "CLAIM_RECEIVED"
    WEBSITE_VISITED = "WEBSITE_VISITED"
    COMMUNICATION_STARTED = "COMMUNICATION_STARTED"
    PAYMENT_REQUESTED = "PAYMENT_REQUESTED"
    PAYMENT_MADE = "PAYMENT_MADE"
    WITHDRAWAL_ATTEMPT = "WITHDRAWAL_ATTEMPT"
    ADDITIONAL_PAYMENT_REQUESTED = "ADDITIONAL_PAYMENT_REQUESTED"
    ACCESS_LOST = "ACCESS_LOST"
    USER_REPORTED = "USER_REPORTED"


class IncidentTimelineEvent(BaseModel):
    event_type: IncidentEventType
    title: str
    description: str
    source: str  # e.g., "OBSERVED_EVIDENCE", "USER_INPUT", "DETECTED_CONTENT"
    evidence_ids: List[str] = Field(default_factory=list)
    timestamp: Optional[str] = None


class IncidentTimeline(BaseModel):
    events: List[IncidentTimelineEvent] = Field(default_factory=list)
    summary: str


class RecoveryStep(BaseModel):
    category: str
    title: str
    instructions: List[str]
    disclaimer: Optional[str] = None


class RecoveryGuidance(BaseModel):
    is_activated: bool = False
    activation_reason: str
    steps: List[RecoveryStep] = Field(default_factory=list)
    general_reporting_guidance: str
    account_security_steps: List[str] = Field(default_factory=list)
    disclaimer: str


class UserIncidentState(BaseModel):
    sent_money: Optional[str] = "NOT_SPECIFIED"  # "YES", "NO", "NOT_SURE", "NOT_SPECIFIED"
    shared_credentials: Optional[str] = "NOT_SPECIFIED"  # "YES", "NO", "NOT_SURE", "NOT_SPECIFIED"


class SafeResponse(BaseModel):
    response_mode: ResponseMode
    action_state: ActionState
    primary_action: SafeActionType
    recommended_actions: List[ActionRecommendation] = Field(default_factory=list)
    guidance_notes: List[str] = Field(default_factory=list)
    incident_timeline: IncidentTimeline
    recovery_guidance: Optional[RecoveryGuidance] = None
    disclaimer: str
