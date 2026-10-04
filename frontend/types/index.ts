/**
 * RakshaScan Core Type Definitions
 * Evidence-Based Financial Scam and Trust-Verification Platform
 */

export type VerificationStatus =
  | "VERIFIED"
  | "UNVERIFIED"
  | "CONTRADICTORY"
  | "UNKNOWN";

export type RiskSeverity = "LOW" | "MEDIUM" | "HIGH";

export type AnalysisInputMode = "website" | "screenshot" | "message" | "entity";

export interface AnalysisInput {
  mode: AnalysisInputMode;
  value: string;
  file?: File | null;
  metadata?: Record<string, string>;
}

export interface Evidence {
  id: string;
  title: string;
  description: string;
  source?: string;
  sourceUrl?: string;
  timestamp?: string;
  category: "registry" | "domain" | "content" | "identity" | "financial";
  verificationStatus: VerificationStatus;
}

export interface RiskSignal {
  id: string;
  severity: RiskSeverity;
  title: string;
  description: string;
  evidenceIds?: string[];
  category?: string;
}

export type TrustChainNodeType =
  | "claim"
  | "entity"
  | "registration"
  | "official_identity"
  | "website"
  | "app"
  | "social_account"
  | "payment_identity";

export interface TrustChainNode {
  id: string;
  label: string;
  type: TrustChainNodeType;
  status: VerificationStatus;
  description?: string;
  details?: string;
  claimedValue?: string;
  verifiedValue?: string;
  evidenceList?: Evidence[];
}

export interface TrustChainRelationship {
  fromNodeId: string;
  toNodeId: string;
  relationType: string;
  status: VerificationStatus;
  notes?: string;
}

export type JourneyStageStatus =
  | "OBSERVED"
  | "SUSPECTED"
  | "NOT_DETECTED"
  | "POTENTIAL_NEXT";

export interface ScamJourneyStage {
  id: string;
  order: number;
  stageName: string;
  description: string;
  observedSignals?: string[];
  riskSeverity?: RiskSeverity;
  status: JourneyStageStatus;
}

export interface AnalysisResultFindings {
  whatWeFound: string[];
  whatWeVerified: string[];
  whatRemainsUncertain: string[];
  whyFlagged: string[];
}

export interface AnalysisResult {
  id: string;
  targetArtifact: string;
  inputMode: AnalysisInputMode;
  analyzedAt: string;
  overallConcern: RiskSeverity;
  primaryReasons: string[];
  findings: AnalysisResultFindings;
  riskSignals: RiskSignal[];
  trustChainNodes: TrustChainNode[];
  trustChainRelationships: TrustChainRelationship[];
  scamJourneyStages: ScamJourneyStage[];
  safeNextSteps: string[];
  isMockExample: boolean;
  trustBreakpoint?: TrustBreakpointData;
}

export interface ExtractedSignal {
  phrase: string;
  category: "regulatory_mention" | "financial_claim" | "registration_number" | "entity" | string;
  source: string;
  context?: string | null;
}

export interface WebsiteAnalysisData {
  input: {
    url: string;
    normalized_url: string;
    input_type?: string;
  };
  fetch: {
    success: boolean;
    status_code?: number | null;
    content_type?: string | null;
    final_url?: string | null;
    redirect_hops: number;
    response_time_ms?: number | null;
    error_message?: string | null;
  };
  page: {
    title?: string | null;
    description?: string | null;
    language?: string | null;
    canonical_url?: string | null;
    headings: string[];
    text_excerpt?: string | null;
  };
  links: Array<{
    url: string;
    text: string;
    internal: boolean;
  }>;
  contact_signals: {
    emails: string[];
    phone_numbers: string[];
  };
  detected_references: {
    entities: ExtractedSignal[];
    registration_numbers: ExtractedSignal[];
    regulatory_mentions: ExtractedSignal[];
    financial_claims: ExtractedSignal[];
  };
  analysis_metadata: {
    analysis_version: string;
    timestamp: string;
    status: string;
    input_source?: string;
    ocr_uncertainty_note?: string | null;
    notice: string;
  };
  entities?: ExtractedEntity[];
  claims?: StructuredClaim[];
  regulatory_references?: RegulatoryReference[];
  financial_claims?: StructuredFinancialClaim[];
  identity_relationships?: IdentityRelationship[];
  evidence?: EvidenceItem[];
  verification_results?: VerificationResult[];
  risk_signals?: RiskSignalItem[];
  assessment?: AssessmentData;
  evidence_summary?: EvidenceSummaryData;
  trust_chain?: TrustChainGraphData;
  scam_journey?: ScamJourneyData;
  safe_response?: SafeResponseData;
  recovery_guidance?: RecoveryGuidanceData;
  trust_breakpoint?: TrustBreakpointData;
}

export type TrustBreakpointStatus =
  | "RECOMMENDED_STOP"
  | "NO_EXPLICIT_STOP"
  | "INSUFFICIENT_EVIDENCE";

export interface TrustBreakpointData {
  status: TrustBreakpointStatus;
  title: string;
  action_text: string;
  amount?: string | null;
  reason: string;
  supporting_signals: string[];
  evidence_ids: string[];
  confidence: "LOW" | "MEDIUM" | "HIGH";
  source_stage?: string;
  disclaimer: string;
}

export interface TrustChainNodeData {
  node_id: string;
  node_type: "CLAIM" | "ENTITY" | "REGISTRATION" | "OFFICIAL_IDENTITY" | "WEBSITE" | "APP" | "SOCIAL_ACCOUNT" | "PAYMENT_IDENTITY" | string;
  label: string;
  value: string;
  status: "VERIFIED" | "UNVERIFIED" | "CONTRADICTORY" | "UNKNOWN" | "UNAVAILABLE" | "NOT_OBSERVED" | string;
  evidence_ids: string[];
  verification_ids: string[];
  metadata?: Record<string, unknown>;
}

export interface TrustChainRelationshipData {
  relationship_id: string;
  source_node_id: string;
  target_node_id: string;
  relationship_type: "CLAIMS" | "REGISTERED_AS" | "IDENTIFIED_AS" | "OPERATES" | "ASSOCIATED_WITH" | "LINKS_TO" | "USES" | "RECEIVES_PAYMENT" | string;
  status: "VERIFIED" | "UNVERIFIED" | "CONTRADICTORY" | "UNKNOWN" | "UNAVAILABLE" | "NOT_OBSERVED" | string;
  evidence_ids: string[];
  verification_ids: string[];
  explanation: string;
}

export interface TrustChainSummaryData {
  total_nodes: number;
  total_relationships: number;
  verified_count: number;
  unverified_count: number;
  contradictory_count: number;
  unknown_count: number;
  unobserved_count: number;
  summary_text: string;
}

export interface TrustChainGraphData {
  nodes: TrustChainNodeData[];
  relationships: TrustChainRelationshipData[];
  summary: TrustChainSummaryData;
}

export interface ScamJourneyStageData {
  stage_id: string;
  order: number;
  stage_type: "INITIAL_CONTACT" | "FINANCIAL_CLAIM" | "WEBSITE" | "COMMUNICATION_CHANNEL" | "DEPOSIT_REQUEST" | "WITHDRAWAL_ISSUE" | string;
  title: string;
  description: string;
  status: "OBSERVED" | "SUSPECTED" | "NOT_OBSERVED" | "UNKNOWN" | string;
  evidence_ids: string[];
  signal_ids: string[];
  confidence: "LOW" | "MEDIUM" | "HIGH" | string;
  why_present: string;
  uncertainty?: string | null;
}

export interface ScamJourneyData {
  journey_id: string;
  pattern_title: string;
  confidence: "LOW" | "MEDIUM" | "HIGH" | string;
  stages: ScamJourneyStageData[];
  evidence_ids: string[];
  uncertainty_notes: string[];
  disclaimer: string;
  summary_text: string;
}


export interface RiskSignalItem {
  signal_id: string;
  category: "IDENTITY" | "REGULATORY" | "FINANCIAL" | "MANIPULATION" | "TECHNICAL" | "BEHAVIORAL" | string;
  severity: "LOW" | "MEDIUM" | "HIGH" | string;
  title: string;
  description: string;
  evidence_ids: string[];
  claim_ids: string[];
  verification_ids: string[];
  confidence: "LOW" | "MEDIUM" | "HIGH" | string;
  source: string;
  explanation: string;
  uncertainty?: string | null;
}

export interface AssessmentData {
  assessment_id: string;
  overall_level: "LOW_CONCERN" | "MODERATE_CONCERN" | "HIGH_CONCERN" | "INSUFFICIENT_EVIDENCE" | string;
  summary: string;
  risk_signals: RiskSignalItem[];
  evidence_count: number;
  verified_claim_count: number;
  unverified_claim_count: number;
  contradictory_claim_count: number;
  unknown_claim_count: number;
  uncertainty_notes: string[];
  safe_next_steps: string[];
  generated_at: string;
}

export interface EvidenceSummaryData {
  total_evidence_count: number;
  verified_claims: number;
  unverified_claims: number;
  contradictory_claims: number;
  unknown_claims: number;
}

export interface VerificationResult {
  id: string;
  claim_id?: string | null;
  reference_id?: string | null;
  status: "VERIFIED" | "CONTRADICTORY" | "NOT_FOUND" | "UNKNOWN" | "UNAVAILABLE" | string;
  source_name: string;
  source_url?: string | null;
  checked_at: string;
  verification_method: string;
  matched_entity?: string | null;
  matched_registration?: string | null;
  evidence: string;
  reason: string;
  is_demo: boolean;
}

export interface EvidenceItem {
  id: string;
  source_type: string;
  source_url: string;
  extracted_text: string;
  context: string;
  extraction_method: string;
}

export interface ExtractedEntity {
  id: string;
  name: string;
  entity_type: "COMPANY" | "PERSON" | "ORGANIZATION" | "DOMAIN" | "UNKNOWN" | string;
  source: string;
  evidence: {
    text: string;
    context: string;
  };
  evidence_id?: string | null;
}

export interface RegulatoryReference {
  id: string;
  authority: string;
  claim_type: string;
  registration_number?: string | null;
  raw_text: string;
  context: string;
  verification_status: string;
  evidence_id?: string | null;
  verification?: VerificationResult | null;
}

export interface StructuredFinancialClaim {
  id: string;
  claim_text: string;
  claim_type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | string;
  evidence_text: string;
  context: string;
  verification_status: string;
  evidence_id?: string | null;
}

export interface StructuredClaim {
  id: string;
  claim_text: string;
  claim_type: string;
  subject_entity_id?: string | null;
  referenced_authority?: string | null;
  registration_reference?: string | null;
  source: string;
  evidence_text: string;
  verification_status: string;
  evidence_id?: string | null;
  verification?: VerificationResult | null;
}

export interface IdentityRelationship {
  id: string;
  source_entity_id: string;
  relationship_type: string;
  target_id_or_value: string;
  description: string;
  verification_status: string;
  evidence_id?: string | null;
}

export type ResponseMode =
  | "PRE_TRANSACTION"
  | "SUSPICIOUS_CONTENT"
  | "POSSIBLE_ACTIVE_SCAM"
  | "POST_INCIDENT"
  | "INFORMATIONAL"
  | "INSUFFICIENT_EVIDENCE";

export type ActionState =
  | "SAFE_TO_CONTINUE_WITH_VERIFICATION"
  | "PAUSE_AND_VERIFY"
  | "HIGH_CAUTION"
  | "POST_INCIDENT_GUIDANCE"
  | "INSUFFICIENT_EVIDENCE";

export type SafeActionType =
  | "PAUSE"
  | "VERIFY"
  | "DO_NOT_SHARE_CREDENTIALS"
  | "DO_NOT_INSTALL_UNKNOWN_APP"
  | "DO_NOT_SEND_ADDITIONAL_MONEY"
  | "PRESERVE_EVIDENCE"
  | "CONTACT_OFFICIAL_CHANNEL"
  | "REPORT"
  | "CONTACT_BANK_OR_PAYMENT_PROVIDER"
  | "MONITOR"
  | "SEEK_HUMAN_ASSISTANCE";

export interface ActionRecommendationData {
  action: SafeActionType;
  title: string;
  explanation: string;
  reason: string;
  evidence_ids: string[];
  verification_ids: string[];
  priority: number;
}

export type IncidentEventType =
  | "FIRST_CONTACT"
  | "CLAIM_RECEIVED"
  | "WEBSITE_VISITED"
  | "COMMUNICATION_STARTED"
  | "PAYMENT_REQUESTED"
  | "PAYMENT_MADE"
  | "WITHDRAWAL_ATTEMPT"
  | "ADDITIONAL_PAYMENT_REQUESTED"
  | "ACCESS_LOST"
  | "USER_REPORTED";

export interface IncidentTimelineEventData {
  event_type: IncidentEventType;
  title: string;
  description: string;
  source: string;
  evidence_ids: string[];
  timestamp?: string | null;
}

export interface IncidentTimelineData {
  events: IncidentTimelineEventData[];
  summary: string;
}

export interface RecoveryStepData {
  category: string;
  title: string;
  instructions: string[];
  disclaimer?: string | null;
}

export interface RecoveryGuidanceData {
  is_activated: boolean;
  activation_reason: string;
  steps: RecoveryStepData[];
  general_reporting_guidance: string;
  account_security_steps: string[];
  disclaimer: string;
}

export interface SafeResponseData {
  response_mode: ResponseMode;
  action_state: ActionState;
  primary_action: SafeActionType;
  recommended_actions: ActionRecommendationData[];
  guidance_notes: string[];
  incident_timeline: IncidentTimelineData;
  recovery_guidance?: RecoveryGuidanceData | null;
  disclaimer: string;
}



