"""Unit tests for RakshaScan Authoritative Verification Architecture (Phase 4).

Validates:
1. Demo verified result
2. Demo contradictory result
3. Demo not-found result
4. Unknown result
5. Unavailable result
6. Exact registration matching
7. Entity mismatch
8. Contradictory registration ownership
9. Provenance preservation
10. Original claim preservation
11. Verification failure does not crash analysis
"""

import pytest
from app.schemas.analysis import ClaimModel, RegulatoryReferenceModel
from app.verification.adapters.demo import DemoVerificationAdapter
from app.verification.base import VerificationAdapter
from app.verification.engine import VerificationEngine
from app.verification.models import VerificationResult, VerificationStatus


import asyncio
import pytest
from app.schemas.analysis import ClaimModel, RegulatoryReferenceModel
from app.verification.adapters.demo import DemoVerificationAdapter
from app.verification.base import VerificationAdapter
from app.verification.engine import VerificationEngine
from app.verification.models import VerificationResult, VerificationStatus


@pytest.fixture
def demo_adapter():
    return DemoVerificationAdapter()


@pytest.fixture
def verification_engine():
    return VerificationEngine()


def test_demo_verified_result(demo_adapter):
    """Test 1: Fictional registration with matching fictional entity produces VERIFIED."""
    claim = {
        "id": "claim-demo-1",
        "registration_reference": "INA000099999",
        "referenced_authority": "SEBI",
    }
    context = {"entity_name": "Example Wealth Advisors Private Limited"}
    result = asyncio.run(demo_adapter.verify(claim, context=context))

    assert result.status == VerificationStatus.VERIFIED
    assert result.is_demo is True
    assert "Demonstration" in result.source_name
    assert result.matched_registration == "INA000099999"
    assert result.matched_entity == "Example Wealth Advisors Private Limited"
    assert "Active" in result.evidence
    assert result.claim_id == "claim-demo-1"


def test_demo_contradictory_result(demo_adapter):
    """Test 2: Fictional registration claimed by a different entity produces CONTRADICTORY."""
    claim = {
        "id": "claim-demo-2",
        "registration_reference": "INA000099999",
        "referenced_authority": "SEBI",
    }
    context = {"entity_name": "Unrelated Impersonation Syndicate"}
    result = asyncio.run(demo_adapter.verify(claim, context=context))

    assert result.status == VerificationStatus.CONTRADICTORY
    assert result.is_demo is True
    assert "contradicts" in result.evidence or "different entity" in result.reason
    assert "scam" not in result.reason.lower()  # Non-prejudicial
    assert result.matched_entity == "Example Wealth Advisors Private Limited"


def test_demo_not_found_result(demo_adapter):
    """Test 3: Non-existent registration query produces NOT_FOUND without asserting fraud."""
    claim = {
        "id": "claim-demo-3",
        "registration_reference": "INA000011111",
        "referenced_authority": "SEBI",
    }
    context = {"entity_name": "Some Company"}
    result = asyncio.run(demo_adapter.verify(claim, context=context))

    assert result.status == VerificationStatus.NOT_FOUND
    assert result.is_demo is True
    assert "Zero matching records" in result.evidence or "not found" in result.reason.lower()
    assert "fraud" not in result.reason.lower() or "does not constitute fraud" in result.reason.lower()


def test_unknown_result_on_missing_identifier(demo_adapter):
    """Test 4: Regulator reference without specific registration produces UNKNOWN."""
    ref = {
        "id": "ref-demo-4",
        "authority": "SEBI",
        "registration_number": None,
    }
    result = asyncio.run(demo_adapter.verify(ref))

    assert result.status == VerificationStatus.UNKNOWN
    assert result.is_demo is True
    assert "Insufficient" in result.reason
    assert result.matched_registration is None


def test_unavailable_result(demo_adapter):
    """Test 5: Simulated registry outage produces UNAVAILABLE without indicating fraud."""
    claim = {
        "id": "claim-demo-5",
        "registration_reference": "INA000099999",
    }
    context = {"simulate_unavailable": True}
    result = asyncio.run(demo_adapter.verify(claim, context=context))

    assert result.status == VerificationStatus.UNAVAILABLE
    assert result.is_demo is True
    assert "unreachable" in result.reason or "offline" in result.evidence.lower()
    assert result.status != VerificationStatus.NOT_FOUND


def test_exact_registration_matching(demo_adapter):
    """Test 6: Registration numbers are normalized and matched regardless of casing/spacing."""
    claim = {
        "id": "claim-demo-6",
        "registration_reference": "  ina000099999  ",
    }
    context = {"entity_name": "example wealth advisors private limited"}
    result = asyncio.run(demo_adapter.verify(claim, context=context))

    assert result.status == VerificationStatus.VERIFIED
    assert result.matched_registration == "INA000099999"


def test_entity_mismatch(demo_adapter):
    """Test 7: Conservative entity matching flags mismatched claimant."""
    claim = {
        "id": "claim-demo-7",
        "registration_reference": "INA000088888",
    }
    # INA000088888 is owned by 'Fictional Genuine Securities Limited' in the fixture
    context = {"entity_name": "Example Wealth Advisors Private Limited"}
    result = asyncio.run(demo_adapter.verify(claim, context=context))

    assert result.status == VerificationStatus.CONTRADICTORY
    assert result.matched_entity == "Fictional Genuine Securities Limited"


def test_contradictory_registration_ownership(demo_adapter):
    """Test 8: Contradictory result preserves authoritative owner name in matched_entity."""
    ref = {
        "id": "ref-demo-8",
        "registration_number": "INA000088888",
        "authority": "SEBI",
    }
    context = {"entity_name": "Totally Different Entity Pvt Ltd"}
    result = asyncio.run(demo_adapter.verify(ref, context=context))

    assert result.status == VerificationStatus.CONTRADICTORY
    assert result.matched_entity == "Fictional Genuine Securities Limited"
    assert "different entity" in result.reason


def test_provenance_preservation(demo_adapter):
    """Test 9: Every verification result retains full provenance metadata."""
    claim = {
        "id": "claim-demo-9",
        "registration_reference": "INA000099999",
    }
    result = asyncio.run(demo_adapter.verify(claim))

    assert result.source_name is not None and len(result.source_name) > 0
    assert result.checked_at is not None and "T" in result.checked_at
    assert result.verification_method is not None and len(result.verification_method) > 0
    assert result.evidence is not None and len(result.evidence) > 0
    assert result.reason is not None and len(result.reason) > 0
    assert isinstance(result.is_demo, bool)


def test_original_claim_preservation(verification_engine):
    """Test 10: Original claim text, evidence, and type are preserved after verification."""
    original_claim = ClaimModel(
        id="claim-test-10",
        claim_text="We are SEBI registered investment advisors",
        claim_type="REGULATORY",
        referenced_authority="SEBI",
        registration_reference="INA000099999",
        source="page_text",
        evidence_text="proud to be SEBI registered under INA000099999",
        verification_status="UNKNOWN",
    )

    claims = [original_claim]
    asyncio.run(
        verification_engine.verify_analysis_claims(
            claims=claims,
            regulatory_references=[],
            entities=[{"name": "Example Wealth Advisors Private Limited", "entity_type": "COMPANY"}],
        )
    )

    # Core claim attributes must remain completely intact
    assert claims[0].claim_text == "We are SEBI registered investment advisors"
    assert claims[0].claim_type == "REGULATORY"
    assert claims[0].referenced_authority == "SEBI"
    assert claims[0].registration_reference == "INA000099999"
    assert claims[0].source == "page_text"
    assert claims[0].evidence_text == "proud to be SEBI registered under INA000099999"

    # Verification status updated and verification object attached
    assert claims[0].verification_status == "VERIFIED"
    assert claims[0].verification is not None
    assert claims[0].verification.is_demo is True


def test_verification_failure_does_not_crash_analysis():
    """Test 11: An unexpected exception in an adapter safely produces UNAVAILABLE."""

    class FailingAdapter(VerificationAdapter):
        @property
        def adapter_name(self) -> str:
            return "FailingAdapter"

        @property
        def is_demo(self) -> bool:
            return False

        def can_verify(self, claim_or_reference) -> bool:
            return True

        async def verify(self, claim_or_reference, context=None):
            raise ConnectionResetError("Remote registry connection dropped abruptly!")

    engine = VerificationEngine(adapters=[FailingAdapter()])
    claim = {
        "id": "claim-fail-test",
        "registration_reference": "INA000099999",
    }

    # Must NOT raise exception
    result = asyncio.run(engine.verify_reference_or_claim(claim))

    assert result.status == VerificationStatus.UNAVAILABLE
    assert "ConnectionResetError" in result.evidence
    assert "UNAVAILABLE" in result.reason
