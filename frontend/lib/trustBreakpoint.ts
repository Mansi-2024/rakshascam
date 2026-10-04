import { WebsiteAnalysisData, TrustBreakpointData } from "@/types";

/**
 * Deterministically computes the "Where Should I Stop? / Trust Breakpoint"
 * for an analysis result based strictly on observable extracted claims,
 * risk signals, evidence IDs, and Scam Journey stages.
 *
 * Rules:
 * 1. Do NOT fabricate payment amounts or stop points if none exist.
 * 2. If an explicit deposit/payment action is detected (e.g., "Deposit ₹20,000 today"),
 *    highlight the exact amount and action: "STOP BEFORE SENDING ₹20,000".
 * 3. If risk signals exist but no explicit payment instruction was submitted,
 *    output NO_EXPLICIT_STOP with honest epistemic uncertainty.
 * 4. Connect to existing evidence_ids and stage identifiers.
 */
export function computeTrustBreakpoint(data: WebsiteAnalysisData): TrustBreakpointData {
  // If backend already provided a trust_breakpoint, use it
  if (data.trust_breakpoint) {
    return data.trust_breakpoint;
  }

  const isInsufficient =
    data.assessment?.overall_level === "INSUFFICIENT_EVIDENCE";

  if (isInsufficient) {
    return {
      status: "INSUFFICIENT_EVIDENCE",
      title: "Where should you stop?",
      action_text: "INSUFFICIENT EVIDENCE FOR STOP POINT",
      amount: null,
      reason: "The submitted content does not contain enough observable evidence to determine a specific financial stop point.",
      supporting_signals: [],
      evidence_ids: [],
      confidence: "LOW",
      disclaimer: "RakshaScan preserves uncertainty when evidence is incomplete.",
    };
  }

  // 1. Check for deposit / payment claims
  const financialClaims = data.financial_claims || [];
  const riskSignals = data.risk_signals || [];
  const scamStages = data.scam_journey?.stages || [];

  const depositClaim = financialClaims.find(
    (c) =>
      c.claim_type === "DEPOSIT_PRESSURE" ||
      c.claim_type === "WITHDRAWAL_FEE" ||
      c.claim_type === "ADVANCE_FEE" ||
      /deposit|transfer|send money|pay(?:ment)?|advance/i.test(c.claim_text || "")
  );

  const depositStage = scamStages.find(
    (s) => s.stage_type === "DEPOSIT_REQUEST" && s.status === "OBSERVED"
  );

  // Extract currency amount if present
  let extractedAmount: string | null = null;
  const currencyRegex = /(?:₹\s*[\d,]+|Rs\.?\s*[\d,]+|INR\s*[\d,]+)/i;

  if (depositClaim?.claim_text) {
    const match = depositClaim.claim_text.match(currencyRegex);
    if (match) {
      extractedAmount = match[0].trim();
    }
  }

  // If not found in deposit claim, scan raw input / text excerpt
  if (!extractedAmount) {
    const textPool = [
      data.input?.url || "",
      data.page?.text_excerpt || "",
      ...(financialClaims.map((c) => c.claim_text || "")),
    ].join(" ");
    const match = textPool.match(currencyRegex);
    if (match) {
      extractedAmount = match[0].trim();
    }
  }

  // Compile supporting signals from existing signals and claims
  const supportingSignals: string[] = [];
  const evidenceIds: string[] = [];

  const hasGuaranteed =
    financialClaims.some((c) => c.claim_type === "GUARANTEED_RETURN") ||
    riskSignals.some((s) => s.category === "FINANCIAL" && /guarantee/i.test(s.title));
  if (hasGuaranteed) supportingSignals.push("Guaranteed-return claim");

  const hasZeroRisk =
    financialClaims.some((c) => c.claim_type === "RISK_FREE") ||
    riskSignals.some((s) => s.category === "FINANCIAL" && /zero risk|risk free/i.test(s.title));
  if (hasZeroRisk) supportingSignals.push("Zero-risk claim");

  const hasUrgency =
    financialClaims.some((c) => c.claim_type === "URGENCY") ||
    riskSignals.some((s) => s.category === "MANIPULATION" && /urgency|scarcity/i.test(s.title));
  if (hasUrgency) supportingSignals.push("Urgency/scarcity pressure");

  const hasRegulatoryClaim =
    (data.regulatory_references && data.regulatory_references.length > 0) ||
    (data.detected_references?.regulatory_mentions && data.detected_references.regulatory_mentions.length > 0) ||
    riskSignals.some((s) => s.category === "REGULATORY");
  if (hasRegulatoryClaim) supportingSignals.push("Regulatory authority claim requires verification");

  if (depositClaim || depositStage) {
    supportingSignals.push(
      depositClaim?.claim_type === "WITHDRAWAL_FEE"
        ? "Withdrawal fee / tax request"
        : "Upfront deposit request"
    );
  }

  // Fallback if no specific signal phrases matched but we have risk signals
  if (supportingSignals.length === 0 && riskSignals.length > 0) {
    riskSignals.slice(0, 3).forEach((s) => supportingSignals.push(s.title));
  }

  // Collect evidence IDs
  if (depositClaim?.evidence_id) {
    evidenceIds.push(depositClaim.evidence_id);
  }
  if (depositStage?.evidence_ids) {
    evidenceIds.push(...depositStage.evidence_ids);
  }
  riskSignals.forEach((s) => {
    if (s.evidence_ids) evidenceIds.push(...s.evidence_ids);
  });
  const uniqueEvidenceIds = Array.from(new Set(evidenceIds)).filter(Boolean);

  // If an explicit deposit / payment was requested:
  if (depositClaim || depositStage || extractedAmount) {
    const actionText = extractedAmount
      ? `STOP BEFORE SENDING ${extractedAmount}`
      : "STOP BEFORE SENDING MONEY";

    return {
      status: "RECOMMENDED_STOP",
      title: "Where should you stop?",
      action_text: actionText,
      amount: extractedAmount,
      reason: "An upfront payment is requested while several high-risk claims remain unresolved.",
      supporting_signals: supportingSignals,
      evidence_ids: uniqueEvidenceIds,
      confidence: "HIGH",
      source_stage: "DEPOSIT_REQUEST",
      disclaimer: "This is a recommended stop point based on observable claims and risk signals. It intercepts the interaction before money changes hands.",
    };
  }

  // If high risk signals exist, but NO payment was requested:
  return {
    status: "NO_EXPLICIT_STOP",
    title: "Where should you stop?",
    action_text: "NO EXPLICIT PAYMENT STEP DETECTED",
    amount: null,
    reason: "RakshaScan identified risk signals, but the submitted content does not contain enough evidence to identify a specific financial transaction stop point.",
    supporting_signals: supportingSignals.length > 0 ? supportingSignals : ["No explicit transaction step observed in input"],
    evidence_ids: uniqueEvidenceIds,
    confidence: "MEDIUM",
    disclaimer: "Preserving uncertainty: No upfront payment instruction was observed in the submitted content.",
  };
}
