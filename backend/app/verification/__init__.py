"""RakshaScan Verification Architecture (Phase 4).

Modular, evidence-backed authoritative verification subsystem.
Core Principle: Extraction != Verification.
Verification results are only authoritative when derived from the identified authoritative source.
"""

from app.verification.models import VerificationResult, VerificationStatus
from app.verification.base import VerificationAdapter
from app.verification.engine import VerificationEngine

__all__ = [
    "VerificationResult",
    "VerificationStatus",
    "VerificationAdapter",
    "VerificationEngine",
]
