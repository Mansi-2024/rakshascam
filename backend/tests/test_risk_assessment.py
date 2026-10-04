"""Unit tests for RakshaScan Evidence Engine & Risk Assessment Engine (Phase 5).

Validates:
Evidence:
1. evidence creation
2. evidence provenance
3. evidence-to-claim relationship
4. evidence preservation

Risk:
5. guaranteed return rule
6. risk-free rule
7. double-money rule
8. deposit-pressure rule
9. withdrawal-fee rule
10. urgency rule
11. regulatory verification-needed rule
12. regulatory contradiction rule
13. registration-not-found rule
14. identity mismatch rule
15. duplicate signal suppression

Assessment:
16. insufficient evidence
17. low concern
18. moderate concern
19. high concern
20. uncertainty preservation
21. no numerical scam score
22. no fraud declaration
"""

import pytest
from app.evidence.engine import EvidenceEngine
from app.evidence.models import EvidenceRecord
from app.risk.engine import RiskAssessmentEngine
from app.risk.models import ConcernLevel, RiskCategory, RiskSeverity
from app.risk.rules import evaluate_risk_rules
from app.verification.models import VerificationResult, VerificationStatus


# ==============================================================================
# EVIDENCE ENGINE TESTS (1-4)
# ==============================================================================

def test_evidence_creation():
    """Test 1: EvidenceRecord can be created with required provenance fields."""
    ev = EvidenceRecord(
        evidence_id="ev-test-1",
        source_type="PAGE_TEXT",
        source_url="https://example-finance.test",
        extracted_text="SEBI registered under INA000099999",
        context="We are proud to be SEBI registered under INA000099999.",
        extraction_method="REGULATORY_PATTERN",
    )
    assert ev.evidence_id == "ev-test-1"
    assert ev.source_type == "PAGE_TEXT"
    assert ev.extracted_text == "SEBI registered under INA000099999"
    assert ev.created_at is not None


def test_evidence_provenance():
    """Test 2: EvidenceRecord preserves origin URL and extraction method."""
    ev = EvidenceRecord(
        evidence_id="ev-test-2",
        source_type="METADATA",
        source_url="https://example-finance.test/about",
        extracted_text="Example Wealth Advisors Private Limited",
        context="<title>Example Wealth Advisors Private Limited</title>",
        extraction_method="TITLE_EXTRACTION",
    )
    engine = EvidenceEngine([ev])
    retrieved = engine.get_evidence("ev-test-2")
    assert retrieved is not None
    assert retrieved.source_url == "https://example-finance.test/about"
    assert retrieved.extraction_method == "TITLE_EXTRACTION"


def test_evidence_to_claim_relationship():
    """Test 3: EvidenceRecord indexes linkages to related claims and entities."""
    ev = EvidenceRecord(
        evidence_id="ev-test-3",
        source_type="PAGE_TEXT",
        source_url="https://example-finance.test",
        extracted_text="18% guaranteed return monthly",
        context="Invest today and receive 18% guaranteed return monthly.",
        extraction_method="FINANCIAL_PATTERN",
        related_claim_id="claim-fin-1",
        related_entity_id="ent-corp-1",
    )
    engine = EvidenceEngine([ev])
    assert ev.related_claim_id == "claim-fin-1"
    assert ev.related_entity_id == "ent-corp-1"
    assert engine.get_evidence("ev-test-3") is not None


def test_evidence_preservation():
    """Test 4: Raw text is preserved verbatim without lossy alteration."""
    raw = "GUARANTEED 100% PROFIT!! NO LOSS RISK! Act NOW!!"
    ev = EvidenceRecord(
        evidence_id="ev-test-4",
        source_type="PAGE_TEXT",
        source_url="https://example.test",
        extracted_text=raw,
        context=f"Header: {raw}",
        extraction_method="FINANCIAL_PATTERN",
    )
    assert ev.extracted_text == raw
    assert "!!" in ev.extracted_text


# ==============================================================================
# RISK RULES TESTS (5-15)
# ==============================================================================

def test_guaranteed_return_rule():
    """Test 5: Rule 1 triggers FINANCIAL / HIGH on guaranteed return language."""
    fin = [{"id": "f1", "claim_type": "GUARANTEED_RETURN", "claim_text": "guaranteed 25% returns", "evidence_id": "ev-1"}]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.FINANCIAL
    assert signals[0].severity == RiskSeverity.HIGH
    assert "Guaranteed" in signals[0].title
    assert "ev-1" in signals[0].evidence_ids


def test_risk_free_rule():
    """Test 6: Rule 2 triggers FINANCIAL / HIGH on risk-free language."""
    fin = [{"id": "f2", "claim_type": "RISK_FREE", "claim_text": "zero risk investment", "evidence_id": "ev-2"}]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.FINANCIAL
    assert signals[0].severity == RiskSeverity.HIGH
    assert "risk" in signals[0].title.lower()


def test_double_money_rule():
    """Test 7: Rule 3 triggers FINANCIAL / HIGH on double-money language."""
    fin = [{"id": "f3", "claim_type": "DOUBLE_MONEY", "claim_text": "double your capital in 7 days", "evidence_id": "ev-3"}]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.FINANCIAL
    assert signals[0].severity == RiskSeverity.HIGH
    assert "doubling" in signals[0].title.lower()


def test_deposit_pressure_rule():
    """Test 8: Rule 4 triggers MANIPULATION / HIGH on deposit pressure."""
    fin = [{"id": "f4", "claim_type": "DEPOSIT_PRESSURE", "claim_text": "deposit immediately to unlock account", "evidence_id": "ev-4"}]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.MANIPULATION
    assert signals[0].severity == RiskSeverity.HIGH
    assert "deposit" in signals[0].title.lower()


def test_withdrawal_fee_rule():
    """Test 9: Rule 5 triggers FINANCIAL / HIGH on withdrawal fee demands."""
    fin = [{"id": "f5", "claim_type": "WITHDRAWAL_FEE", "claim_text": "pay 10% clearance fee before withdrawal", "evidence_id": "ev-5"}]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.FINANCIAL
    assert signals[0].severity == RiskSeverity.HIGH
    assert "withdrawal" in signals[0].title.lower()


def test_urgency_rule():
    """Test 10: Rule 6 triggers MANIPULATION / MEDIUM on urgency phrasing."""
    fin = [{"id": "f6", "claim_type": "ACT_NOW", "claim_text": "act now slots closing", "evidence_id": "ev-6"}]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.MANIPULATION
    assert signals[0].severity == RiskSeverity.MEDIUM
    assert "urgency" in signals[0].title.lower()


def test_regulatory_verification_needed_rule():
    """Test 11: Rule 7 triggers REGULATORY / MEDIUM when regulatory claim is unverified."""
    claims = [{"id": "c7", "claim_type": "REGULATORY", "claim_text": "SEBI registered", "verification_status": "UNKNOWN"}]
    signals = evaluate_risk_rules(claims=claims, regulatory_references=[], financial_claims=[], entities=[], verification_results=[])

    assert len(signals) == 1
    assert signals[0].category == RiskCategory.REGULATORY
    assert signals[0].severity == RiskSeverity.MEDIUM
    assert "requires verification" in signals[0].title.lower()
    assert "false" not in signals[0].title.lower()  # Do NOT call claim false


def test_regulatory_contradiction_rule():
    """Test 12: Rule 8 triggers REGULATORY / HIGH when verification is CONTRADICTORY."""
    vr = VerificationResult(
        id="vr-8",
        claim_id="c8",
        status=VerificationStatus.CONTRADICTORY,
        source_name="Official Directory",
        checked_at="2026-10-03T12:00:00Z",
        verification_method="REGISTRY_LOOKUP",
        matched_entity="Different Entity Ltd",
        matched_registration="INA000088888",
        evidence="Assigned to Different Entity Ltd",
        reason="Registration belongs to a different entity",
        is_demo=False,
    )
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=[], entities=[], verification_results=[vr])

    reg_signals = [s for s in signals if s.category == RiskCategory.REGULATORY]
    assert len(reg_signals) >= 1
    assert reg_signals[0].severity == RiskSeverity.HIGH
    assert "contradiction" in reg_signals[0].title.lower()
    assert "scam" not in reg_signals[0].explanation.lower()  # Never state "this is a scam"


def test_registration_not_found_rule():
    """Test 13: Rule 9 triggers REGULATORY / MEDIUM on NOT_FOUND with explicit caveat."""
    vr = VerificationResult(
        id="vr-9",
        claim_id="c9",
        status=VerificationStatus.NOT_FOUND,
        source_name="Official Directory",
        checked_at="2026-10-03T12:00:00Z",
        verification_method="REGISTRY_LOOKUP",
        evidence="Zero records matched",
        reason="Registration not found in database",
        is_demo=False,
    )
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=[], entities=[], verification_results=[vr])

    not_found_signals = [s for s in signals if "not be found" in s.title.lower()]
    assert len(not_found_signals) == 1
    assert not_found_signals[0].severity == RiskSeverity.MEDIUM
    assert "does not by itself establish fraud" in not_found_signals[0].explanation.lower()


def test_identity_mismatch_rule():
    """Test 14: Rule 10 triggers IDENTITY / HIGH when registration belongs to another entity."""
    vr = VerificationResult(
        id="vr-10",
        claim_id="c10",
        status=VerificationStatus.CONTRADICTORY,
        source_name="Official Directory",
        checked_at="2026-10-03T12:00:00Z",
        verification_method="REGISTRY_LOOKUP",
        matched_entity="Fictional Genuine Securities Limited",
        matched_registration="INA000088888",
        evidence="Officially registered to Fictional Genuine Securities Limited",
        reason="Registration reference is associated with a different entity",
        is_demo=True,
    )
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=[], entities=[], verification_results=[vr])

    id_signals = [s for s in signals if s.category == RiskCategory.IDENTITY]
    assert len(id_signals) == 1
    assert id_signals[0].severity == RiskSeverity.HIGH
    assert "Identity mismatch" in id_signals[0].title
    assert "Fictional Genuine Securities Limited" in id_signals[0].description


def test_duplicate_signal_suppression():
    """Test 15: Multiple occurrences of the same financial rule are deduplicated into one signal."""
    fin = [
        {"id": "f15a", "claim_type": "GUARANTEED_RETURN", "claim_text": "guaranteed returns", "evidence_id": "ev-15a"},
        {"id": "f15b", "claim_type": "GUARANTEED_RETURN", "claim_text": "guaranteed 18% monthly profit", "evidence_id": "ev-15b"},
        {"id": "f15c", "claim_type": "GUARANTEED_RETURN", "claim_text": "assured fixed return", "evidence_id": "ev-15c"},
    ]
    signals = evaluate_risk_rules(claims=[], regulatory_references=[], financial_claims=fin, entities=[], verification_results=[])

    guaranteed_signals = [s for s in signals if "Guaranteed-return" in s.title]
    assert len(guaranteed_signals) == 1  # Deduplicated into exactly 1 signal
    assert len(guaranteed_signals[0].evidence_ids) == 3  # All evidence IDs preserved
    assert len(guaranteed_signals[0].claim_ids) == 3


# ==============================================================================
# ASSESSMENT ENGINE TESTS (16-22)
# ==============================================================================

def test_insufficient_evidence_assessment():
    """Test 16: Empty or failed page extraction produces INSUFFICIENT_EVIDENCE."""
    engine = RiskAssessmentEngine()
    ev_engine = EvidenceEngine()
    assessment = engine.evaluate_assessment(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=False,
    )
    assert assessment.overall_level == ConcernLevel.INSUFFICIENT_EVIDENCE
    assert "Insufficient" in assessment.summary


def test_low_concern_assessment():
    """Test 17: Normal page with no major red flags produces LOW_CONCERN."""
    engine = RiskAssessmentEngine()
    ev_record1 = EvidenceRecord(
        evidence_id="ev-17a",
        source_url="https://example.com",
        extracted_text="About Our Advisory",
        context="We provide standard advisory services.",
        extraction_method="TEXT",
    )
    ev_record2 = EvidenceRecord(
        evidence_id="ev-17b",
        source_url="https://example.com",
        extracted_text="Contact Us",
        context="Email info@example.com",
        extraction_method="TEXT",
    )
    ev_engine = EvidenceEngine([ev_record1, ev_record2])

    assessment = engine.evaluate_assessment(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=True,
    )
    assert assessment.overall_level == ConcernLevel.LOW_CONCERN
    assert len(assessment.risk_signals) == 0


def test_moderate_concern_assessment():
    """Test 18: Unverified regulatory claim or urgency creates MODERATE_CONCERN."""
    engine = RiskAssessmentEngine()
    ev_record1 = EvidenceRecord(
        evidence_id="ev-18a",
        source_url="https://example.com",
        extracted_text="SEBI registered advisor",
        context="We are SEBI registered.",
        extraction_method="TEXT",
    )
    ev_engine = EvidenceEngine([ev_record1, ev_record1])
    claims = [{"id": "c18", "claim_type": "REGULATORY", "claim_text": "SEBI registered", "verification_status": "UNKNOWN"}]

    assessment = engine.evaluate_assessment(
        claims=claims,
        regulatory_references=[{"id": "r18", "authority": "SEBI", "claim_type": "REGULATORY_MENTION"}],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=True,
    )
    assert assessment.overall_level == ConcernLevel.MODERATE_CONCERN


def test_high_concern_assessment():
    """Test 19: Identity contradiction or multiple high financial signals produce HIGH_CONCERN."""
    engine = RiskAssessmentEngine()
    ev_engine = EvidenceEngine()
    fin = [
        {"id": "f19a", "claim_type": "GUARANTEED_RETURN", "claim_text": "guaranteed 30%", "evidence_id": "ev-19a"},
        {"id": "f19b", "claim_type": "DEPOSIT_PRESSURE", "claim_text": "deposit within 1 hour", "evidence_id": "ev-19b"},
    ]
    assessment = engine.evaluate_assessment(
        claims=[],
        regulatory_references=[],
        financial_claims=fin,
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=True,
    )
    assert assessment.overall_level == ConcernLevel.HIGH_CONCERN


def test_uncertainty_preservation():
    """Test 20: Assessment explicitly provides uncertainty notes."""
    engine = RiskAssessmentEngine()
    ev_engine = EvidenceEngine()
    assessment = engine.evaluate_assessment(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=True,
    )
    assert len(assessment.uncertainty_notes) > 0
    assert any("NOT_FOUND" in n or "Unverified" in n for n in assessment.uncertainty_notes)


def test_no_numerical_scam_score():
    """Test 21: Assessment does NOT expose any arbitrary numerical scam or trust score."""
    engine = RiskAssessmentEngine()
    ev_engine = EvidenceEngine()
    assessment = engine.evaluate_assessment(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=True,
    )
    # Check that assessment dict does NOT contain 'score', 'trust_score', 'scam_score', 'legit_score'
    asmt_dict = assessment.model_dump()
    assert "score" not in asmt_dict
    assert "scam_score" not in asmt_dict
    assert "trust_score" not in asmt_dict
    assert "fraud_probability" not in asmt_dict


def test_no_fraud_declaration():
    """Test 22: Assessment summary and signals do NOT make definitive judicial fraud declarations."""
    engine = RiskAssessmentEngine()
    ev_engine = EvidenceEngine()
    fin = [
        {"id": "f22a", "claim_type": "GUARANTEED_RETURN", "claim_text": "guaranteed return"},
        {"id": "f22b", "claim_type": "WITHDRAWAL_FEE", "claim_text": "withdrawal fee"},
    ]
    assessment = engine.evaluate_assessment(
        claims=[],
        regulatory_references=[],
        financial_claims=fin,
        entities=[],
        verification_results=[],
        evidence_engine=ev_engine,
        fetch_success=True,
    )
    # Never proclaim "This is a scam" or "Confirmed fraud"
    assert "this is a scam" not in assessment.summary.lower()
    assert "confirmed fraud" not in assessment.summary.lower()
    for sig in assessment.risk_signals:
        assert "this is a scam" not in sig.description.lower()
        assert "this is a scam" not in sig.explanation.lower()
