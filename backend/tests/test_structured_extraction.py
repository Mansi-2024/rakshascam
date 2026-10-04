"""Unit tests for Phase 3 structured intelligence, entity extraction, claims, and relationships."""

import pytest
from app.services.html_extractor import (
    extract_comprehensive_analysis,
    extract_html_information,
)

PHASE3_TEST_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Apex Global Wealth Advisory Private Limited | Institutional Portfolio</title>
  <meta name="description" content="Premier wealth advisory authorized by SEBI.">
  <link rel="canonical" href="https://example-apex.test">
</head>
<body>
  <h1>Apex Global Wealth Advisory Private Limited</h1>
  <p class="leader">Chief Strategist: Dr. R. Sharma</p>
  <p class="intro">
    We provide guaranteed returns of 35% monthly and guaranteed profit on pre-IPO quotas.
    Our programs are completely risk-free investment options with 100% principal protection.
    Act now—this is an urgent limited time opportunity to double your money.
  </p>
  <section class="regulatory">
    <p>
      We are proud to be SEBI registered under License No. INA000099999.
      Corporate CIN: U67120MH2020PTC123456.
      Our firm is government approved and licensed for portfolio operations.
    </p>
  </section>
  <section class="settlement">
    <p>
      Deposit immediately to lock quota: send capital to our priority UPI settlement desk.
    </p>
  </section>
  <section class="withdrawals">
    <p>
      Standard withdrawal policy: account subject to tax clearance fee prior to withdrawal release.
      Additional payment required to restore frozen margin account.
    </p>
  </section>
  <nav>
    <a href="/portal">Internal Portal</a>
    <a href="https://partner-exchange.example/terminal">External Exchange</a>
  </nav>
</body>
</html>
"""


def test_company_and_entity_extraction():
    """1. Test deterministic extraction of company and person entities."""
    (
        _,
        _,
        _,
        _,
        entities,
        _,
        _,
        _,
        _,
        evidence,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    entity_names = [e.name for e in entities]
    assert any("Apex Global Wealth Advisory Private Limited" in name for name in entity_names)

    # Check entity types
    entity_types = {e.name: e.entity_type for e in entities}
    company_name = next(n for n in entity_names if "Private Limited" in n)
    assert entity_types[company_name] == "COMPANY"

    # Check domain entity
    assert "example-apex.test" in entity_names
    assert entity_types["example-apex.test"] == "DOMAIN"

    # Check person entity
    assert any("Dr. R. Sharma" in n for n in entity_names)
    person_name = next(n for n in entity_names if "Dr. R. Sharma" in n)
    assert entity_types[person_name] == "PERSON"


def test_regulatory_reference_extraction():
    """2. Test extraction of regulatory references (SEBI, Government)."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        reg_refs,
        _,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    authorities = [r.authority for r in reg_refs]
    assert "SEBI" in authorities
    assert any(r.claim_type in ("REGISTERED", "APPROVED", "LICENSED") for r in reg_refs)


def test_registration_association():
    """3. Test associating registration codes (SEBI INA/MCA CIN) with nearby regulatory context."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        reg_refs,
        _,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    # Find SEBI reference
    sebi_ref = next(r for r in reg_refs if r.authority == "SEBI")
    assert sebi_ref.registration_number is not None
    assert "INA000099999" in sebi_ref.registration_number
    assert sebi_ref.verification_status == "UNKNOWN"


def test_guaranteed_return_detection():
    """4. Test detection and classification of guaranteed return claims."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        fin_claims,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    guaranteed = [c for c in fin_claims if c.claim_type == "GUARANTEED_RETURN"]
    assert len(guaranteed) >= 1
    assert any("guaranteed return" in c.claim_text.lower() for c in guaranteed)
    assert all(c.severity == "HIGH" for c in guaranteed)


def test_risk_free_detection():
    """5. Test detection and classification of risk-free / principal protection claims."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        fin_claims,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    risk_free = [c for c in fin_claims if c.claim_type == "RISK_FREE"]
    assert len(risk_free) >= 1
    assert any("risk-free" in c.claim_text.lower() or "principal protection" in c.claim_text.lower() for c in risk_free)
    assert all(c.severity == "HIGH" for c in risk_free)


def test_urgency_and_act_now_detection():
    """6. Test detection of urgency, act now, and limited time phrasing."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        fin_claims,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    claim_types = [c.claim_type for c in fin_claims]
    assert "URGENCY" in claim_types or "ACT_NOW" in claim_types or "LIMITED_TIME" in claim_types


def test_deposit_pressure_detection():
    """7. Test detection of deposit pressure language."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        fin_claims,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    deposit_pressure = [c for c in fin_claims if c.claim_type == "DEPOSIT_PRESSURE"]
    assert len(deposit_pressure) >= 1
    assert any("deposit immediately" in c.claim_text.lower() or "send capital" in c.claim_text.lower() for c in deposit_pressure)
    assert deposit_pressure[0].severity == "HIGH"


def test_withdrawal_fee_detection():
    """8. Test detection of withdrawal lock/fee language."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        fin_claims,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    fee_claims = [c for c in fin_claims if c.claim_type == "WITHDRAWAL_FEE"]
    assert len(fee_claims) >= 1
    assert any("tax clearance fee" in c.claim_text.lower() or "withdrawal" in c.claim_text.lower() for c in fee_claims)
    assert fee_claims[0].severity == "HIGH"


def test_claim_construction():
    """9. Test synthesis of generalized Claim objects from references and signals."""
    (
        _,
        _,
        _,
        _,
        entities,
        claims,
        _,
        _,
        _,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    assert len(claims) >= 2
    types = [c.claim_type for c in claims]
    assert "REGULATORY" in types
    assert "FINANCIAL" in types

    # Subject entity should be assigned
    company = next((e for e in entities if e.entity_type == "COMPANY"), None)
    if company:
        assert any(c.subject_entity_id == company.id for c in claims)


def test_evidence_construction():
    """10. Test that every extracted entity and claim is traceable to an Evidence object."""
    (
        _,
        _,
        _,
        _,
        entities,
        claims,
        reg_refs,
        fin_claims,
        _,
        evidence,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    assert len(evidence) >= 5
    evidence_ids = {ev.id for ev in evidence}

    # Verify entities have evidence
    for ent in entities:
        assert ent.evidence_id in evidence_ids
        assert ent.evidence.text is not None
        assert ent.evidence.context is not None

    # Verify regulatory references have evidence
    for reg in reg_refs:
        assert reg.evidence_id in evidence_ids

    # Verify financial claims have evidence
    for fin in fin_claims:
        assert fin.evidence_id in evidence_ids


def test_unknown_verification_status():
    """11. Core Principle: Verification status MUST default to UNKNOWN."""
    (
        _,
        _,
        _,
        _,
        _,
        claims,
        reg_refs,
        fin_claims,
        relationships,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    for c in claims:
        assert c.verification_status == "UNKNOWN"

    for r in reg_refs:
        assert r.verification_status == "UNKNOWN"

    for f in fin_claims:
        assert f.verification_status == "UNKNOWN"

    for rel in relationships:
        assert rel.verification_status == "UNKNOWN"


def test_identity_relationship_construction():
    """12. Test preliminary relationship linking (Domain, Authorization, Registration, External link)."""
    (
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        relationships,
        _,
    ) = extract_comprehensive_analysis(PHASE3_TEST_HTML, "https://example-apex.test")

    rel_types = [r.relationship_type for r in relationships]
    assert "OPERATES_DOMAIN" in rel_types
    assert "CLAIMS_AUTHORIZATION" in rel_types
    assert "REFERENCES_REGISTRATION" in rel_types
    assert "LINKS_TO_EXTERNAL" in rel_types
    assert "ASSOCIATED_WITH" in rel_types

    # Ensure all relationships have context and unknown status
    for rel in relationships:
        assert rel.verification_status == "UNKNOWN"
        assert rel.description is not None
        assert len(rel.description) > 0
