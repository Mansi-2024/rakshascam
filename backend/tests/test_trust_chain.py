"""Tests for RakshaScan Phase 6 Financial Trust Chain.

Covers:
1. node creation
2. relationship creation
3. verified relationship
4. contradictory relationship
5. unknown relationship
6. missing evidence does not create relationship / marks unobserved
7. status does not incorrectly propagate
8. evidence traceability
9. summary counts are calculated correctly
"""

import pytest
from app.trust_chain.builder import TrustChainBuilder
from app.trust_chain.models import (
    TrustChainGraph,
    TrustChainNode,
    TrustChainNodeType,
    TrustChainRelationship,
    TrustChainRelationshipType,
    TrustChainStatus,
)


def test_trust_chain_node_creation():
    """1. Test that all 8 core trust chain nodes are created with appropriate types and labels."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence=[],
        links=[],
        page_data=None,
        target_url="https://example.test",
        contact_signals={},
    )

    assert isinstance(graph, TrustChainGraph)
    assert len(graph.nodes) == 8
    node_types = [n.node_type for n in graph.nodes]
    expected_types = [
        TrustChainNodeType.CLAIM.value,
        TrustChainNodeType.ENTITY.value,
        TrustChainNodeType.REGISTRATION.value,
        TrustChainNodeType.OFFICIAL_IDENTITY.value,
        TrustChainNodeType.WEBSITE.value,
        TrustChainNodeType.APP.value,
        TrustChainNodeType.SOCIAL_ACCOUNT.value,
        TrustChainNodeType.PAYMENT_IDENTITY.value,
    ]
    for et in expected_types:
        assert et in node_types, f"Missing node type {et}"


def test_trust_chain_relationship_creation():
    """2. Test that relationships between nodes are constructed."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence=[],
        links=[],
        page_data=None,
        target_url="https://example.test",
        contact_signals={},
    )

    assert len(graph.relationships) > 0
    for rel in graph.relationships:
        assert isinstance(rel, TrustChainRelationship)
        assert rel.source_node_id
        assert rel.target_node_id
        assert rel.relationship_type
        assert rel.status
        assert rel.explanation


def test_trust_chain_verified_relationship():
    """3. Test verified relationship when directory confirms entity and registration."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[
            {
                "id": "claim-1",
                "claim_text": "SEBI Registered Advisory INA000099999",
                "evidence_id": "ev-claim-1",
            }
        ],
        regulatory_references=[
            {
                "id": "reg-1",
                "registration_number": "INA000099999",
                "raw_text": "SEBI registered under License No. INA000099999",
                "evidence_id": "ev-reg-1",
            }
        ],
        financial_claims=[],
        entities=[
            {
                "id": "ent-1",
                "name": "Genuine Advisory Services Limited",
                "evidence_id": "ev-ent-1",
            }
        ],
        verification_results=[
            {
                "id": "vr-1",
                "reference_id": "reg-1",
                "status": "VERIFIED",
                "matched_entity": "Genuine Advisory Services Limited",
                "matched_registration": "INA000099999",
            }
        ],
        evidence=[{"id": "ev-page-1"}],
        links=[],
        page_data=None,
        target_url="https://genuine-advisory.test",
        contact_signals={},
    )

    # Check that registration node is VERIFIED
    reg_node = next(n for n in graph.nodes if n.node_type == TrustChainNodeType.REGISTRATION.value)
    assert reg_node.status == TrustChainStatus.VERIFIED.value

    # Check ENTITY -> REGISTRATION relationship is VERIFIED
    rel_entity_reg = next(
        r for r in graph.relationships
        if r.relationship_type == TrustChainRelationshipType.REGISTERED_AS.value
    )
    assert rel_entity_reg.status == TrustChainStatus.VERIFIED.value
    assert "verified" in rel_entity_reg.explanation.lower()


def test_trust_chain_contradictory_relationship():
    """4. Test contradictory relationship when registration belongs to a different entity."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[
            {
                "id": "claim-1",
                "claim_text": "SEBI Registered Advisory INA000088888",
                "evidence_id": "ev-claim-1",
            }
        ],
        regulatory_references=[
            {
                "id": "reg-1",
                "registration_number": "INA000088888",
                "raw_text": "SEBI license INA000088888",
                "evidence_id": "ev-reg-1",
            }
        ],
        financial_claims=[],
        entities=[
            {
                "id": "ent-1",
                "name": "Example Wealth Advisors Private Limited",
                "evidence_id": "ev-ent-1",
            }
        ],
        verification_results=[
            {
                "id": "vr-1",
                "reference_id": "reg-1",
                "status": "CONTRADICTORY",
                "matched_entity": "Fictional Genuine Securities Limited",
                "matched_registration": "INA000088888",
            }
        ],
        evidence=[{"id": "ev-page-1"}],
        links=[],
        page_data=None,
        target_url="https://example-wealth.test",
        contact_signals={},
    )

    # Check that registration node is CONTRADICTORY
    reg_node = next(n for n in graph.nodes if n.node_type == TrustChainNodeType.REGISTRATION.value)
    assert reg_node.status == TrustChainStatus.CONTRADICTORY.value

    # Check relationship is CONTRADICTORY with explicit explanation
    rel_entity_reg = next(
        r for r in graph.relationships
        if r.relationship_type == TrustChainRelationshipType.REGISTERED_AS.value
    )
    assert rel_entity_reg.status == TrustChainStatus.CONTRADICTORY.value
    assert "contradiction" in rel_entity_reg.explanation.lower() or "different entity" in rel_entity_reg.explanation.lower()
    # Explicitly check that node is NOT labeled "SCAM" per requirements
    assert "scam" not in reg_node.value.lower()


def test_trust_chain_unknown_relationship():
    """5. Test unknown relationship when insufficient evidence exists."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[],
        verification_results=[],
        evidence=[],
        links=[],
        page_data=None,
        target_url="https://unknown-site.test",
        contact_signals={},
    )

    rel_claim_entity = next(
        r for r in graph.relationships
        if r.relationship_type == TrustChainRelationshipType.CLAIMS.value
    )
    assert rel_claim_entity.status == TrustChainStatus.UNKNOWN.value
    assert "insufficient evidence" in rel_claim_entity.explanation.lower()


def test_trust_chain_missing_evidence_does_not_create_fabricated_relationship():
    """6. Test that absent payment/app identity does not invent links."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[],
        financial_claims=[],
        entities=[{"id": "e1", "name": "Some Company", "evidence_id": "ev1"}],
        verification_results=[],
        evidence=[{"id": "ev1"}],
        links=[],
        page_data=None,
        target_url="https://some-company.test",
        contact_signals={},
    )

    # Check payment node is NOT_OBSERVED or UNKNOWN
    pay_node = next(n for n in graph.nodes if n.node_type == TrustChainNodeType.PAYMENT_IDENTITY.value)
    assert pay_node.status == TrustChainStatus.NOT_OBSERVED.value

    # Check payment relationship is NOT_OBSERVED, NOT verified
    pay_rel = next(
        r for r in graph.relationships
        if r.relationship_type == TrustChainRelationshipType.RECEIVES_PAYMENT.value
    )
    assert pay_rel.status == TrustChainStatus.NOT_OBSERVED.value
    assert "no supporting evidence" in pay_rel.explanation.lower()


def test_trust_chain_status_does_not_propagate_incorrectly():
    """7. Test status propagation rule: REGISTRATION = VERIFIED does NOT make WEBSITE = VERIFIED."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[
            {"id": "r1", "registration_number": "INA000011111", "raw_text": "SEBI INA000011111", "evidence_id": "ev1"}
        ],
        financial_claims=[],
        entities=[{"id": "e1", "name": "Verified Advisor", "evidence_id": "ev2"}],
        verification_results=[
            {
                "id": "vr1",
                "reference_id": "r1",
                "status": "VERIFIED",
                "matched_entity": "Verified Advisor",
            }
        ],
        evidence=[{"id": "ev1"}],
        links=[],
        page_data=None,
        target_url="https://unverified-third-party-host.test",
        contact_signals={},
    )

    reg_node = next(n for n in graph.nodes if n.node_type == TrustChainNodeType.REGISTRATION.value)
    website_node = next(n for n in graph.nodes if n.node_type == TrustChainNodeType.WEBSITE.value)

    assert reg_node.status == TrustChainStatus.VERIFIED.value
    # Crucial rule: Website must NOT become VERIFIED just because registration is verified!
    assert website_node.status != TrustChainStatus.VERIFIED.value
    assert website_node.status == TrustChainStatus.UNVERIFIED.value


def test_trust_chain_evidence_traceability():
    """8. Test that nodes and relationships link to actual evidence IDs."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[
            {"id": "r1", "registration_number": "INA000099999", "raw_text": "SEBI INA000099999", "evidence_id": "ev-reg-trace-123"}
        ],
        financial_claims=[],
        entities=[{"id": "e1", "name": "Entity Name", "evidence_id": "ev-ent-trace-456"}],
        verification_results=[],
        evidence=[{"id": "ev-page-789"}],
        links=[],
        page_data=None,
        target_url="https://example.test",
        contact_signals={},
    )

    reg_node = next(n for n in graph.nodes if n.node_type == TrustChainNodeType.REGISTRATION.value)
    assert "ev-reg-trace-123" in reg_node.evidence_ids

    rel = next(
        r for r in graph.relationships
        if r.relationship_type == TrustChainRelationshipType.REGISTERED_AS.value
    )
    assert "ev-reg-trace-123" in rel.evidence_ids
    assert "ev-ent-trace-456" in rel.evidence_ids


def test_trust_chain_summary_counts_calculated_correctly():
    """9. Test summary counts match the actual status distribution of relationships."""
    builder = TrustChainBuilder()
    graph = builder.build_trust_chain(
        claims=[],
        regulatory_references=[
            {"id": "r1", "registration_number": "INA000099999", "raw_text": "SEBI INA000099999", "evidence_id": "ev1"}
        ],
        financial_claims=[],
        entities=[{"id": "e1", "name": "Company", "evidence_id": "ev2"}],
        verification_results=[
            {
                "id": "vr1",
                "reference_id": "r1",
                "status": "VERIFIED",
                "matched_entity": "Company",
            }
        ],
        evidence=[{"id": "ev1"}],
        links=[],
        page_data=None,
        target_url="https://example.test",
        contact_signals={},
    )

    summary = graph.summary
    assert summary.total_relationships == len(graph.relationships)
    computed_verified = sum(1 for r in graph.relationships if r.status == TrustChainStatus.VERIFIED.value)
    computed_unverified = sum(1 for r in graph.relationships if r.status == TrustChainStatus.UNVERIFIED.value)
    computed_contradictory = sum(1 for r in graph.relationships if r.status == TrustChainStatus.CONTRADICTORY.value)
    computed_unknown = sum(1 for r in graph.relationships if r.status == TrustChainStatus.UNKNOWN.value)
    computed_unobserved = sum(1 for r in graph.relationships if r.status in [TrustChainStatus.NOT_OBSERVED.value, TrustChainStatus.UNAVAILABLE.value])

    assert summary.verified_count == computed_verified
    assert summary.unverified_count == computed_unverified
    assert summary.contradictory_count == computed_contradictory
    assert summary.unknown_count == computed_unknown
    assert summary.unobserved_count == computed_unobserved
    assert str(summary.total_relationships) in summary.summary_text


@pytest.mark.anyio
async def test_url_analyzer_service_includes_trust_chain_and_scam_journey():
    """Integration test: analyze_url_service produces trust_chain and scam_journey."""
    from app.services.url_analyzer import analyze_url_service

    result = await analyze_url_service("https://example-finance.test")
    assert result.trust_chain is not None
    assert len(result.trust_chain.nodes) == 8
    assert len(result.trust_chain.relationships) > 0
    assert result.trust_chain.summary.total_relationships > 0

    assert result.scam_journey is not None
    assert len(result.scam_journey.stages) == 6
    assert result.scam_journey.confidence in ["LOW", "MEDIUM", "HIGH"]
    assert result.scam_journey.disclaimer == (
        "This represents a reconstructed pattern, not a determination that a specific case is fraudulent."
    )

