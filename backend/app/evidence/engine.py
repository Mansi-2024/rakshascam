"""Evidence Engine for RakshaScan Phase 5.

Collects, indexes, validates, and summarizes evidence records across extraction
and verification stages, ensuring an unbroken audit trail.
"""

from typing import Any, Dict, List, Optional
from app.evidence.models import EvidenceRecord, EvidenceSummary


class EvidenceEngine:
    """Manages the lifecycle, indexing, and aggregation of evidence records."""

    def __init__(self, initial_evidence: Optional[List[EvidenceRecord]] = None):
        self._evidence_by_id: Dict[str, EvidenceRecord] = {}
        self._claim_index: Dict[str, List[str]] = {}
        self._entity_index: Dict[str, List[str]] = {}

        if initial_evidence:
            for item in initial_evidence:
                self.register_evidence(item)

    def register_evidence(self, evidence: EvidenceRecord) -> None:
        """Register an evidence record and update cross-indices."""
        self._evidence_by_id[evidence.evidence_id] = evidence

        if evidence.related_claim_id:
            self._claim_index.setdefault(evidence.related_claim_id, []).append(evidence.evidence_id)
        if evidence.related_entity_id:
            self._entity_index.setdefault(evidence.related_entity_id, []).append(evidence.evidence_id)

    def get_evidence(self, evidence_id: str) -> Optional[EvidenceRecord]:
        """Retrieve evidence record by its identifier."""
        return self._evidence_by_id.get(evidence_id)

    def get_evidence_list(self, evidence_ids: List[str]) -> List[EvidenceRecord]:
        """Retrieve all matching evidence records."""
        return [self._evidence_by_id[eid] for eid in evidence_ids if eid in self._evidence_by_id]

    def get_all(self) -> List[EvidenceRecord]:
        """Return all registered evidence records."""
        return list(self._evidence_by_id.values())

    def compute_summary(
        self,
        claims: List[Any],
        verification_results: List[Any],
    ) -> EvidenceSummary:
        """Compute aggregated counts of verified, contradictory, unverified, and unknown claims."""
        verified = 0
        contradictory = 0
        unknown = 0
        unverified = 0

        # Check claim statuses
        for claim in claims:
            raw_v_status = getattr(claim, "verification_status", None) or (
                claim.get("verification_status") if isinstance(claim, dict) else "UNKNOWN"
            )
            v_status = getattr(raw_v_status, "value", str(raw_v_status)).upper()
            if "VERIFICATIONSTATUS." in v_status:
                v_status = v_status.replace("VERIFICATIONSTATUS.", "")

            if v_status == "VERIFIED":
                verified += 1
            elif v_status == "CONTRADICTORY":
                contradictory += 1
            elif v_status in ["NOT_FOUND", "UNAVAILABLE"]:
                unverified += 1
            else:
                unknown += 1

        return EvidenceSummary(
            total_evidence_count=len(self._evidence_by_id),
            verified_claims=verified,
            unverified_claims=unverified,
            contradictory_claims=contradictory,
            unknown_claims=unknown,
        )
