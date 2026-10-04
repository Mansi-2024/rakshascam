"""Abstract base class for verification adapters."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from app.verification.models import VerificationResult


class VerificationAdapter(ABC):
    """Abstract interface for all authoritative and demonstration verification adapters."""

    @property
    @abstractmethod
    def adapter_name(self) -> str:
        """Name of the adapter."""
        pass

    @property
    @abstractmethod
    def is_demo(self) -> bool:
        """Indicates whether this adapter operates on simulated/fictional test data."""
        pass

    @abstractmethod
    def can_verify(self, claim_or_reference: Any) -> bool:
        """Determines if this adapter is capable of verifying the given claim or regulatory reference."""
        pass

    @abstractmethod
    async def verify(
        self,
        claim_or_reference: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        """Performs verification inquiry and produces a structured VerificationResult with complete provenance."""
        pass
