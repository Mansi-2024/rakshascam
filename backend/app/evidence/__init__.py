"""Evidence Engine Package (Phase 5).

Manages traceable evidence records anchored to raw webpage observations
and authoritative verification provenance.
"""

from app.evidence.models import EvidenceRecord
from app.evidence.engine import EvidenceEngine

__all__ = ["EvidenceRecord", "EvidenceEngine"]
