from typing import List, Optional, Any
from app.response.models import (
    SafeResponse,
    RecoveryGuidance,
    UserIncidentState,
    IncidentTimeline,
    SafeActionType,
    ActionState,
    ResponseMode,
)
from app.response.rules import (
    evaluate_action_state_and_mode,
    collect_recommended_actions,
    build_recovery_guidance,
    build_incident_timeline,
    get_signal_type,
)



class SafeResponseEngine:
    """
    Deterministic interpretation and action layer answering:
    'What should the user safely do next?'
    Based on evidence, risk signals, verification states, and user incident inputs.
    """

    DEFAULT_DISCLAIMER = (
        "RakshaScan provides safety and verification guidance. It does not provide investment advice, "
        "guarantee outcomes, or determine legal liability."
    )

    def generate_response(
        self,
        overall_concern: str,
        risk_signals: List[Any],
        verification_results: List[Any],
        claims: List[Any],
        evidence: List[Any],
        user_state: Optional[UserIncidentState] = None,
        fetch_success: bool = True,
    ) -> SafeResponse:
        user_state = user_state or UserIncidentState()

        if hasattr(overall_concern, "value"):
            concern_str = overall_concern.value
        elif hasattr(overall_concern, "overall_level"):
            level = getattr(overall_concern, "overall_level")
            concern_str = getattr(level, "value", str(level))
        else:
            concern_str = str(overall_concern)

        # 1. Action State and Response Mode
        action_state, response_mode = evaluate_action_state_and_mode(
            overall_concern=concern_str,

            risk_signals=risk_signals,
            verification_results=verification_results,
            user_state=user_state,
        )

        # 2. Recommended Actions (Traceable to evidence & verification IDs)
        recommended_actions = collect_recommended_actions(
            action_state=action_state,
            risk_signals=risk_signals,
            verification_results=verification_results,
            claims=claims,
            user_state=user_state,
        )

        primary_action = (
            recommended_actions[0].action if recommended_actions else SafeActionType.PAUSE
        )

        # 3. Guidance Notes
        guidance_notes = []
        if action_state == ActionState.POST_INCIDENT_GUIDANCE:
            guidance_notes.append("Post-incident recovery protocols are recommended based on detected friction or reported transactions.")
        elif action_state == ActionState.HIGH_CAUTION:
            guidance_notes.append("Elevated risk signals detected. Halt all transactions until independent verification is performed.")
        elif action_state == ActionState.PAUSE_AND_VERIFY:
            guidance_notes.append("Moderate risk or unverified claims detected. Pause and verify regulatory authorizations.")
        else:
            guidance_notes.append("No immediate active scam indicators observed, but always independently verify financial counterparties.")

        # 4. Incident Timeline
        timeline_events, timeline_summary = build_incident_timeline(
            claims=claims,
            risk_signals=risk_signals,
            evidence=evidence,
            user_state=user_state,
            fetch_success=fetch_success,
        )
        incident_timeline = IncidentTimeline(
            events=timeline_events,
            summary=timeline_summary,
        )

        # 5. Recovery Guidance
        is_recovery_active = (
            action_state == ActionState.POST_INCIDENT_GUIDANCE
            or user_state.sent_money in ("YES", "NOT_SURE")
            or user_state.shared_credentials == "YES"
            or any(get_signal_type(s) in ("WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT") for s in risk_signals)
        )

        activation_reason = (
            "User reported payment or credential exposure"
            if user_state.sent_money == "YES" or user_state.shared_credentials == "YES"
            else "Withdrawal fee, fee demand, or elevated post-incident patterns detected in content"
            if any(get_signal_type(s) in ("WITHDRAWAL_FEE", "ADDITIONAL_PAYMENT") for s in risk_signals)
            else "Precautionary recovery protocol available if transactions occurred"
        )


        recovery = build_recovery_guidance(
            is_activated=is_recovery_active,
            activation_reason=activation_reason,
        )

        return SafeResponse(
            response_mode=response_mode,
            action_state=action_state,
            primary_action=primary_action,
            recommended_actions=recommended_actions,
            guidance_notes=guidance_notes,
            incident_timeline=incident_timeline,
            recovery_guidance=recovery,
            disclaimer=self.DEFAULT_DISCLAIMER,
        )
