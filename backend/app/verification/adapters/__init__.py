"""Verification adapters package."""

from app.verification.adapters.demo import DemoVerificationAdapter
from app.verification.adapters.official_stubs import SebiRegistryAdapter, McaRegistryAdapter

__all__ = ["DemoVerificationAdapter", "SebiRegistryAdapter", "McaRegistryAdapter"]
