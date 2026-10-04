"""Unit and integration tests for Phase 9: Safe Response & Recovery."""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.response.engine import SafeResponseEngine
from app.response.models import (
    ResponseMode,
    ActionState,
    SafeActionType,
    UserIncidentState,
    IncidentEventType,
)
from app.evidence.models import EvidenceRecord
from app.risk.models import RiskSignal, RiskCategory, RiskSeverity
from app.verification.models import VerificationResult, VerificationStatus




@pytest.fixture
def engine():
    return SafeResponseEngine()


def make_signal(signal_name: str, evidence_ids=None):
    category = RiskCategory.FINANCIAL
    if "deposit" in signal_name.lower():
        category = RiskCategory.MANIPULATION
    return RiskSignal(
        signal_id=f"sig-{signal_name.lower().replace('_', '-')}-01",
        category=category,
        severity=RiskSeverity.HIGH,
        confidence=RiskSeverity.HIGH,
        title=f"Test {signal_name}",
        description=f"Description for {signal_name}",
        evidence_ids=evidence_ids or ["ev-123"],
        claim_ids=["cl-1"],
        verification_ids=[],
        source="unit_test",
        explanation="Detected in test",
    )


def make_evidence(ev_id="ev-123"):
    return EvidenceRecord(
        evidence_id=ev_id,
        source_type="PAGE_TEXT",
        source_url="https://example.com",
        extracted_text="Test claim value",
        context="Snippet for test",
        extraction_method="FINANCIAL_PATTERN",
    )



def test_low_concern_informational_guidance(engine):
    """Low concern without signals leads to safe to continue with verification."""
    resp = engine.generate_response(
        overall_concern="LOW_CONCERN",
        risk_signals=[],
        verification_results=[],
        claims=[],
        evidence=[],
    )
    assert resp.action_state == ActionState.SAFE_TO_CONTINUE_WITH_VERIFICATION
    assert resp.response_mode == ResponseMode.PRE_TRANSACTION
    assert any(a.action in (SafeActionType.VERIFY, SafeActionType.MONITOR) for a in resp.recommended_actions)
    assert resp.recovery_guidance.is_activated is False


def test_moderate_concern_pause_and_verify(engine):
    """Moderate concern leads to PAUSE_AND_VERIFY action state."""
    sig = make_signal("GUARANTEED_RETURN", ["ev-gr-1"])
    ev = make_evidence("ev-gr-1")

    resp = engine.generate_response(
        overall_concern="MODERATE_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[ev],
    )
    assert resp.action_state == ActionState.PAUSE_AND_VERIFY
    assert resp.response_mode == ResponseMode.SUSPICIOUS_CONTENT
    assert any(a.action == SafeActionType.PAUSE for a in resp.recommended_actions)
    assert any(a.action == SafeActionType.VERIFY for a in resp.recommended_actions)


def test_high_concern_stronger_safety_actions(engine):
    """High concern triggers high caution and stronger defensive actions."""
    sig1 = make_signal("GUARANTEED_RETURN", ["ev-1"])
    sig2 = make_signal("DEPOSIT_PRESSURE", ["ev-2"])

    resp = engine.generate_response(
        overall_concern="HIGH_CONCERN",
        risk_signals=[sig1, sig2],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-1"), make_evidence("ev-2")],
    )
    assert resp.action_state == ActionState.HIGH_CAUTION
    assert resp.response_mode == ResponseMode.POSSIBLE_ACTIVE_SCAM
    actions = [a.action for a in resp.recommended_actions]
    assert SafeActionType.PAUSE in actions
    assert SafeActionType.DO_NOT_SEND_ADDITIONAL_MONEY in actions
    assert SafeActionType.PRESERVE_EVIDENCE in actions


def test_guaranteed_return_triggers_pause(engine):
    """Guaranteed return claim explicitly triggers Pause with documented reason."""
    sig = make_signal("GUARANTEED_RETURN", ["ev-gr-99"])

    resp = engine.generate_response(
        overall_concern="MODERATE_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-gr-99")],
    )
    pause_action = next(a for a in resp.recommended_actions if a.action == SafeActionType.PAUSE)
    assert "guaranteed-return" in pause_action.reason.lower()
    assert "ev-gr-99" in pause_action.evidence_ids


def test_deposit_pressure_triggers_do_not_send_money(engine):
    """Deposit pressure triggers DO_NOT_SEND_ADDITIONAL_MONEY recommendation."""
    sig = make_signal("DEPOSIT_PRESSURE", ["ev-dp-1"])

    resp = engine.generate_response(
        overall_concern="MODERATE_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-dp-1")],
    )
    action = next(a for a in resp.recommended_actions if a.action == SafeActionType.DO_NOT_SEND_ADDITIONAL_MONEY)
    assert "deposit demands" in action.reason.lower()
    assert "ev-dp-1" in action.evidence_ids


def test_withdrawal_fee_triggers_post_incident_guidance(engine):
    """Withdrawal fee shifts action state to POST_INCIDENT_GUIDANCE and activates recovery."""
    sig = make_signal("WITHDRAWAL_FEE", ["ev-wf-1"])

    resp = engine.generate_response(
        overall_concern="HIGH_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-wf-1")],
    )
    assert resp.action_state == ActionState.POST_INCIDENT_GUIDANCE
    assert resp.response_mode == ResponseMode.POST_INCIDENT
    assert resp.recovery_guidance is not None
    assert resp.recovery_guidance.is_activated is True
    assert len(resp.recovery_guidance.steps) >= 5


def test_additional_payment_triggers_post_incident_guidance(engine):
    """Additional payment request signal activates recovery guidance."""
    sig = make_signal("ADDITIONAL_PAYMENT", ["ev-ap-1"])

    resp = engine.generate_response(
        overall_concern="HIGH_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-ap-1")],
    )
    assert resp.action_state == ActionState.POST_INCIDENT_GUIDANCE
    assert resp.recovery_guidance.is_activated is True


def test_evidence_traceability_and_no_unsupported_reasons(engine):
    """Every recommended action has an explanatory reason and traceable evidence or verification IDs."""
    sig = make_signal("GUARANTEED_RETURN", ["ev-trace-1"])
    ver = VerificationResult(
        id="vr-test-1",
        claim_id="ev-trace-2",
        status=VerificationStatus.CONTRADICTORY,
        source_name="SEBI Portal",

        verification_method="REGISTRY_QUERY",
        evidence="Registration number belongs to an unrelated firm.",
        reason="Contradictory records in registry.",
    )


    resp = engine.generate_response(
        overall_concern="HIGH_CONCERN",
        risk_signals=[sig],
        verification_results=[ver],
        claims=[],
        evidence=[make_evidence("ev-trace-1"), make_evidence("ev-trace-2")],
    )

    for action in resp.recommended_actions:
        assert action.reason and len(action.reason.strip()) > 5
        assert action.title and len(action.title.strip()) > 5
        assert action.explanation and len(action.explanation.strip()) > 10

    verify_action = next(a for a in resp.recommended_actions if a.action == SafeActionType.VERIFY)
    assert "vr-test-1" in verify_action.verification_ids
    assert "ev-trace-2" in verify_action.evidence_ids


def test_no_automatic_assumption_of_payment(engine):
    """Having deposit pressure or guaranteed return MUST NOT infer payment was made."""
    sig = make_signal("DEPOSIT_PRESSURE", ["ev-dp-10"])


    resp = engine.generate_response(
        overall_concern="HIGH_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-dp-10")],
        user_state=UserIncidentState(sent_money="NO"),
    )
    # Timeline should NOT have PAYMENT_MADE
    event_types = [e.event_type for e in resp.incident_timeline.events]
    assert IncidentEventType.PAYMENT_MADE not in event_types
    assert IncidentEventType.PAYMENT_REQUESTED in event_types


def test_user_declared_payment_activates_recovery(engine):
    """When user explicitly declares payment occurred, recovery guidance is activated."""
    resp = engine.generate_response(
        overall_concern="LOW_CONCERN",
        risk_signals=[],
        verification_results=[],
        claims=[],
        evidence=[],
        user_state=UserIncidentState(sent_money="YES"),
    )
    assert resp.action_state == ActionState.POST_INCIDENT_GUIDANCE
    assert resp.response_mode == ResponseMode.POST_INCIDENT
    assert resp.recovery_guidance.is_activated is True
    # Timeline includes PAYMENT_MADE from user declaration
    event_types = [e.event_type for e in resp.incident_timeline.events]
    assert IncidentEventType.PAYMENT_MADE in event_types


def test_user_declared_no_payment_retains_pre_transaction(engine):
    """When user says no payment occurred, system remains in pre-transaction mode."""
    sig = make_signal("GUARANTEED_RETURN", ["ev-1"])
    resp = engine.generate_response(

        overall_concern="MODERATE_CONCERN",
        risk_signals=[sig],
        verification_results=[],
        claims=[],
        evidence=[make_evidence("ev-1")],
        user_state=UserIncidentState(sent_money="NO"),
    )
    assert resp.response_mode == ResponseMode.SUSPICIOUS_CONTENT
    assert resp.action_state == ActionState.PAUSE_AND_VERIFY
    event_types = [e.event_type for e in resp.incident_timeline.events]
    assert IncidentEventType.PAYMENT_MADE not in event_types


def test_user_not_sure_provides_cautious_guidance(engine):
    """When user is not sure about payments, cautious guidance and recovery options are made available."""
    resp = engine.generate_response(
        overall_concern="MODERATE_CONCERN",
        risk_signals=[],
        verification_results=[],
        claims=[],
        evidence=[],
        user_state=UserIncidentState(sent_money="NOT_SURE"),
    )
    assert resp.recovery_guidance.is_activated is True
    actions = [a.action for a in resp.recommended_actions]
    assert SafeActionType.CONTACT_BANK_OR_PAYMENT_PROVIDER in actions
    event_types = [e.event_type for e in resp.incident_timeline.events]
    assert IncidentEventType.USER_REPORTED in event_types
    assert IncidentEventType.PAYMENT_MADE not in event_types


def test_incident_timeline_does_not_invent_events(engine):
    """Incident timeline strictly uses observed evidence and explicit declarations."""
    resp = engine.generate_response(
        overall_concern="LOW_CONCERN",
        risk_signals=[],
        verification_results=[],
        claims=[],
        evidence=[],
        fetch_success=True,
    )
    assert len(resp.incident_timeline.events) == 1
    assert resp.incident_timeline.events[0].event_type == IncidentEventType.WEBSITE_VISITED


@pytest.mark.anyio
async def test_api_returns_safe_response():
    """Verify API analysis endpoints return safe_response and recovery_guidance structures."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post(
            "/api/v1/analyze/message",
            json={"text": "Guaranteed 50% monthly profit. Deposit 5000 now. Withdrawal fee applies."},
        )
        assert res.status_code == 200
        data = res.json()
        assert "safe_response" in data
        assert data["safe_response"] is not None
        assert "action_state" in data["safe_response"]
        assert "recommended_actions" in data["safe_response"]
        assert len(data["safe_response"]["recommended_actions"]) > 0
        assert "incident_timeline" in data["safe_response"]
        assert "recovery_guidance" in data
        assert data["recovery_guidance"]["is_activated"] is True
