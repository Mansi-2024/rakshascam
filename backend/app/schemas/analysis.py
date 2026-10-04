"""Pydantic schemas for URL analysis requests, normalized responses, and Phase 3 structured intelligence."""

from typing import List, Optional
from pydantic import BaseModel, Field


class URLAnalysisRequest(BaseModel):
    url: str = Field(
        ...,
        description="The target HTTP/HTTPS website URL to analyze.",
        examples=["https://example-finance.test"],
    )


class MessageAnalysisRequest(BaseModel):
    text: str = Field(
        ...,
        description="Pasted financial message, chat snippet, or promotional text to analyze.",
        examples=["URGENT: SEBI approved guaranteed investment opportunity. Earn 25% monthly with zero risk."],
    )


class URLInputModel(BaseModel):
    url: str
    normalized_url: str
    input_type: str = "URL"


class FetchResultModel(BaseModel):
    success: bool
    status_code: Optional[int] = None
    content_type: Optional[str] = None
    final_url: Optional[str] = None
    redirect_hops: int = 0
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None


class PageModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    canonical_url: Optional[str] = None
    headings: List[str] = Field(default_factory=list)
    text_excerpt: Optional[str] = None


class LinkItemModel(BaseModel):
    url: str
    text: str
    internal: bool


class ContactSignalsModel(BaseModel):
    emails: List[str] = Field(default_factory=list)
    phone_numbers: List[str] = Field(default_factory=list)


class ExtractedSignalModel(BaseModel):
    phrase: str
    category: str  # "regulatory_mention", "financial_claim", "registration_number", "entity"
    source: str = "page_text"
    context: Optional[str] = None


class DetectedReferencesModel(BaseModel):
    entities: List[ExtractedSignalModel] = Field(default_factory=list)
    registration_numbers: List[ExtractedSignalModel] = Field(default_factory=list)
    regulatory_mentions: List[ExtractedSignalModel] = Field(default_factory=list)
    financial_claims: List[ExtractedSignalModel] = Field(default_factory=list)


# =========================================================================
# PHASE 3 STRUCTURED INTELLIGENCE & EVIDENCE DATA MODELS
# =========================================================================

class EvidenceModel(BaseModel):
    id: str
    source_type: str = "PAGE_TEXT"  # "PAGE_TEXT", "METADATA", "LINK"
    source_url: str
    extracted_text: str
    context: str
    extraction_method: str  # "ENTITY_PATTERN", "REGULATORY_PATTERN", "FINANCIAL_PATTERN", "LINK_EXTRACTION", "METADATA_EXTRACTION"


class EntityEvidence(BaseModel):
    text: str
    context: str


class VerificationResultModel(BaseModel):
    id: str
    claim_id: Optional[str] = None
    reference_id: Optional[str] = None
    status: str  # "VERIFIED", "CONTRADICTORY", "NOT_FOUND", "UNKNOWN", "UNAVAILABLE"
    source_name: str
    source_url: Optional[str] = None
    checked_at: str
    verification_method: str
    matched_entity: Optional[str] = None
    matched_registration: Optional[str] = None
    evidence: str
    reason: str
    is_demo: bool = False


class EntityModel(BaseModel):
    id: str
    name: str
    entity_type: str  # "COMPANY", "PERSON", "ORGANIZATION", "DOMAIN", "UNKNOWN"
    source: str = "page_text"  # "page_text", "metadata", "link"
    evidence: EntityEvidence
    evidence_id: Optional[str] = None


class RegulatoryReferenceModel(BaseModel):
    id: str
    authority: str  # "SEBI", "RBI", "MCA", "NSE", "BSE", "IRDAI", "PFRDA", "GOVERNMENT"
    claim_type: str  # "REGISTERED", "APPROVED", "LICENSED", "AUTHORIZED", "REGULATORY_MENTION"
    registration_number: Optional[str] = None
    raw_text: str
    context: str
    verification_status: str = "UNKNOWN"
    evidence_id: Optional[str] = None
    verification: Optional[VerificationResultModel] = None


class FinancialClaimModel(BaseModel):
    id: str
    claim_text: str
    claim_type: str  # "GUARANTEED_RETURN", "RISK_FREE", "HIGH_RETURN", "DOUBLE_MONEY", "FIXED_RETURN", "URGENCY", "LIMITED_TIME", "ACT_NOW", "DEPOSIT_PRESSURE", "WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT", "OTHER"
    severity: str = "MEDIUM"  # "LOW", "MEDIUM", "HIGH" (nature of detected language, NOT a fraud determination)
    evidence_text: str
    context: str
    verification_status: str = "UNKNOWN"
    evidence_id: Optional[str] = None


class ClaimModel(BaseModel):
    id: str
    claim_text: str
    claim_type: str  # "REGULATORY", "FINANCIAL", "IDENTITY", "AUTHORIZATION", "OTHER"
    subject_entity_id: Optional[str] = None
    referenced_authority: Optional[str] = None
    registration_reference: Optional[str] = None
    source: str = "page_text"
    evidence_text: str
    verification_status: str = "UNKNOWN"
    evidence_id: Optional[str] = None
    verification: Optional[VerificationResultModel] = None


class IdentityRelationshipModel(BaseModel):
    id: str
    source_entity_id: str
    relationship_type: str  # "CLAIMS_AUTHORIZATION", "OPERATES_DOMAIN", "REFERENCES_REGISTRATION", "LINKS_TO_EXTERNAL", "ASSOCIATED_WITH"
    target_id_or_value: str
    description: str
    verification_status: str = "UNKNOWN"
    evidence_id: Optional[str] = None


class AnalysisMetadataModel(BaseModel):
    analysis_version: str = "phase-8"
    timestamp: str
    status: str = "ANALYSIS COMPLETE"
    input_source: str = "WEBSITE"
    ocr_uncertainty_note: Optional[str] = None
    notice: str = (
        "Extraction is informational only. RakshaScan produces evidence-backed concern assessments, not fraud verdicts. "
        "Verification results are only authoritative when derived from official statutory directories."
    )


class RiskSignalModel(BaseModel):
    signal_id: str
    category: str  # "IDENTITY", "REGULATORY", "FINANCIAL", "MANIPULATION", "TECHNICAL", "BEHAVIORAL"
    severity: str  # "LOW", "MEDIUM", "HIGH"
    title: str
    description: str
    evidence_ids: List[str] = Field(default_factory=list)
    claim_ids: List[str] = Field(default_factory=list)
    verification_ids: List[str] = Field(default_factory=list)
    confidence: str = "HIGH"
    source: str = "page_analysis"
    explanation: str
    uncertainty: Optional[str] = None


class AssessmentModel(BaseModel):
    assessment_id: str
    overall_level: str  # "LOW_CONCERN", "MODERATE_CONCERN", "HIGH_CONCERN", "INSUFFICIENT_EVIDENCE"
    summary: str
    risk_signals: List[RiskSignalModel] = Field(default_factory=list)
    evidence_count: int = 0
    verified_claim_count: int = 0
    unverified_claim_count: int = 0
    contradictory_claim_count: int = 0
    unknown_claim_count: int = 0
    uncertainty_notes: List[str] = Field(default_factory=list)
    safe_next_steps: List[str] = Field(default_factory=list)
    generated_at: str


class EvidenceSummaryModel(BaseModel):
    total_evidence_count: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    contradictory_claims: int = 0
    unknown_claims: int = 0


from app.trust_chain.models import TrustChainGraph
from app.journey.models import ScamJourney
from app.response.models import SafeResponse, RecoveryGuidance


class URLAnalysisResponse(BaseModel):
    # Phase 2 preserved fields
    input: URLInputModel
    fetch: FetchResultModel
    page: PageModel
    links: List[LinkItemModel] = Field(default_factory=list)
    contact_signals: ContactSignalsModel = Field(default_factory=ContactSignalsModel)
    detected_references: DetectedReferencesModel = Field(default_factory=DetectedReferencesModel)
    analysis_metadata: AnalysisMetadataModel

    # Phase 3 structured intelligence & evidence fields
    entities: List[EntityModel] = Field(default_factory=list)
    claims: List[ClaimModel] = Field(default_factory=list)
    regulatory_references: List[RegulatoryReferenceModel] = Field(default_factory=list)
    financial_claims: List[FinancialClaimModel] = Field(default_factory=list)
    identity_relationships: List[IdentityRelationshipModel] = Field(default_factory=list)
    evidence: List[EvidenceModel] = Field(default_factory=list)

    # Phase 4 authoritative verification results
    verification_results: List[VerificationResultModel] = Field(default_factory=list)

    # Phase 5 risk assessment & evidence summary fields
    risk_signals: List[RiskSignalModel] = Field(default_factory=list)
    assessment: Optional[AssessmentModel] = None
    evidence_summary: Optional[EvidenceSummaryModel] = None

    # Phase 6 Financial Trust Chain
    trust_chain: Optional[TrustChainGraph] = None

    # Phase 7 Scam Journey Reconstruction
    scam_journey: Optional[ScamJourney] = None

    # Phase 9 Safe Response & Recovery Guidance
    safe_response: Optional[SafeResponse] = None
    recovery_guidance: Optional[RecoveryGuidance] = None

