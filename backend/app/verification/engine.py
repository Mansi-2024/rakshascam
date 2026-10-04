"""Verification Engine for RakshaScan Phase 4.

Orchestrates verification adapters, maps claims to authoritative sources,
attaches structured results with provenance, and guarantees fault-tolerant execution.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.verification.adapters.demo import DemoVerificationAdapter
from app.verification.adapters.official_stubs import McaRegistryAdapter, SebiRegistryAdapter
from app.verification.base import VerificationAdapter
from app.verification.models import VerificationResult, VerificationStatus

logger = logging.getLogger("rakshascan.verification")


class VerificationEngine:
    """Orchestrates authoritative and demonstration verification for extracted claims and references."""

    def __init__(self, adapters: Optional[List[VerificationAdapter]] = None):
        if adapters is not None:
            self.adapters = adapters
        else:
            # Default adapter chain in priority order
            self.adapters = [
                DemoVerificationAdapter(),
                SebiRegistryAdapter(),
                McaRegistryAdapter(),
            ]

    def register_adapter(self, adapter: VerificationAdapter, priority: bool = False) -> None:
        """Register a new verification adapter."""
        if priority:
            self.adapters.insert(0, adapter)
        else:
            self.adapters.append(adapter)

    async def verify_reference_or_claim(
        self,
        item: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        """Finds an appropriate adapter and executes verification with complete exception isolation."""
        context = context or {}
        item_id = getattr(item, "id", None) or (item.get("id") if isinstance(item, dict) else None)
        reg_num = (
            getattr(item, "registration_number", None)
            or getattr(item, "registration_reference", None)
            or (item.get("registration_number") if isinstance(item, dict) else None)
        )

        # Find matching adapter
        selected_adapter: Optional[VerificationAdapter] = None
        for adapter in self.adapters:
            try:
                if adapter.can_verify(item):
                    selected_adapter = adapter
                    break
            except Exception as e:
                logger.warning(f"Error checking can_verify on adapter {adapter.adapter_name}: {e}")

        # If no adapter can handle it, return UNKNOWN
        if not selected_adapter:
            return VerificationResult(
                id=f"verif-unknown-{uuid.uuid4().hex[:8]}",
                claim_id=item_id,
                reference_id=item_id,
                status=VerificationStatus.UNKNOWN,
                source_name="None (No Applicable Verification Adapter)",
                source_url=None,
                checked_at=datetime.now(timezone.utc).isoformat(),
                verification_method="NO_ADAPTER_MATCH",
                matched_entity=None,
                matched_registration=reg_num,
                evidence="No authoritative verification adapter registered for this claim type or authority.",
                reason="Verification status remains UNKNOWN due to absence of an authoritative verification mechanism.",
                is_demo=False,
            )

        # Execute verification with safety boundary
        try:
            result = await selected_adapter.verify(item, context=context)
            # Ensure claim_id/reference_id are attached
            if not result.claim_id and item_id:
                result.claim_id = item_id
            if not result.reference_id and item_id:
                result.reference_id = item_id
            return result
        except Exception as e:
            logger.error(f"Verification adapter {selected_adapter.adapter_name} failed: {e}", exc_info=True)
            # Safe UNAVAILABLE fallback without crashing
            return VerificationResult(
                id=f"verif-err-{uuid.uuid4().hex[:8]}",
                claim_id=item_id,
                reference_id=item_id,
                status=VerificationStatus.UNAVAILABLE,
                source_name=f"{selected_adapter.adapter_name} (Encountered Error)",
                source_url=None,
                checked_at=datetime.now(timezone.utc).isoformat(),
                verification_method="ERROR_FALLBACK",
                matched_entity=None,
                matched_registration=reg_num,
                evidence=f"Verification provider query failed with internal exception: {type(e).__name__}.",
                reason="Verification inquiry could not be completed successfully. Verification state is UNAVAILABLE.",
                is_demo=selected_adapter.is_demo,
            )

    async def verify_analysis_claims(
        self,
        claims: List[Any],
        regulatory_references: List[Any],
        entities: List[Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[VerificationResult]:
        """Evaluates all claims and regulatory references, updates their verification statuses,

        and returns a complete list of VerificationResults while preserving original claim data.
        """
        context = context or {}
        results: List[VerificationResult] = []

        # Find primary corporate entity name if present in entities list
        primary_entity_name = None
        for entity in entities:
            e_type = getattr(entity, "entity_type", None) or (
                entity.get("entity_type") if isinstance(entity, dict) else None
            )
            e_name = getattr(entity, "name", None) or (entity.get("name") if isinstance(entity, dict) else None)
            if e_type in ["COMPANY", "ORGANIZATION"] and e_name:
                primary_entity_name = e_name
                break

        enriched_context = dict(context)
        if primary_entity_name and "entity_name" not in enriched_context:
            enriched_context["entity_name"] = primary_entity_name

        # 1. Verify regulatory references first
        for ref in regulatory_references:
            res = await self.verify_reference_or_claim(ref, context=enriched_context)
            results.append(res)
            # Update reference verification status and attach verification object if supported
            if hasattr(ref, "verification_status"):
                ref.verification_status = res.status.value
            if hasattr(ref, "verification"):
                ref.verification = res

        # 2. Verify claims (especially REGULATORY claims or claims with registration reference)
        for claim in claims:
            c_type = getattr(claim, "claim_type", None) or (
                claim.get("claim_type") if isinstance(claim, dict) else None
            )
            c_reg = getattr(claim, "registration_reference", None) or (
                claim.get("registration_reference") if isinstance(claim, dict) else None
            )

            # We verify claims that are regulatory or carry a registration number
            if c_type == "REGULATORY" or c_reg:
                res = await self.verify_reference_or_claim(claim, context=enriched_context)
                results.append(res)
                if hasattr(claim, "verification_status"):
                    claim.verification_status = res.status.value
                if hasattr(claim, "verification"):
                    claim.verification = res

        return results
