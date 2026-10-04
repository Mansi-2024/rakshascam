from typing import List, Dict, Any, Tuple
from app.response.models import (
    ResponseMode,
    ActionState,
    SafeActionType,
    ActionRecommendation,
    IncidentEventType,
    IncidentTimelineEvent,
    RecoveryStep,
    RecoveryGuidance,
    UserIncidentState,
)


def get_signal_type(sig: Any) -> str:
    """Extracts or deduces normalized signal_type from RiskSignal object or dict."""
    explicit = getattr(sig, "signal_type", None) or (sig.get("signal_type") if isinstance(sig, dict) else None)
    if explicit:
        return explicit.value if hasattr(explicit, "value") else str(explicit)

    sig_id = (getattr(sig, "signal_id", None) or (sig.get("signal_id") if isinstance(sig, dict) else "") or "").lower()
    title = (getattr(sig, "title", None) or (sig.get("title") if isinstance(sig, dict) else "") or "").lower()

    if "withdraw" in sig_id or "withdraw" in title or "clearance" in title:
        return "WITHDRAWAL_FEE"
    if "additional" in sig_id or "additional" in title or "advance fee" in title:
        return "ADDITIONAL_PAYMENT"
    if "deposit" in sig_id or "deposit" in title:
        return "DEPOSIT_PRESSURE"
    if "guaranteed" in sig_id or "guaranteed" in title or "riskfree" in sig_id or "double" in sig_id or "risk-free" in title:
        return "GUARANTEED_RETURN"
    if "impersonat" in sig_id or "impersonat" in title:
        return "IMPERSONATION_RISK"
    if "urgency" in sig_id or "urgency" in title:
        return "URGENCY_INDUCEMENT"
    if "off-platform" in sig_id or "off_platform" in sig_id or "telegram" in title or "whatsapp" in title:
        return "OFF_PLATFORM_REDIRECT"
    if "unregistered" in sig_id or "unregistered" in title:
        return "UNREGISTERED_INTERMEDIARY"
    if "mismatch" in sig_id or "mismatch" in title:
        return "REGISTRATION_MISMATCH"

    return ""


def evaluate_action_state_and_mode(
    overall_concern: str,
    risk_signals: List[Any],
    verification_results: List[Any],
    user_state: UserIncidentState,
) -> Tuple[ActionState, ResponseMode]:
    """
    Deterministically computes ActionState and ResponseMode.
    Uses contextual action states, never scam scores.
    """
    signal_types = {get_signal_type(s) for s in risk_signals}

    # User explicitly reports money sent or post-incident markers present
    user_sent_money = user_state.sent_money == "YES"
    has_post_incident_signals = bool(signal_types & {"WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT"})

    if user_sent_money or (has_post_incident_signals and overall_concern in ("HIGH_CONCERN", "ELEVATED_CONCERN", "MODERATE_CONCERN")):
        return ActionState.POST_INCIDENT_GUIDANCE, ResponseMode.POST_INCIDENT

    if overall_concern == "HIGH_CONCERN":
        return ActionState.HIGH_CAUTION, ResponseMode.POSSIBLE_ACTIVE_SCAM

    if overall_concern in ("ELEVATED_CONCERN", "MODERATE_CONCERN"):
        return ActionState.PAUSE_AND_VERIFY, ResponseMode.SUSPICIOUS_CONTENT

    if overall_concern in ("INSUFFICIENT_DATA", "INSUFFICIENT_EVIDENCE"):
        return ActionState.INSUFFICIENT_EVIDENCE, ResponseMode.INSUFFICIENT_EVIDENCE

    # LOW_CONCERN or unflagged
    return ActionState.SAFE_TO_CONTINUE_WITH_VERIFICATION, ResponseMode.PRE_TRANSACTION



def collect_recommended_actions(
    action_state: ActionState,
    risk_signals: List[Any],
    verification_results: List[Any],
    claims: List[Any],
    user_state: UserIncidentState,
) -> List[ActionRecommendation]:
    """
    Produces deterministic recommendations where every action has an explicit reason
    and traceable evidence / verification IDs.
    """
    actions: List[ActionRecommendation] = []
    seen_types = set()

    # Build index of signal_type -> (signal, evidence_ids)
    signal_map: Dict[str, Tuple[Any, List[str]]] = {}
    for s in risk_signals:
        stype = get_signal_type(s)
        ev_ids = getattr(s, "evidence_ids", []) or (s.get("evidence_ids", []) if isinstance(s, dict) else [])
        if stype:
            signal_map[stype] = (s, ev_ids)


    # Contradictory or unverified verification IDs
    unverified_vids = []
    unverified_ev_ids = []
    for v in verification_results:
        st = getattr(v, "status", "")
        st_val = getattr(st, "value", str(st)).upper()
        if st_val in ("UNVERIFIED", "CONTRADICTED", "CONTRADICTORY", "NOT_FOUND", "UNKNOWN", "UNAVAILABLE"):
            vid = getattr(v, "verification_id", None) or getattr(v, "id", None) or ""
            if vid:
                unverified_vids.append(vid)
            ev_id = getattr(v, "evidence_id", None) or getattr(v, "claim_id", None) or ""
            if ev_id:
                unverified_ev_ids.append(ev_id)


    # 1. PAUSE (Priority 1 in Caution / Pause states)
    if action_state in (ActionState.HIGH_CAUTION, ActionState.PAUSE_AND_VERIFY, ActionState.POST_INCIDENT_GUIDANCE):
        pause_evidence: List[str] = []
        pause_reasons: List[str] = []

        if "GUARANTEED_RETURN" in signal_map:
            pause_evidence.extend(signal_map["GUARANTEED_RETURN"][1])
            pause_reasons.append("guaranteed-return claim detected")
        if "DEPOSIT_PRESSURE" in signal_map:
            pause_evidence.extend(signal_map["DEPOSIT_PRESSURE"][1])
            pause_reasons.append("deposit-pressure indicators detected")
        if "URGENCY_INDUCEMENT" in signal_map:
            pause_evidence.extend(signal_map["URGENCY_INDUCEMENT"][1])
            pause_reasons.append("urgency inducement observed")

        reason_str = (
            f"Observed risk indicators: {', '.join(pause_reasons)}."
            if pause_reasons
            else "Elevated risk indicators observed across submitted content."
        )

        actions.append(
            ActionRecommendation(
                action=SafeActionType.PAUSE,
                title="Pause Before Transferring Any Funds",
                explanation="Do not send money, approve transfers, or commit funds until identity and regulatory authorizations are independently confirmed.",
                reason=reason_str,
                evidence_ids=list(dict.fromkeys(pause_evidence)),
                verification_ids=[],
                priority=1,
            )
        )
        seen_types.add(SafeActionType.PAUSE)

    # 2. DO NOT SEND ADDITIONAL MONEY (Critical when withdrawal fee or deposit pressure exists)
    if (
        "WITHDRAWAL_FEE" in signal_map
        or "ADDITIONAL_PAYMENT" in signal_map
        or "DEPOSIT_PRESSURE" in signal_map
        or action_state == ActionState.POST_INCIDENT_GUIDANCE
    ):
        add_ev: List[str] = []
        add_reasons: List[str] = []
        if "WITHDRAWAL_FEE" in signal_map:
            add_ev.extend(signal_map["WITHDRAWAL_FEE"][1])
            add_reasons.append("withdrawal fee demands")
        if "ADDITIONAL_PAYMENT" in signal_map:
            add_ev.extend(signal_map["ADDITIONAL_PAYMENT"][1])
            add_reasons.append("additional payment requests")
        if "DEPOSIT_PRESSURE" in signal_map:
            add_ev.extend(signal_map["DEPOSIT_PRESSURE"][1])
            add_reasons.append("repeated deposit demands")

        reason_text = (
            f"Identified payment friction patterns: {', '.join(add_reasons)}."
            if add_reasons
            else "Payment pressure or fee demand pattern identified."
        )

        actions.append(
            ActionRecommendation(
                action=SafeActionType.DO_NOT_SEND_ADDITIONAL_MONEY,
                title="Do Not Send Additional Funds to Unlock Balances",
                explanation="Legitimate financial platforms do not demand advance fees, taxes, or deposit top-ups to release user withdrawals.",
                reason=reason_text,
                evidence_ids=list(dict.fromkeys(add_ev)),
                verification_ids=[],
                priority=2,
            )
        )
        seen_types.add(SafeActionType.DO_NOT_SEND_ADDITIONAL_MONEY)

    # 3. VERIFY (Independent authoritative corroboration)
    if unverified_vids or claims or action_state in (ActionState.PAUSE_AND_VERIFY, ActionState.HIGH_CAUTION, ActionState.SAFE_TO_CONTINUE_WITH_VERIFICATION):
        reason_verify = (
            "Claimed regulatory or identity registrations could not be independently corroborated."
            if unverified_vids
            else "Entities and registration numbers must be verified against official regulatory registries."
        )
        actions.append(
            ActionRecommendation(
                action=SafeActionType.VERIFY,
                title="Verify Authorizations on Authoritative Portals",
                explanation="Check entity registration numbers directly on official portals (e.g. SEBI, RBI, MCA) rather than trusting credentials printed on messages or sites.",
                reason=reason_verify,
                evidence_ids=list(dict.fromkeys(unverified_ev_ids)),
                verification_ids=unverified_vids,
                priority=3,
            )
        )
        seen_types.add(SafeActionType.VERIFY)

    # 4. DO NOT SHARE CREDENTIALS
    if (
        user_state.shared_credentials in ("YES", "NOT_SURE")
        or action_state in (ActionState.HIGH_CAUTION, ActionState.POST_INCIDENT_GUIDANCE, ActionState.PAUSE_AND_VERIFY)
    ):
        cred_reasons = []
        cred_ev: List[str] = []
        if user_state.shared_credentials == "YES":
            cred_reasons.append("user indicated credentials may have been shared")
        if "IMPERSONATION_RISK" in signal_map:
            cred_ev.extend(signal_map["IMPERSONATION_RISK"][1])
            cred_reasons.append("impersonation risk detected")
        if "OFF_PLATFORM_REDIRECT" in signal_map:
            cred_ev.extend(signal_map["OFF_PLATFORM_REDIRECT"][1])
            cred_reasons.append("off-platform channel redirection detected")

        reason_text = (
            f"Security precautions indicated: {', '.join(cred_reasons)}."
            if cred_reasons
            else "Protective measure to prevent account takeover."
        )

        actions.append(
            ActionRecommendation(
                action=SafeActionType.DO_NOT_SHARE_CREDENTIALS,
                title="Never Share Passwords, OTPs, PINs, or CVV",
                explanation="No genuine bank, regulatory authority, or payment provider will ever ask for your OTP, ATM PIN, UPI PIN, or password.",
                reason=reason_text,
                evidence_ids=list(dict.fromkeys(cred_ev)),
                verification_ids=[],
                priority=4,
            )
        )
        seen_types.add(SafeActionType.DO_NOT_SHARE_CREDENTIALS)

    # 5. PRESERVE EVIDENCE
    if action_state != ActionState.SAFE_TO_CONTINUE_WITH_VERIFICATION or risk_signals:
        all_ev_ids = [getattr(s, "evidence_ids", []) for s in risk_signals]
        flattened_ev = [item for sublist in all_ev_ids for item in sublist][:5]
        actions.append(
            ActionRecommendation(
                action=SafeActionType.PRESERVE_EVIDENCE,
                title="Preserve Communication Records and Transaction References",
                explanation="Save unedited screenshots, URLs, payment handles, sender numbers, and bank transaction reference numbers (UTR/RRN).",
                reason="Documenting transaction artifacts enables rapid escalation to banks and reporting bodies.",
                evidence_ids=flattened_ev,
                verification_ids=[],
                priority=5,
            )
        )
        seen_types.add(SafeActionType.PRESERVE_EVIDENCE)

    # 6. CONTACT BANK OR PAYMENT PROVIDER (If post-incident or money sent)
    if action_state == ActionState.POST_INCIDENT_GUIDANCE or user_state.sent_money in ("YES", "NOT_SURE"):
        actions.append(
            ActionRecommendation(
                action=SafeActionType.CONTACT_BANK_OR_PAYMENT_PROVIDER,
                title="Contact Your Financial Provider Immediately",
                explanation="If money was transferred, immediately reach your bank or payment app's official support to request a transaction dispute or freeze.",
                reason="Early reporting within the golden hour significantly improves chances of recalling unauthorized transfers.",
                evidence_ids=[],
                verification_ids=[],
                priority=6,
            )
        )
        seen_types.add(SafeActionType.CONTACT_BANK_OR_PAYMENT_PROVIDER)

    # 7. REPORT (Post-incident or high caution)
    if action_state in (ActionState.POST_INCIDENT_GUIDANCE, ActionState.HIGH_CAUTION):
        actions.append(
            ActionRecommendation(
                action=SafeActionType.REPORT,
                title="Report Through Official Jurisdictional Channels",
                explanation="Lodge a complaint on official law enforcement or consumer portals (e.g. National Cyber Crime Reporting Portal cybercrime.gov.in / 1930).",
                reason="Official reporting creates a formal record and aids inter-bank freeze mechanisms.",
                evidence_ids=[],
                verification_ids=[],
                priority=7,
            )
        )
        seen_types.add(SafeActionType.REPORT)

    # 8. DO NOT INSTALL UNKNOWN APP (If off-platform or apk signals)
    if "OFF_PLATFORM_REDIRECT" in signal_map:
        actions.append(
            ActionRecommendation(
                action=SafeActionType.DO_NOT_INSTALL_UNKNOWN_APP,
                title="Do Not Install Unknown APKs or Remote Desktop Apps",
                explanation="Do not download APKs, screen-sharing tools (AnyDesk, TeamViewer, RustDesk), or unverified apps sent over messaging platforms.",
                reason="Off-platform communications frequently attempt remote device access or sideloading malicious packages.",
                evidence_ids=signal_map["OFF_PLATFORM_REDIRECT"][1],
                verification_ids=[],
                priority=8,
            )
        )
        seen_types.add(SafeActionType.DO_NOT_INSTALL_UNKNOWN_APP)

    # Fallback for safe / informational
    if not actions:
        actions.append(
            ActionRecommendation(
                action=SafeActionType.MONITOR,
                title="Maintain Ongoing Caution and Verify Links",
                explanation="Review terms and conditions, confirm identity on official registries, and monitor account activity routinely.",
                reason="No active high-risk indicators were detected in the provided submission.",
                evidence_ids=[],
                verification_ids=[],
                priority=10,
            )
        )

    # Sort actions by priority
    actions.sort(key=lambda a: a.priority)
    return actions


def build_recovery_guidance(
    is_activated: bool,
    activation_reason: str,
) -> RecoveryGuidance:
    """
    Builds structured, conditional recovery guidance.
    Uses non-judgmental language: 'If you have already sent money...'
    """
    steps = [
        RecoveryStep(
            category="STOP_PAYMENTS",
            title="1. Stop Any Further Money Transfers",
            instructions=[
                "Do not send additional money to 'unlock', 'recover', 'verify', 'release', or pay alleged 'taxes' on your balance.",
                "Legitimate financial institutions and regulators do not require upfront deposits to disburse or withdraw your funds.",
                "Cease all communication with unverified contact numbers, handles, or groups demanding payments.",
            ],
            disclaimer="Refusing additional payment demands prevents escalating secondary losses.",
        ),
        RecoveryStep(
            category="PRESERVE_EVIDENCE",
            title="2. Preserve All Documentation and Transaction References",
            instructions=[
                "Save original screenshots of chats, payment receipts, deposit screens, and error messages.",
                "Record transaction reference IDs (UTR numbers, RRN, UPI transaction IDs, and bank account numbers).",
                "Note down phone numbers, group invite links, usernames, and submitted URLs.",
                "Do NOT save or share passwords, OTPs, ATM PINs, or CVV codes.",
            ],
            disclaimer="Accurate reference numbers and timestamps are essential for banking recalls and police complaints.",
        ),
        RecoveryStep(
            category="CONTACT_PROVIDER",
            title="3. Contact Your Bank or Payment App Through Official Channels",
            instructions=[
                "Notify your bank or payment app support immediately using verified numbers from your physical card or official app.",
                "Request a transaction dispute or payment recall on fraudulent or unauthorized debit entries.",
                "If net banking credentials or debit cards were exposed, request an immediate card block or account freeze.",
            ],
            disclaimer="Speed is critical: contacting your financial provider immediately maximizes recovery chances.",
        ),
        RecoveryStep(
            category="OFFICIAL_REPORTING",
            title="4. File an Official Incident Report",
            instructions=[
                "Report the incident through your jurisdiction's official reporting authority.",
                "In India, file a complaint on the National Cyber Crime Reporting Portal at cybercrime.gov.in or call 1930.",
                "Attach preserved transaction IDs, payment handles, and message screenshots to your complaint.",
            ],
            disclaimer="Always use authoritative government and law enforcement portals directly.",
        ),
        RecoveryStep(
            category="ACCOUNT_SECURITY",
            title="5. Secure Compromised Accounts and Devices",
            instructions=[
                "Change internet banking passwords, email passwords, and UPI PINs from an independent, secure device.",
                "If any application or APK was installed at the request of the contact, uninstall it immediately.",
                "Enable multi-factor authentication (2FA) on your primary email and banking accounts.",
            ],
            disclaimer="Do not enter credentials into any third-party links or test forms.",
        ),
    ]

    return RecoveryGuidance(
        is_activated=is_activated,
        activation_reason=activation_reason,
        steps=steps,
        general_reporting_guidance=(
            "If money or sensitive credentials may have been transferred, immediately use your financial provider's "
            "official support channels and file a report with official authorities (e.g. cybercrime.gov.in / 1930 in India)."
        ),
        account_security_steps=[
            "Change online banking and email passwords immediately from a secure device.",
            "Verify that no unauthorized remote-access applications or screen-sharing tools are installed.",
            "Review recent account statements for unauthorized mandates or recurring payments.",
        ],
        disclaimer=(
            "RakshaScan provides safety and verification guidance. It does not provide legal representation, "
            "financial guarantees, or emergency dispatch services."
        ),
    )


def build_incident_timeline(
    claims: List[Any],
    risk_signals: List[Any],
    evidence: List[Any],
    user_state: UserIncidentState,
    fetch_success: bool = True,
) -> Tuple[List[IncidentTimelineEvent], str]:
    """
    Constructs a lightweight incident timeline based ONLY on observed facts and explicit user declarations.
    Never infers PAYMENT_MADE merely because DEPOSIT_PRESSURE exists.
    """
    events: List[IncidentTimelineEvent] = []

    # 1. Submission / Observation
    if fetch_success:
        events.append(
            IncidentTimelineEvent(
                event_type=IncidentEventType.WEBSITE_VISITED,
                title="Target Content or Website Analyzed",
                description="RakshaScan safely inspected and parsed content from the submitted source.",
                source="OBSERVED_EVIDENCE",
                evidence_ids=[getattr(e, "evidence_id", "") for e in evidence[:2] if getattr(e, "evidence_id", "")],
            )
        )

    # 2. Claims Received
    if claims:
        claim_ev = [getattr(c, "evidence_id", "") for c in claims if getattr(c, "evidence_id", "")]
        events.append(
            IncidentTimelineEvent(
                event_type=IncidentEventType.CLAIM_RECEIVED,
                title="Specific Financial Claims or Returns Presented",
                description=f"Observed {len(claims)} explicit claim(s) regarding returns, registrations, or investment terms.",
                source="OBSERVED_EVIDENCE",
                evidence_ids=claim_ev[:3],
            )
        )

    # 3. Off-platform or communication initiation
    off_plat = [s for s in risk_signals if get_signal_type(s) == "OFF_PLATFORM_REDIRECT"]
    if off_plat:
        events.append(
            IncidentTimelineEvent(
                event_type=IncidentEventType.COMMUNICATION_STARTED,
                title="Off-Platform Communication Channel Indicated",
                description="Content directs communication toward private messaging channels (e.g. WhatsApp or Telegram).",
                source="OBSERVED_EVIDENCE",
                evidence_ids=getattr(off_plat[0], "evidence_ids", []),
            )
        )

    # 4. Payment or Deposit Requested
    dep_signals = [
        s for s in risk_signals
        if get_signal_type(s) in ("DEPOSIT_PRESSURE", "WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT")
    ]
    if dep_signals:
        sig = dep_signals[0]
        stype = get_signal_type(sig)
        ev_type = (
            IncidentEventType.ADDITIONAL_PAYMENT_REQUESTED
            if stype in ("WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT")

            else IncidentEventType.PAYMENT_REQUESTED
        )
        title_text = (
            "Additional Fee / Withdrawal Charge Demanded"
            if stype in ("WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT")
            else "Initial Deposit or Investment Demanded"
        )
        events.append(
            IncidentTimelineEvent(
                event_type=ev_type,
                title=title_text,
                description=getattr(sig, "description", "Payment demand detected in observed content."),
                source="OBSERVED_EVIDENCE",
                evidence_ids=getattr(sig, "evidence_ids", []),
            )
        )

    # 5. User-Declared Payment (ONLY IF EXPLICITLY STATED)
    if user_state.sent_money == "YES":
        events.append(
            IncidentTimelineEvent(
                event_type=IncidentEventType.PAYMENT_MADE,
                title="User Reported Payment Transferred",
                description="User explicitly indicated that funds were transferred to the counterparty.",
                source="USER_DECLARED",
                evidence_ids=[],
            )
        )
    elif user_state.sent_money == "NOT_SURE":
        events.append(
            IncidentTimelineEvent(
                event_type=IncidentEventType.USER_REPORTED,
                title="Uncertain Payment State Reported",
                description="User indicated uncertainty regarding whether funds or debits occurred.",
                source="USER_DECLARED",
                evidence_ids=[],
            )
        )

    # 6. User-Declared Credentials Shared
    if user_state.shared_credentials == "YES":
        events.append(
            IncidentTimelineEvent(
                event_type=IncidentEventType.USER_REPORTED,
                title="User Reported Sensitive Credentials Shared",
                description="User declared that account credentials, PIN, or confidential details may have been shared.",
                source="USER_DECLARED",
                evidence_ids=[],
            )
        )

    summary_text = (
        f"Timeline reconstructed with {len(events)} verified event(s). "
        "Only directly observed content and user-declared statements are included."
    )

    return events, summary_text
