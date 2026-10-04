"""Tests for RakshaScan Phase 7 Scam Journey Reconstruction.

Covers:
10. financial claim stage
11. deposit request stage
12. withdrawal issue stage
13. unknown stage
14. observed vs suspected distinction
15. journey confidence calculation
16. evidence traceability
17. mandatory disclaimer presence and phrasing
18. no fabricated stages
"""

import pytest
from app.journey.builder import ScamJourneyBuilder
from app.journey.models import (
    MANDATORY_JOURNEY_DISCLAIMER,
    JourneyConfidence,
    ScamJourney,
    ScamJourneyStage,
    StageStatus,
    StageType,
)
from app.risk.models import RiskCategory, RiskSeverity, RiskSignal


def test_scam_journey_financial_claim_stage():
    """10. Test that financial claim stage is OBSERVED when guaranteed return claim exists."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[
            RiskSignal(
                signal_id="sig-fin-guaranteed-123",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Guaranteed-return promise detected",
                description="Promotes assured return",
                evidence_ids=["ev-fin-1"],
                source="page_analysis",
                explanation="Guaranteed returns represent high risk.",
            )
        ],
        claims=[],
        financial_claims=[
            {
                "id": "fc-1",
                "claim_type": "GUARANTEED_RETURN",
                "claim_text": "Guaranteed 35% monthly return",
                "evidence_id": "ev-fin-1",
            }
        ],
        evidence=[{"id": "ev-page-1"}],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    stage = next(s for s in journey.stages if s.stage_type == StageType.FINANCIAL_CLAIM.value)
    assert stage.status == StageStatus.OBSERVED.value
    assert "ev-fin-1" in stage.evidence_ids
    assert "sig-fin-guaranteed-123" in stage.signal_ids
    assert stage.confidence == JourneyConfidence.HIGH.value


def test_scam_journey_deposit_request_stage():
    """11. Test that deposit request stage is OBSERVED when deposit pressure is detected."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[
            RiskSignal(
                signal_id="sig-manip-deposit-456",
                category=RiskCategory.MANIPULATION,
                severity=RiskSeverity.HIGH,
                title="Immediate deposit pressure detected",
                description="Mandates immediate deposit to priority desk",
                evidence_ids=["ev-dep-1"],
                source="page_analysis",
                explanation="Deposit pressure limits due diligence.",
            )
        ],
        claims=[],
        financial_claims=[
            {
                "id": "fc-dep-1",
                "claim_type": "DEPOSIT_PRESSURE",
                "claim_text": "Deposit immediately to lock quota",
                "evidence_id": "ev-dep-1",
            }
        ],
        evidence=[{"id": "ev-page-1"}],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    stage = next(s for s in journey.stages if s.stage_type == StageType.DEPOSIT_REQUEST.value)
    assert stage.status == StageStatus.OBSERVED.value
    assert "ev-dep-1" in stage.evidence_ids
    assert "sig-manip-deposit-456" in stage.signal_ids


def test_scam_journey_withdrawal_issue_stage():
    """12. Test that withdrawal issue stage is OBSERVED when advance clearance fee is detected."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[
            RiskSignal(
                signal_id="sig-fin-withdraw-789",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Upfront withdrawal fee or clearance payment demand detected",
                description="Tax clearance fee required",
                evidence_ids=["ev-with-1"],
                source="page_analysis",
                explanation="Upfront fee required to release balance.",
            )
        ],
        claims=[],
        financial_claims=[
            {
                "id": "fc-with-1",
                "claim_type": "WITHDRAWAL_FEE",
                "claim_text": "Tax clearance fee prior to withdrawal release",
                "evidence_id": "ev-with-1",
            }
        ],
        evidence=[{"id": "ev-page-1"}],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    stage = next(s for s in journey.stages if s.stage_type == StageType.WITHDRAWAL_ISSUE.value)
    assert stage.status == StageStatus.OBSERVED.value
    assert "ev-with-1" in stage.evidence_ids
    assert "sig-fin-withdraw-789" in stage.signal_ids


def test_scam_journey_unknown_stage():
    """13. Test that unobserved stage (e.g. initial contact without urgency) is UNKNOWN."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[],
        claims=[],
        financial_claims=[],
        evidence=[{"id": "ev-1"}],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    s1 = next(s for s in journey.stages if s.stage_type == StageType.INITIAL_CONTACT.value)
    assert s1.status == StageStatus.UNKNOWN.value
    assert "unobserved" in s1.description.lower() or "no direct evidence" in s1.why_present.lower()


def test_scam_journey_observed_vs_suspected_distinction():
    """14. Test distinction between OBSERVED (explicit text) and SUSPECTED (inferred from urgency)."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[
            RiskSignal(
                signal_id="sig-manip-urgency-001",
                category=RiskCategory.MANIPULATION,
                severity=RiskSeverity.MEDIUM,
                title="High-pressure urgency language detected",
                description="Urgency cues 'act now'",
                evidence_ids=["ev-urg-1"],
                source="page_analysis",
                explanation="Urgency cues induce impulsive actions.",
            )
        ],
        claims=[],
        financial_claims=[
            {
                "id": "fc-urg-1",
                "claim_type": "URGENCY",
                "claim_text": "Act now - limited time allocation",
                "evidence_id": "ev-urg-1",
            }
        ],
        evidence=[{"id": "ev-1"}],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    s1 = next(s for s in journey.stages if s.stage_type == StageType.INITIAL_CONTACT.value)
    # Urgency on page indicates SUSPECTED outbound initial contact push, not direct cold-call log
    assert s1.status == StageStatus.SUSPECTED.value
    assert s1.status != StageStatus.OBSERVED.value


def test_scam_journey_confidence_levels():
    """15. Test journey confidence calculation (LOW, MEDIUM, HIGH based on stage completeness)."""
    builder = ScamJourneyBuilder()

    # Case A: Low evidence (0-1 stages)
    j_low = builder.build_journey(
        risk_signals=[],
        claims=[],
        financial_claims=[],
        evidence=[],
        links=[],
        contact_signals={},
        fetch_success=False,
    )
    assert j_low.confidence == JourneyConfidence.LOW.value

    # Case B: High evidence (>= 4 stages: Website, Financial Claim, Deposit Request, Communication)
    j_high = builder.build_journey(
        risk_signals=[
            RiskSignal(
                signal_id="sig-fin-guaranteed-1",
                category=RiskCategory.FINANCIAL,
                severity=RiskSeverity.HIGH,
                title="Guaranteed return",
                description="",
                source="page_analysis",
                explanation="",
            ),
            RiskSignal(
                signal_id="sig-manip-deposit-1",
                category=RiskCategory.MANIPULATION,
                severity=RiskSeverity.HIGH,
                title="Immediate deposit pressure",
                description="",
                source="page_analysis",
                explanation="",
            ),
        ],
        claims=[],
        financial_claims=[
            {"id": "f1", "claim_type": "GUARANTEED_RETURN", "claim_text": "35% return", "evidence_id": "ev1"},
            {"id": "f2", "claim_type": "DEPOSIT_PRESSURE", "claim_text": "Deposit now", "evidence_id": "ev2"},
        ],
        evidence=[{"id": "ev-web-1"}],
        links=[],
        contact_signals={"phone_numbers": ["+91 98765 43210"], "emails": []},
        fetch_success=True,
    )
    assert j_high.confidence == JourneyConfidence.HIGH.value
    assert "stages supported" in j_high.summary_text


def test_scam_journey_evidence_traceability():
    """16. Test that journey stages link to evidence records."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[],
        claims=[],
        financial_claims=[
            {
                "id": "fc-1",
                "claim_type": "GUARANTEED_RETURN",
                "claim_text": "Guaranteed profit",
                "evidence_id": "ev-trace-999",
            }
        ],
        evidence=[{"id": "ev-web-base"}],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    stage_fc = next(s for s in journey.stages if s.stage_type == StageType.FINANCIAL_CLAIM.value)
    assert "ev-trace-999" in stage_fc.evidence_ids
    assert "ev-trace-999" in journey.evidence_ids


def test_scam_journey_mandatory_disclaimer():
    """17. Test that mandatory legal disclaimer is present verbatim."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[],
        claims=[],
        financial_claims=[],
        evidence=[],
        links=[],
        contact_signals={},
        fetch_success=True,
    )

    expected_disclaimer = "This represents a reconstructed pattern, not a determination that a specific case is fraudulent."
    assert journey.disclaimer == expected_disclaimer
    assert journey.pattern_title == "Possible scam journey pattern"
    # Ensure prejudicial wording is NOT used
    assert "confirmed scam" not in journey.pattern_title.lower()
    assert "proven scam" not in journey.pattern_title.lower()


def test_scam_journey_no_fabricated_stages():
    """18. Test that stages with zero evidence are NOT_OBSERVED or UNKNOWN, never marked OBSERVED."""
    builder = ScamJourneyBuilder()
    journey = builder.build_journey(
        risk_signals=[],
        claims=[],
        financial_claims=[],  # No deposit, no withdrawal, no financial claim
        evidence=[{"id": "ev-web-1"}],
        links=[],
        contact_signals={"phone_numbers": [], "emails": []},
        fetch_success=True,
    )

    dep_stage = next(s for s in journey.stages if s.stage_type == StageType.DEPOSIT_REQUEST.value)
    with_stage = next(s for s in journey.stages if s.stage_type == StageType.WITHDRAWAL_ISSUE.value)
    fin_stage = next(s for s in journey.stages if s.stage_type == StageType.FINANCIAL_CLAIM.value)

    assert dep_stage.status == StageStatus.NOT_OBSERVED.value
    assert with_stage.status == StageStatus.NOT_OBSERVED.value
    assert fin_stage.status == StageStatus.NOT_OBSERVED.value
    assert len(dep_stage.evidence_ids) == 0
    assert len(with_stage.evidence_ids) == 0
