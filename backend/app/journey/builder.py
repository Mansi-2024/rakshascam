"""Scam Journey Reconstruction Builder for RakshaScan Phase 7.

Constructs a structured 6-stage possible interaction pattern from observed evidence
and detected risk signals, strictly adhering to non-prejudicial language and determinism.
"""

from typing import Any, Dict, List, Optional
import uuid

from app.journey.models import (
    MANDATORY_JOURNEY_DISCLAIMER,
    JourneyConfidence,
    ScamJourney,
    ScamJourneyStage,
    StageStatus,
    StageType,
)


class ScamJourneyBuilder:
    """Builds a deterministic Scam Journey Reconstruction from observed evidence and risk signals."""

    def build_journey(
        self,
        risk_signals: List[Any],
        claims: List[Any],
        financial_claims: List[Any],
        evidence: List[Any],
        links: List[Any],
        contact_signals: Any,
        fetch_success: bool = True,
    ) -> ScamJourney:
        """Constructs 6-stage possible scam journey pattern based strictly on available evidence."""
        journey_id = f"jrny-{uuid.uuid4().hex[:8]}"
        stages: List[ScamJourneyStage] = []
        all_journey_evidence_ids: List[str] = []

        # Map signals by category and title/keyword
        signals_by_type: Dict[str, List[Any]] = {}
        for sig in risk_signals:
            sig_id = getattr(sig, "signal_id", "") or (sig.get("signal_id", "") if isinstance(sig, dict) else "")
            cat = getattr(sig, "category", "") or (sig.get("category", "") if isinstance(sig, dict) else "")
            cat_str = getattr(cat, "value", str(cat)).upper()
            title = getattr(sig, "title", "") or (sig.get("title", "") if isinstance(sig, dict) else "")

            if "deposit" in title.lower() or "deposit" in sig_id.lower():
                signals_by_type.setdefault("DEPOSIT", []).append(sig)
            elif "withdraw" in title.lower() or "clearance" in title.lower() or "withdraw" in sig_id.lower():
                signals_by_type.setdefault("WITHDRAWAL", []).append(sig)
            elif "guaranteed" in title.lower() or "risk-free" in title.lower() or "doubling" in title.lower() or cat_str == "FINANCIAL":
                signals_by_type.setdefault("FINANCIAL", []).append(sig)
            elif "urgency" in title.lower() or "urgency" in sig_id.lower():
                signals_by_type.setdefault("URGENCY", []).append(sig)

        # -------------------------------------------------------------
        # STAGE 1: INITIAL_CONTACT (Order 1)
        # -------------------------------------------------------------
        urgency_sigs = signals_by_type.get("URGENCY", [])
        urgency_claims = [
            fc for fc in financial_claims
            if (getattr(fc, "claim_type", "") or (fc.get("claim_type", "") if isinstance(fc, dict) else "")) in ["URGENCY", "ACT_NOW", "LIMITED_TIME"]
        ]

        if urgency_sigs or urgency_claims:
            s1_status = StageStatus.SUSPECTED.value
            s1_signals = [getattr(s, "signal_id", "") for s in urgency_sigs]
            s1_ev_ids = []
            for fc in urgency_claims:
                eid = getattr(fc, "evidence_id", None) or (fc.get("evidence_id") if isinstance(fc, dict) else None)
                if eid and eid not in s1_ev_ids:
                    s1_ev_ids.append(eid)
            s1_desc = "Webpage utilizes aggressive urgency cues ('act now', 'limited time', quota limits) suggestive of high-pressure outbound marketing."
            s1_why = "Page text contains promotional pressure cues designed to prompt immediate response before prudent due diligence."
            s1_conf = JourneyConfidence.MEDIUM.value
            s1_uncert = "Direct outbound contact channels (e.g. unsolicited cold call or DM) cannot be confirmed without victim testimony."
        else:
            s1_status = StageStatus.UNKNOWN.value
            s1_signals = []
            s1_ev_ids = []
            s1_desc = "Initial outreach channel (unsolicited message, cold call, or social advertisement) is unobserved in webpage analysis."
            s1_why = "No direct evidence was observed on how prospective investors are initially approached."
            s1_conf = JourneyConfidence.LOW.value
            s1_uncert = "Public website inspection only observes destination content, not outbound acquisition channels."

        stage_1 = ScamJourneyStage(
            stage_id="stage-1-initial-contact",
            order=1,
            stage_type=StageType.INITIAL_CONTACT.value,
            title="Initial Contact & Outreach",
            description=s1_desc,
            status=s1_status,
            evidence_ids=s1_ev_ids,
            signal_ids=s1_signals,
            confidence=s1_conf,
            why_present=s1_why,
            uncertainty=s1_uncert,
        )
        stages.append(stage_1)
        all_journey_evidence_ids.extend(s1_ev_ids)

        # -------------------------------------------------------------
        # STAGE 2: FINANCIAL_CLAIM (Order 2)
        # -------------------------------------------------------------
        fin_sigs = signals_by_type.get("FINANCIAL", [])
        fin_claims = [
            fc for fc in financial_claims
            if (getattr(fc, "claim_type", "") or (fc.get("claim_type", "") if isinstance(fc, dict) else "")) in [
                "GUARANTEED_RETURN", "RISK_FREE", "DOUBLE_MONEY", "HIGH_RETURN", "FIXED_RETURN"
            ]
        ]

        if fin_sigs or fin_claims:
            s2_status = StageStatus.OBSERVED.value
            s2_signals = [getattr(s, "signal_id", "") for s in fin_sigs]
            s2_ev_ids = []
            for fc in fin_claims:
                eid = getattr(fc, "evidence_id", None) or (fc.get("evidence_id") if isinstance(fc, dict) else None)
                if eid and eid not in s2_ev_ids:
                    s2_ev_ids.append(eid)
            s2_desc = "Webpage explicitly promises contractual high returns, zero loss risk, or rapid principal doubling."
            s2_why = "Clear textual evidence asserting unconditional profit guarantees and capital protection detected on page."
            s2_conf = JourneyConfidence.HIGH.value
            s2_uncert = "Linguistic pattern evaluates promotional statements; underlying legal entity solvency is not audited."
        else:
            s2_status = StageStatus.NOT_OBSERVED.value
            s2_signals = []
            s2_ev_ids = []
            s2_desc = "No explicit contractual profit guarantees or zero-risk assertions were detected in the analyzed text."
            s2_why = "No financial return guarantee phrases were identified on page."
            s2_conf = JourneyConfidence.HIGH.value
            s2_uncert = None

        stage_2 = ScamJourneyStage(
            stage_id="stage-2-financial-claim",
            order=2,
            stage_type=StageType.FINANCIAL_CLAIM.value,
            title="Financial Claims & Return Promises",
            description=s2_desc,
            status=s2_status,
            evidence_ids=s2_ev_ids,
            signal_ids=s2_signals,
            confidence=s2_conf,
            why_present=s2_why,
            uncertainty=s2_uncert,
        )
        stages.append(stage_2)
        all_journey_evidence_ids.extend(s2_ev_ids)

        # -------------------------------------------------------------
        # STAGE 3: WEBSITE (Order 3)
        # -------------------------------------------------------------
        is_url_analysis = any(
            (getattr(e, "source_type", "") or (e.get("source_type", "") if isinstance(e, dict) else "")) == "PAGE_TEXT"
            for e in evidence
        )

        if fetch_success and evidence:
            s3_status = StageStatus.OBSERVED.value
            s3_ev_ids = [evidence[0].id if hasattr(evidence[0], "id") else evidence[0]["id"]]
            s3_desc = "Live public web platform hosting corporate claims, executive attributions, and promotional investment plans."
            s3_why = "Target URL was successfully fetched and verified to serve active financial presentation content."
            s3_conf = JourneyConfidence.HIGH.value
            s3_uncert = "Website hosting records establish online presence, but do not prove operational legitimacy or statutory standing."
        elif links:
            s3_status = StageStatus.OBSERVED.value
            s3_ev_ids = [evidence[0].id if hasattr(evidence[0], "id") else evidence[0]["id"]] if evidence else []
            s3_desc = f"Content directs prospective investors to destination portal link: {links[0].url}"
            s3_why = "Submitted content includes an explicit destination website or portal link."
            s3_conf = JourneyConfidence.MEDIUM.value
            s3_uncert = "Extracted link was identified within submitted material; full recursive web crawling was not performed."
        elif not fetch_success and not links and any(
            (getattr(e, "source_type", "") or (e.get("source_type", "") if isinstance(e, dict) else "")) in ("USER_SUBMITTED_MESSAGE", "SCREENSHOT_OCR")
            for e in evidence
        ):
            s3_status = StageStatus.NOT_OBSERVED.value
            s3_ev_ids = []
            s3_desc = "No destination website or web portal link was observed in the submitted content."
            s3_why = "No web URL or online presentation link was identified in the provided material."
            s3_conf = JourneyConfidence.LOW.value
            s3_uncert = "Suspicious financial interactions may occur exclusively via closed messaging groups without a standalone website."
        else:
            s3_status = StageStatus.UNKNOWN.value
            s3_ev_ids = []
            s3_desc = "Web platform content could not be retrieved or safely verified."
            s3_why = "Destination URL failed HTTP retrieval or safety checks."
            s3_conf = JourneyConfidence.LOW.value
            s3_uncert = "Offline or unreachable web infrastructure prevents inspection."

        stage_3 = ScamJourneyStage(
            stage_id="stage-3-website",
            order=3,
            stage_type=StageType.WEBSITE.value,
            title="Web Platform & Presentation",
            description=s3_desc,
            status=s3_status,
            evidence_ids=s3_ev_ids,
            signal_ids=[],
            confidence=s3_conf,
            why_present=s3_why,
            uncertainty=s3_uncert,
        )
        stages.append(stage_3)
        all_journey_evidence_ids.extend(s3_ev_ids)

        # -------------------------------------------------------------
        # STAGE 4: COMMUNICATION_CHANNEL (Order 4)
        # -------------------------------------------------------------
        phone_nums = getattr(contact_signals, "phone_numbers", []) or (contact_signals.get("phone_numbers", []) if isinstance(contact_signals, dict) else [])
        emails = getattr(contact_signals, "emails", []) or (contact_signals.get("emails", []) if isinstance(contact_signals, dict) else [])
        messaging_links: List[str] = []
        if links:
            for lk in links:
                u = getattr(lk, "url", "") or (lk.get("url", "") if isinstance(lk, dict) else "")
                if any(x in u.lower() for x in ["t.me", "telegram.me", "wa.me", "api.whatsapp.com"]):
                    messaging_links.append(u)

        if phone_nums or messaging_links or emails:
            s4_status = StageStatus.OBSERVED.value
            s4_desc = f"Identified dedicated communication points ({len(phone_nums)} phone numbers, {len(emails)} emails, {len(messaging_links)} messaging links) used to conduct direct investor communications."
            s4_why = "Page provides explicit telephone hotlines, email addresses, or chat links to guide users into direct interaction."
            s4_conf = JourneyConfidence.HIGH.value
            s4_uncert = "Observing contact handles does not reveal private chat transcripts or call recordings."
            s4_ev_ids = [evidence[0].id if hasattr(evidence[0], "id") else evidence[0]["id"]] if evidence else []
        else:
            s4_status = StageStatus.NOT_OBSERVED.value
            s4_desc = "No external messaging links or direct telephone numbers were detected on the page."
            s4_why = "Content does not expose dedicated phone numbers or private messaging channels."
            s4_conf = JourneyConfidence.MEDIUM.value
            s4_uncert = None
            s4_ev_ids = []

        stage_4 = ScamJourneyStage(
            stage_id="stage-4-communication-channel",
            order=4,
            stage_type=StageType.COMMUNICATION_CHANNEL.value,
            title="Communication Channel & Handlers",
            description=s4_desc,
            status=s4_status,
            evidence_ids=s4_ev_ids,
            signal_ids=[],
            confidence=s4_conf,
            why_present=s4_why,
            uncertainty=s4_uncert,
        )
        stages.append(stage_4)
        all_journey_evidence_ids.extend(s4_ev_ids)

        # -------------------------------------------------------------
        # STAGE 5: DEPOSIT_REQUEST (Order 5)
        # -------------------------------------------------------------
        deposit_sigs = signals_by_type.get("DEPOSIT", [])
        deposit_claims = [
            fc for fc in financial_claims
            if (getattr(fc, "claim_type", "") or (fc.get("claim_type", "") if isinstance(fc, dict) else "")) == "DEPOSIT_PRESSURE"
        ]

        if deposit_sigs or deposit_claims:
            s5_status = StageStatus.OBSERVED.value
            s5_signals = [getattr(s, "signal_id", "") for s in deposit_sigs]
            s5_ev_ids = []
            for fc in deposit_claims:
                eid = getattr(fc, "evidence_id", None) or (fc.get("evidence_id") if isinstance(fc, dict) else None)
                if eid and eid not in s5_ev_ids:
                    s5_ev_ids.append(eid)
            s5_desc = "Direct mandates urging immediate capital transfers, institutional settlement desk deposits, or quota locking."
            s5_why = "Page text directs users to send capital immediately to priority desks or minimum threshold accounts."
            s5_conf = JourneyConfidence.HIGH.value
            s5_uncert = "Evaluates textual instructions; banking destination account ownership is not queried."
        else:
            s5_status = StageStatus.NOT_OBSERVED.value
            s5_signals = []
            s5_ev_ids = []
            s5_desc = "No immediate capital transfer mandates or deposit pressure detected on the page."
            s5_why = "Text does not demand urgent funding or priority capital lock-ins."
            s5_conf = JourneyConfidence.HIGH.value
            s5_uncert = None

        stage_5 = ScamJourneyStage(
            stage_id="stage-5-deposit-request",
            order=5,
            stage_type=StageType.DEPOSIT_REQUEST.value,
            title="Deposit Request & Capital Mandate",
            description=s5_desc,
            status=s5_status,
            evidence_ids=s5_ev_ids,
            signal_ids=s5_signals,
            confidence=s5_conf,
            why_present=s5_why,
            uncertainty=s5_uncert,
        )
        stages.append(stage_5)
        all_journey_evidence_ids.extend(s5_ev_ids)

        # -------------------------------------------------------------
        # STAGE 6: WITHDRAWAL_ISSUE (Order 6)
        # -------------------------------------------------------------
        with_sigs = signals_by_type.get("WITHDRAWAL", [])
        with_claims = [
            fc for fc in financial_claims
            if (getattr(fc, "claim_type", "") or (fc.get("claim_type", "") if isinstance(fc, dict) else "")) in ["WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT"]
        ]

        if with_sigs or with_claims:
            s6_status = StageStatus.OBSERVED.value
            s6_signals = [getattr(s, "signal_id", "") for s in with_sigs]
            s6_ev_ids = []
            for fc in with_claims:
                eid = getattr(fc, "evidence_id", None) or (fc.get("evidence_id") if isinstance(fc, dict) else None)
                if eid and eid not in s6_ev_ids:
                    s6_ev_ids.append(eid)
            s6_desc = "Terms require advance clearance payments, margin maintenance fees, or tax levies before withdrawal release."
            s6_why = "Page explicitly sets upfront payment hurdles as preconditions to releasing investor funds."
            s6_conf = JourneyConfidence.HIGH.value
            s6_uncert = "Evaluates observable withdrawal policy phrasing; actual payout refusal can only be confirmed by transactional history."
        else:
            s6_status = StageStatus.NOT_OBSERVED.value
            s6_signals = []
            s6_ev_ids = []
            s6_desc = "No advance withdrawal fee requirements or release restrictions detected in page text."
            s6_why = "Content does not contain clauses requiring extra payments to release funds."
            s6_conf = JourneyConfidence.HIGH.value
            s6_uncert = None

        stage_6 = ScamJourneyStage(
            stage_id="stage-6-withdrawal-issue",
            order=6,
            stage_type=StageType.WITHDRAWAL_ISSUE.value,
            title="Withdrawal Restriction / Advance Clearance",
            description=s6_desc,
            status=s6_status,
            evidence_ids=s6_ev_ids,
            signal_ids=s6_signals,
            confidence=s6_conf,
            why_present=s6_why,
            uncertainty=s6_uncert,
        )
        stages.append(stage_6)
        all_journey_evidence_ids.extend(s6_ev_ids)

        # -------------------------------------------------------------
        # JOURNEY CONFIDENCE & SUMMARY
        # -------------------------------------------------------------
        supported_stages = [s for s in stages if s.status in [StageStatus.OBSERVED.value, StageStatus.SUSPECTED.value]]
        supported_count = len(supported_stages)

        if supported_count >= 4:
            journey_confidence = JourneyConfidence.HIGH.value
        elif supported_count >= 2:
            journey_confidence = JourneyConfidence.MEDIUM.value
        else:
            journey_confidence = JourneyConfidence.LOW.value

        summary_text = f"{supported_count} of 6 stages supported by available evidence."

        uncertainty_notes = [
            "This represents a reconstructed pattern, not a determination that a specific case is fraudulent.",
            "Journey confidence reflects evidence completeness in matching an analytical model, NOT a probability of fraud.",
            "Stages marked UNKNOWN reflect absent on-page visibility into external vectors like private chat rooms or outbound phone calls.",
            "Stages marked SUSPECTED are inferred from linguistic urgency or marketing presentation rather than direct transactional logs.",
        ]

        # Deduplicate evidence IDs
        dedup_ev_ids = list(dict.fromkeys(all_journey_evidence_ids))

        return ScamJourney(
            journey_id=journey_id,
            pattern_title="Possible scam journey pattern",
            confidence=journey_confidence,
            stages=stages,
            evidence_ids=dedup_ev_ids,
            uncertainty_notes=uncertainty_notes,
            disclaimer=MANDATORY_JOURNEY_DISCLAIMER,
            summary_text=summary_text,
        )
