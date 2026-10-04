"""Deterministic Risk Rules for RakshaScan Phase 5.

Implements Rules 1 through 10 with robust signal deduplication, evidence linkage,
and non-prejudicial explanations.
"""

import uuid
from typing import Any, Dict, List
from app.risk.models import RiskCategory, RiskSeverity, RiskSignal


def evaluate_risk_rules(
    claims: List[Any],
    regulatory_references: List[Any],
    financial_claims: List[Any],
    entities: List[Any],
    verification_results: List[Any],
) -> List[RiskSignal]:
    """Evaluates all inputs deterministically and returns deduplicated RiskSignals."""
    signals: List[RiskSignal] = []

    # Map helper for verification results
    verif_by_claim_or_ref: Dict[str, Any] = {}
    for vr in verification_results:
        cid = getattr(vr, "claim_id", None) or (vr.get("claim_id") if isinstance(vr, dict) else None)
        rid = getattr(vr, "reference_id", None) or (vr.get("reference_id") if isinstance(vr, dict) else None)
        if cid:
            verif_by_claim_or_ref[cid] = vr
        if rid:
            verif_by_claim_or_ref[rid] = vr

    # -------------------------------------------------------------
    # RULE 1: Guaranteed Return Language (FINANCIAL / HIGH)
    # -------------------------------------------------------------
    guaranteed_items = [
        f for f in financial_claims
        if (getattr(f, "claim_type", None) or (f.get("claim_type") if isinstance(f, dict) else None)) == "GUARANTEED_RETURN"
    ]
    if guaranteed_items:
        eids = [
            getattr(f, "evidence_id", None) or (f.get("evidence_id") if isinstance(f, dict) else None)
            for f in guaranteed_items
        ]
        cids = [
            getattr(f, "id", None) or (f.get("id") if isinstance(f, dict) else None)
            for f in guaranteed_items
        ]
        phrases = [
            getattr(f, "claim_text", "") or (f.get("claim_text", "") if isinstance(f, dict) else "")
            for f in guaranteed_items
        ]
        sample_phrase = phrases[0] if phrases else "guaranteed return"

        signals.append(
            RiskSignal(
                signal_id=f"sig-fin-guaranteed-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Guaranteed-return promise detected",
                description=(
                    f"The webpage promotes assured financial returns (e.g., '{sample_phrase}'). "
                    "In regulated financial markets, genuine investments inherently involve market risk."
                ),
                evidence_ids=[e for e in eids if e],
                claim_ids=[c for c in cids if c],
                verification_ids=[],
                confidence=RiskSeverity.HIGH,
                source="page_analysis",
                explanation="Financial products offering contractual or unconditional high returns without downside risk represent a documented risk pattern.",
                uncertainty="Analysis notes the linguistic pattern. It does not assess the solvency of the counterparty.",
            )
        )

    # -------------------------------------------------------------
    # RULE 2: Risk-Free Language (FINANCIAL / HIGH)
    # -------------------------------------------------------------
    risk_free_items = [
        f for f in financial_claims
        if (getattr(f, "claim_type", None) or (f.get("claim_type") if isinstance(f, dict) else None)) == "RISK_FREE"
    ]
    if risk_free_items:
        eids = [
            getattr(f, "evidence_id", None) or (f.get("evidence_id") if isinstance(f, dict) else None)
            for f in risk_free_items
        ]
        cids = [
            getattr(f, "id", None) or (f.get("id") if isinstance(f, dict) else None)
            for f in risk_free_items
        ]
        signals.append(
            RiskSignal(
                signal_id=f"sig-fin-riskfree-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Zero-risk / capital guarantee language detected",
                description="The page claims that capital is completely risk-free or protected against loss.",
                evidence_ids=[e for e in eids if e],
                claim_ids=[c for c in cids if c],
                verification_ids=[],
                confidence=RiskSeverity.HIGH,
                source="page_analysis",
                explanation="Legitimate investment avenues are subject to systemic and credit risks. Absolute risk-free claims violate regulatory advertising norms.",
                uncertainty="Risk assessment evaluates textual advertising; sovereign securities (e.g. RBI bonds) may have government backing.",
            )
        )

    # -------------------------------------------------------------
    # RULE 3: Double-Money Language (FINANCIAL / HIGH)
    # -------------------------------------------------------------
    double_money_items = [
        f for f in financial_claims
        if (getattr(f, "claim_type", None) or (f.get("claim_type") if isinstance(f, dict) else None)) == "DOUBLE_MONEY"
    ]
    if double_money_items:
        eids = [
            getattr(f, "evidence_id", None) or (f.get("evidence_id") if isinstance(f, dict) else None)
            for f in double_money_items
        ]
        cids = [
            getattr(f, "id", None) or (f.get("id") if isinstance(f, dict) else None)
            for f in double_money_items
        ]
        signals.append(
            RiskSignal(
                signal_id=f"sig-fin-double-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Rapid capital doubling language detected",
                description="The page contains claims of doubling investment capital in short timeframes.",
                evidence_ids=[e for e in eids if e],
                claim_ids=[c for c in cids if c],
                verification_ids=[],
                confidence=RiskSeverity.HIGH,
                source="page_analysis",
                explanation="Offers promising rapid capital multiplication are characteristic of high-risk speculative or ponzi structures.",
                uncertainty="Linguistic detection identifies the offer phrasing on the target URL.",
            )
        )

    # -------------------------------------------------------------
    # RULE 4: Deposit Pressure (MANIPULATION / HIGH)
    # -------------------------------------------------------------
    deposit_items = [
        f for f in financial_claims
        if (getattr(f, "claim_type", None) or (f.get("claim_type") if isinstance(f, dict) else None)) == "DEPOSIT_PRESSURE"
    ]
    if deposit_items:
        eids = [
            getattr(f, "evidence_id", None) or (f.get("evidence_id") if isinstance(f, dict) else None)
            for f in deposit_items
        ]
        cids = [
            getattr(f, "id", None) or (f.get("id") if isinstance(f, dict) else None)
            for f in deposit_items
        ]
        signals.append(
            RiskSignal(
                signal_id=f"sig-manip-deposit-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.MANIPULATION,
                severity=RiskSeverity.HIGH,
                title="Immediate deposit pressure detected",
                description="The page emphasizes immediate capital transfers, minimum deposit thresholds, or urgent top-ups.",
                evidence_ids=[e for e in eids if e],
                claim_ids=[c for c in cids if c],
                verification_ids=[],
                confidence=RiskSeverity.HIGH,
                source="page_analysis",
                explanation="Urgent deposit mandates are frequently utilized in social engineering to restrict deliberate investor consideration.",
                uncertainty="Linguistic observation indicates pressure phrasing; minimum account sizes can also exist legitimately.",
            )
        )

    # -------------------------------------------------------------
    # RULE 5: Withdrawal Fee / Additional Payment (FINANCIAL / HIGH)
    # -------------------------------------------------------------
    withdrawal_items = [
        f for f in financial_claims
        if (getattr(f, "claim_type", None) or (f.get("claim_type") if isinstance(f, dict) else None)) in ["WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT"]
    ]
    if withdrawal_items:
        eids = [
            getattr(f, "evidence_id", None) or (f.get("evidence_id") if isinstance(f, dict) else None)
            for f in withdrawal_items
        ]
        cids = [
            getattr(f, "id", None) or (f.get("id") if isinstance(f, dict) else None)
            for f in withdrawal_items
        ]
        signals.append(
            RiskSignal(
                signal_id=f"sig-fin-withdraw-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Upfront withdrawal fee or clearance payment demand detected",
                description="Text requires advance clearance payments, margin releases, or tax levies before user withdrawals are permitted.",
                evidence_ids=[e for e in eids if e],
                claim_ids=[c for c in cids if c],
                verification_ids=[],
                confidence=RiskSeverity.HIGH,
                source="page_analysis",
                explanation="Requiring external upfront payments to release existing balances is an adversarial extraction pattern.",
                uncertainty="Regulatory statutory deductions (TDS) exist, but are normally deducted at source rather than demanded as upfront deposits.",
            )
        )

    # -------------------------------------------------------------
    # RULE 6: Urgency / Act Now (MANIPULATION / MEDIUM)
    # -------------------------------------------------------------
    urgency_items = [
        f for f in financial_claims
        if (getattr(f, "claim_type", None) or (f.get("claim_type") if isinstance(f, dict) else None)) in ["URGENCY", "ACT_NOW", "LIMITED_TIME"]
    ]
    if urgency_items:
        eids = [
            getattr(f, "evidence_id", None) or (f.get("evidence_id") if isinstance(f, dict) else None)
            for f in urgency_items
        ]
        cids = [
            getattr(f, "id", None) or (f.get("id") if isinstance(f, dict) else None)
            for f in urgency_items
        ]
        signals.append(
            RiskSignal(
                signal_id=f"sig-manip-urgency-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.MANIPULATION,
                severity=RiskSeverity.MEDIUM,
                title="High-pressure urgency language detected",
                description="Marketing language employs artificial deadlines ('limited time', 'act now', 'slots closing').",
                evidence_ids=[e for e in eids if e],
                claim_ids=[c for c in cids if c],
                verification_ids=[],
                confidence=RiskSeverity.MEDIUM,
                source="page_analysis",
                explanation="High-pressure temporal cues aim to induce impulsive financial commitments without prudent due diligence.",
                uncertainty="Commercial promotional campaigns often use limited-time discounts; urgency alone does not imply fraud.",
            )
        )

    # -------------------------------------------------------------
    # Check Verification Results for Rules 7, 8, 9, 10
    # -------------------------------------------------------------
    # Identify unique verification states across regulatory claims & references
    reg_contradictions = []
    reg_not_founds = []
    reg_unverifieds = []
    identity_mismatches = []

    for v_res in verification_results:
        raw_status = getattr(v_res, "status", None) or (v_res.get("status") if isinstance(v_res, dict) else "")
        status = getattr(raw_status, "value", str(raw_status)).upper()
        if "VERIFICATIONSTATUS." in status:
            status = status.replace("VERIFICATIONSTATUS.", "")

        vid = getattr(v_res, "id", None) or (v_res.get("id") if isinstance(v_res, dict) else "")
        cid = getattr(v_res, "claim_id", None) or (v_res.get("claim_id") if isinstance(v_res, dict) else "")
        matched_ent = getattr(v_res, "matched_entity", None) or (v_res.get("matched_entity") if isinstance(v_res, dict) else "")
        reason = getattr(v_res, "reason", "") or (v_res.get("reason", "") if isinstance(v_res, dict) else "")

        if status == "CONTRADICTORY":
            reg_contradictions.append(v_res)
            # If the reason indicates different entity ownership, also flag identity mismatch
            if matched_ent or "different entity" in reason.lower() or "contradicts" in reason.lower():
                identity_mismatches.append(v_res)
        elif status == "NOT_FOUND":
            reg_not_founds.append(v_res)
        elif status in ["UNKNOWN", "UNAVAILABLE"]:
            reg_unverifieds.append(v_res)

    # -------------------------------------------------------------
    # RULE 8: Regulatory Contradiction (REGULATORY / HIGH)
    # -------------------------------------------------------------
    if reg_contradictions:
        vids = [
            getattr(v, "id", None) or (v.get("id") if isinstance(v, dict) else None)
            for v in reg_contradictions
        ]
        cids = [
            getattr(v, "claim_id", None) or (v.get("claim_id") if isinstance(v, dict) else None)
            for v in reg_contradictions
        ]
        sample_v = reg_contradictions[0]
        sample_reason = getattr(sample_v, "reason", "") or (sample_v.get("reason", "") if isinstance(sample_v, dict) else "")

        signals.append(
            RiskSignal(
                signal_id=f"sig-reg-contradiction-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.REGULATORY,
                severity=RiskSeverity.HIGH,
                title="Regulatory identity contradiction detected",
                description=(
                    f"Official registry verification contradicts the on-page claim. {sample_reason}"
                ),
                evidence_ids=[],
                claim_ids=[c for c in cids if c],
                verification_ids=[v for v in vids if v],
                confidence=RiskSeverity.HIGH,
                source="authoritative_verification",
                explanation="The registration reference exists in the authoritative registry, but is associated with a different legal entity.",
                uncertainty="Analysis reflects the current authoritative registry snapshot. Does not assert intent or judicial fraud.",
            )
        )

    # -------------------------------------------------------------
    # RULE 10: Entity Identity Mismatch (IDENTITY / HIGH)
    # -------------------------------------------------------------
    if identity_mismatches:
        vids = [
            getattr(v, "id", None) or (v.get("id") if isinstance(v, dict) else None)
            for v in identity_mismatches
        ]
        sample_v = identity_mismatches[0]
        matched_ent = getattr(sample_v, "matched_entity", None) or (sample_v.get("matched_entity") if isinstance(sample_v, dict) else "another registered firm")
        matched_reg = getattr(sample_v, "matched_registration", None) or (sample_v.get("matched_registration") if isinstance(sample_v, dict) else "")

        signals.append(
            RiskSignal(
                signal_id=f"sig-id-mismatch-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.IDENTITY,
                severity=RiskSeverity.HIGH,
                title="Identity mismatch: Registration belongs to different entity",
                description=(
                    f"Registration {matched_reg} is officially registered to '{matched_ent}', "
                    "differing from the entity operating this web presentation."
                ),
                evidence_ids=[],
                claim_ids=[],
                verification_ids=[v for v in vids if v],
                confidence=RiskSeverity.HIGH,
                source="authoritative_verification",
                explanation="Impersonation or borrowing another entity's regulatory license is a primary indicator of unauthorized financial operation.",
                uncertainty="Corporate subsidiary relationships or recent name changes may explain discrepancies if legal documentation is furnished.",
            )
        )

    # -------------------------------------------------------------
    # RULE 9: Registration Not Found (REGULATORY / MEDIUM)
    # -------------------------------------------------------------
    if reg_not_founds:
        vids = [
            getattr(v, "id", None) or (v.get("id") if isinstance(v, dict) else None)
            for v in reg_not_founds
        ]
        signals.append(
            RiskSignal(
                signal_id=f"sig-reg-notfound-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.REGULATORY,
                severity=RiskSeverity.MEDIUM,
                title="Registration could not be found in checked source",
                description="The claimed regulatory identifier could not be located in the queried registry database.",
                evidence_ids=[],
                claim_ids=[],
                verification_ids=[v for v in vids if v],
                confidence=RiskSeverity.MEDIUM,
                source="authoritative_verification",
                explanation="The queried registry returned zero matches for the cited registration number. Note: Not found does not by itself establish fraud.",
                uncertainty="Registrations may be newly filed, pending publication, or recorded under alternate typographical conventions.",
            )
        )

    # -------------------------------------------------------------
    # RULE 7: Regulatory Claim Requiring Verification (REGULATORY / MEDIUM)
    # -------------------------------------------------------------
    # If a regulatory reference or claim exists but has not been verified (UNKNOWN or UNAVAILABLE)
    # and no contradictory/not_found signal was already raised for it
    if (regulatory_references or [c for c in claims if (getattr(c, "claim_type", None) or (c.get("claim_type") if isinstance(c, dict) else None)) == "REGULATORY"]) and not reg_contradictions and not reg_not_founds:
        # Check if any claim remains UNKNOWN or UNAVAILABLE
        unverified_claims = [
            c for c in claims
            if (getattr(c, "claim_type", None) or (c.get("claim_type") if isinstance(c, dict) else None)) == "REGULATORY"
            and (getattr(c, "verification_status", None) or (c.get("verification_status") if isinstance(c, dict) else "UNKNOWN")) in ["UNKNOWN", "UNAVAILABLE"]
        ]
        if unverified_claims or regulatory_references:
            cids = [
                getattr(c, "id", None) or (c.get("id") if isinstance(c, dict) else None)
                for c in unverified_claims
            ]
            signals.append(
                RiskSignal(
                    signal_id=f"sig-reg-unverified-{uuid.uuid4().hex[:6]}",
                    category=RiskCategory.REGULATORY,
                    severity=RiskSeverity.MEDIUM,
                    title="Regulatory claim requires verification",
                    description="The webpage references regulatory authorization (e.g. SEBI, RBI, MCA) that has not yet been independently verified.",
                    evidence_ids=[],
                    claim_ids=[c for c in cids if c],
                    verification_ids=[],
                    confidence=RiskSeverity.MEDIUM,
                    source="page_analysis",
                    explanation="Statutory credentials claimed on marketing websites must be independently cross-checked on official regulator portals before transferring capital.",
                    uncertainty="The claim is unverified, NOT false. Verification remains pending or the official portal requires interactive lookups.",
                )
            )

    return signals
