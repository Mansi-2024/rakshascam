import { AnalysisResult, ScamJourneyStage, TrustChainNode, TrustChainRelationship, TrustBreakpointData } from "@/types";

/**
 * Fictional Demonstration Dataset for RakshaScan
 * Based strictly on the standard demonstration message:
 * "URGENT: SEBI approved guaranteed investment opportunity.
 *  Earn 25% monthly with zero risk.
 *  Only 10 investor slots remaining.
 *  Deposit ₹20,000 today to activate your account.
 *  To withdraw your profit, pay a refundable processing tax.
 *  Official portal: https://example-finance.test"
 *
 * NOTE: The prototype uses synthetic test records for architectural evaluation.
 * It does not perform live, automated lookups against external regulator databases.
 */

export const MOCK_TRUST_BREAKPOINT: TrustBreakpointData = {
  status: "RECOMMENDED_STOP",
  title: "Where should you stop?",
  action_text: "STOP BEFORE SENDING ₹20,000",
  amount: "₹20,000",
  reason: "RakshaScan detected multiple unresolved high-risk claims before the message asks the user to transfer money.",
  supporting_signals: [
    "Guaranteed-return claim (25% monthly)",
    "Zero-risk claim",
    "Urgency/scarcity (10 investor slots remaining)",
    "Regulatory authority claim requires verification",
    "Upfront deposit request (₹20,000)",
  ],
  evidence_ids: ["ev-deposit-01", "ev-sebi-01", "ev-return-01"],
  confidence: "HIGH",
  source_stage: "DEPOSIT_REQUEST",
  disclaimer: "This is a recommended stop point based on observable claims and risk signals. It intercepts the interaction before money changes hands.",
};

export const MOCK_TRUST_CHAIN_NODES: TrustChainNode[] = [
  {
    id: "node-claim-regulatory",
    label: "Regulatory Authority Claim",
    type: "claim",
    status: "UNVERIFIED",
    claimedValue: "'SEBI approved' investment opportunity",
    verifiedValue: "Unverified promotional claim — no official registration citation provided",
    description: "Message asserts regulatory approval as a promotional hook without license details.",
    details: "⚠️ DEMO VERIFICATION: Derived from synthetic test database records for architectural evaluation. Does not represent a live regulator confirmation.",
  },
  {
    id: "node-claim-return",
    label: "Guaranteed Return Claim",
    type: "claim",
    status: "CONTRADICTORY",
    claimedValue: "25% monthly returns with zero risk",
    verifiedValue: "Statutory rules prohibit guaranteed returns in Indian securities markets",
    description: "Claim of assured high return contradicts statutory SEBI guidelines.",
    details: "Statutory circulars strictly forbid any regulated financial intermediary from offering assured returns or risk-free equity/advisory schemes.",
  },
  {
    id: "node-urgency",
    label: "Urgency / Scarcity Vector",
    type: "claim",
    status: "UNVERIFIED",
    claimedValue: "'Only 10 investor slots remaining'",
    verifiedValue: "High-pressure psychological manipulation tactic",
    description: "Artificial scarcity used to discourage independent verification.",
    details: "Scarcity claims are frequently combined with guaranteed returns to force hurried capital commitments.",
  },
  {
    id: "node-deposit",
    label: "Deposit Action (Breakpoint)",
    type: "payment_identity",
    status: "CONTRADICTORY",
    claimedValue: "Deposit ₹20,000 today to activate account",
    verifiedValue: "Upfront capital transfer requested before verification",
    description: "The primary financial transfer vector where capital changes hands.",
    details: "Recommended Stop Point: Do not send ₹20,000 while underlying claims remain unverified.",
  },
  {
    id: "node-withdrawal-tax",
    label: "Advance-Fee Condition",
    type: "claim",
    status: "CONTRADICTORY",
    claimedValue: "Refundable processing tax to withdraw profits",
    verifiedValue: "Advance-fee lock-in pattern (Advance Fee Fraud / 419 vector)",
    description: "Demanding fees/taxes before releasing funds is a hallmark extraction tactic.",
    details: "Legitimate regulated investment portals never require upfront cash payments to release investor withdrawals.",
  },
  {
    id: "node-website",
    label: "Web Infrastructure",
    type: "website",
    status: "UNVERIFIED",
    claimedValue: "https://example-finance.test",
    verifiedValue: "Fictional demonstration endpoint (.test reserved TLD)",
    description: "Target portal URL provided in message body.",
    details: "Evaluated in a sandboxed demonstration environment.",
  },
];

export const MOCK_TRUST_CHAIN_RELATIONSHIPS: TrustChainRelationship[] = [
  {
    fromNodeId: "node-claim-regulatory",
    toNodeId: "node-claim-return",
    relationType: "asserted_alongside",
    status: "UNVERIFIED",
    notes: "SEBI approval claim used to legitimize high-yield return promise",
  },
  {
    fromNodeId: "node-claim-return",
    toNodeId: "node-urgency",
    relationType: "amplified_by",
    status: "UNVERIFIED",
    notes: "Urgency tactic accelerates decision-making before verification",
  },
  {
    fromNodeId: "node-urgency",
    toNodeId: "node-deposit",
    relationType: "pressures_into",
    status: "CONTRADICTORY",
    notes: "High-pressure claims funnel target directly to ₹20,000 deposit request",
  },
  {
    fromNodeId: "node-deposit",
    toNodeId: "node-withdrawal-tax",
    relationType: "sets_up",
    status: "CONTRADICTORY",
    notes: "Initial deposit locks victim into secondary processing tax demand",
  },
  {
    fromNodeId: "node-deposit",
    toNodeId: "node-website",
    relationType: "directs_to",
    status: "UNVERIFIED",
    notes: "Message invites deposit activation via https://example-finance.test",
  },
];

export const MOCK_SCAM_JOURNEY_STAGES: ScamJourneyStage[] = [
  {
    id: "stage-1",
    order: 1,
    stageName: "Initial contact",
    description: "Unsolicited promotional message circulating on chat apps or SMS.",
    observedSignals: ["Unsolicited message", "Urgent subject line", "High-yield hook"],
    status: "OBSERVED",
    riskSeverity: "HIGH",
  },
  {
    id: "stage-2",
    order: 2,
    stageName: "Financial claim",
    description: "Guaranteed 25% monthly return claim paired with an unverified SEBI approval assertion.",
    observedSignals: ["Guaranteed return language", "Zero-risk claim", "Unverified regulatory claim"],
    status: "OBSERVED",
    riskSeverity: "HIGH",
  },
  {
    id: "stage-3",
    order: 3,
    stageName: "Website",
    description: "Directs recipient to official-sounding portal link: https://example-finance.test.",
    observedSignals: ["External portal link", "Demonstration target domain"],
    status: "OBSERVED",
    riskSeverity: "HIGH",
  },
  {
    id: "stage-4",
    order: 4,
    stageName: "Communication channel",
    description: "Scarcity pressure: 'Only 10 investor slots remaining' to force hasty response.",
    observedSignals: ["Urgency / scarcity countdown", "Peer validation tactics"],
    status: "OBSERVED",
    riskSeverity: "MEDIUM",
  },
  {
    id: "stage-5",
    order: 5,
    stageName: "Deposit request",
    description: "Immediate capital transfer requested: 'Deposit ₹20,000 today to activate your account.'",
    observedSignals: ["Upfront deposit pressure", "Explicit ₹20,000 transfer request", "Account activation precondition"],
    status: "OBSERVED",
    riskSeverity: "HIGH",
  },
  {
    id: "stage-6",
    order: 6,
    stageName: "Withdrawal issue",
    description: "Conditioning withdrawals on extra fees: 'pay a refundable processing tax'.",
    observedSignals: ["Advance fee extraction pattern", "Processing tax demand", "Withdrawal blockage vector"],
    status: "OBSERVED",
    riskSeverity: "HIGH",
  },
];

export const MOCK_ANALYSIS_RESULT: AnalysisResult = {
  id: "assessment-demo-001",
  targetArtifact: "Fictional investment message",
  inputMode: "message",
  analyzedAt: "Fictional Demonstration Preview",
  overallConcern: "HIGH",
  primaryReasons: [
    "Guaranteed-return language",
    "Zero-risk claim",
    "Urgency/scarcity",
    "Advance deposit pressure",
    "Withdrawal fee request",
    "Regulatory claim requires verification",
  ],
  findings: {
    whatWeFound: [
      "Message asserts 'SEBI approved guaranteed investment opportunity' without citing any registered license number.",
      "Message promises 'Earn 25% monthly with zero risk' — an assurance fundamentally incompatible with regulated financial markets.",
      "Artificial scarcity mechanism observed: 'Only 10 investor slots remaining'.",
      "Explicit financial transfer requested: 'Deposit ₹20,000 today to activate your account'.",
      "Advance-fee extraction condition observed: 'To withdraw your profit, pay a refundable processing tax'.",
    ],
    whatWeVerified: [
      "Claims vs Regulatory Rules: SEBI regulations strictly prohibit registered investment entities from guaranteeing returns or claiming zero-risk.",
      "Regulatory Claim Status: Classified as an unverified promotional CLAIM, not an authoritative regulator confirmation.",
      "Demonstration Context: Derived from synthetic test database records for architectural evaluation.",
    ],
    whatRemainsUncertain: [
      "Whether the entity mentioned in the message possesses any genuine registration records cannot be confirmed from the message excerpt alone.",
      "Identity, physical location, and bank account ownership of the promoter remain unverified.",
      "Whether the portal https://example-finance.test operates independent payment gateways.",
    ],
    whyFlagged: [
      "Deceptive Financial Vector: High-yield return promises combined with urgent deposit requests match standard financial fraud lifecycles.",
      "Trust Breakpoint Trigger: User is asked to transfer ₹20,000 before any independent authorization has been verified.",
      "Advance-Fee Pattern: Conditioning withdrawals on paying upfront 'processing taxes' is a classic secondary fraud extortion tactic.",
    ],
  },
  riskSignals: [
    {
      id: "sig-1",
      severity: "HIGH",
      title: "Guaranteed Return Language",
      description: "Promises of assured 25% monthly returns violate SEBI investor protection regulations.",
      category: "financial",
    },
    {
      id: "sig-2",
      severity: "HIGH",
      title: "Zero-Risk Claim",
      description: "Asserting financial market investment has zero risk is misleading and statutorily non-compliant.",
      category: "financial",
    },
    {
      id: "sig-3",
      severity: "HIGH",
      title: "Advance Deposit Pressure",
      description: "Demanding ₹20,000 upfront deposit creates immediate financial exposure.",
      category: "financial",
    },
    {
      id: "sig-4",
      severity: "HIGH",
      title: "Withdrawal Fee / Tax Requirement",
      description: "Conditioning withdrawals on paying a refundable processing tax is an advance-fee red flag.",
      category: "financial",
    },
    {
      id: "sig-5",
      severity: "MEDIUM",
      title: "Urgency / Scarcity Manipulation",
      description: "'Only 10 investor slots remaining' induces hasty decision-making.",
      category: "manipulation",
    },
    {
      id: "sig-6",
      severity: "HIGH",
      title: "Unverified Regulatory Claim",
      description: "'SEBI approved' is an unverified promotional claim requiring authoritative check.",
      category: "regulatory",
    },
  ],
  trustChainNodes: MOCK_TRUST_CHAIN_NODES,
  trustChainRelationships: MOCK_TRUST_CHAIN_RELATIONSHIPS,
  scamJourneyStages: MOCK_SCAM_JOURNEY_STAGES,
  trustBreakpoint: MOCK_TRUST_BREAKPOINT,
  safeNextSteps: [
    "PAUSE: Do NOT transfer the requested ₹20,000 to activate any account.",
    "VERIFY: Cross-reference regulatory claims against authoritative public records before committing funds.",
    "DO NOT SEND ADDITIONAL MONEY: Never pay advance processing fees or taxes to unlock investment withdrawals.",
    "PROTECT: Never share passwords, OTPs, UPI PINs, or bank card security details.",
    "REPORT: If you have already transferred money, immediately contact your bank and file a complaint at 1930 or cybercrime.gov.in.",
  ],
  isMockExample: true,
};
