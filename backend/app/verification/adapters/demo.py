"""Demonstration verification adapter for RakshaScan Phase 4.

IMPORTANT:
This adapter operates strictly on synthetic, fictional demonstration records.
It does NOT query real-world regulatory databases (SEBI, MCA, RBI) and does
NOT produce legally binding or authoritative real-world determinations.
All results are explicitly labeled with `is_demo = True`.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.verification.base import VerificationAdapter
from app.verification.models import VerificationResult, VerificationStatus


# In-memory synthetic demonstration records for testing verification architecture
DEMO_REGISTRY = {
    "INA000099999": {
        "authority": "SEBI",
        "category": "Investment Adviser",
        "registered_entity": "Example Wealth Advisors Private Limited",
        "registration_number": "INA000099999",
        "status": "ACTIVE",
        "valid_until": "2028-12-31",
        "source_name": "Demonstration Regulatory Directory (Fictional / Non-Authoritative)",
        "source_url": "https://registry.demo.internal/sebi/advisers/INA000099999",
    },
    "INA000088888": {
        "authority": "SEBI",
        "category": "Stock Broker",
        "registered_entity": "Fictional Genuine Securities Limited",
        "registration_number": "INA000088888",
        "status": "ACTIVE",
        "valid_until": "2029-06-30",
        "source_name": "Demonstration Regulatory Directory (Fictional / Non-Authoritative)",
        "source_url": "https://registry.demo.internal/sebi/brokers/INA000088888",
    },
    "U67190MH2021PTC369999": {
        "authority": "MCA",
        "category": "Company Incorporation",
        "registered_entity": "Example Wealth Advisors Private Limited",
        "registration_number": "U67190MH2021PTC369999",
        "status": "ACTIVE",
        "valid_until": "PERPETUAL",
        "source_name": "Demonstration MCA Master Data (Fictional / Non-Authoritative)",
        "source_url": "https://registry.demo.internal/mca/company/U67190MH2021PTC369999",
    },
}


class DemoVerificationAdapter(VerificationAdapter):
    """Deterministic demonstration verification adapter for testing the architecture."""

    @property
    def adapter_name(self) -> str:
        return "DemoVerificationAdapter"

    @property
    def is_demo(self) -> bool:
        return True

    def can_verify(self, claim_or_reference: Any) -> bool:
        """Determines if the claim or regulatory reference has an identifier or context

        that can be evaluated against the demonstration fixture.
        """
        # Check for registration number attribute or dict key
        reg_num = getattr(claim_or_reference, "registration_number", None) or getattr(
            claim_or_reference, "registration_reference", None
        )
        if not reg_num and isinstance(claim_or_reference, dict):
            reg_num = claim_or_reference.get("registration_number") or claim_or_reference.get("registration_reference")

        # Handles demo registration numbers or references targeting SEBI/MCA in demo mode
        if reg_num:
            return True

        authority = getattr(claim_or_reference, "authority", None) or getattr(
            claim_or_reference, "referenced_authority", None
        )
        if authority in ["SEBI", "MCA", "RBI"]:
            return True

        return False

    async def verify(
        self,
        claim_or_reference: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        """Performs conservative, deterministic evaluation of the claim or reference against

        synthetic demonstration records.
        """
        context = context or {}
        check_id = f"verif-demo-{uuid.uuid4().hex[:8]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # Extract identifiers from claim or reference object
        claim_id = getattr(claim_or_reference, "id", None)
        if isinstance(claim_or_reference, dict):
            claim_id = claim_or_reference.get("id")

        reg_num = (
            getattr(claim_or_reference, "registration_number", None)
            or getattr(claim_or_reference, "registration_reference", None)
        )
        if not reg_num and isinstance(claim_or_reference, dict):
            reg_num = claim_or_reference.get("registration_number") or claim_or_reference.get("registration_reference")

        # Entity claiming the registration
        claimed_entity = context.get("entity_name")
        if not claimed_entity:
            claimed_entity = getattr(claim_or_reference, "subject_entity_name", None)

        # 1. Check for simulated unavailability
        if context.get("simulate_unavailable") or (reg_num and "UNAVAILABLE" in reg_num.upper()):
            return VerificationResult(
                id=check_id,
                claim_id=claim_id,
                reference_id=claim_id,
                status=VerificationStatus.UNAVAILABLE,
                source_name="Demonstration Regulatory Directory (Fictional / Non-Authoritative)",
                source_url=None,
                checked_at=now_iso,
                verification_method="DEMO_REGISTRY_LOOKUP",
                matched_entity=None,
                matched_registration=reg_num,
                evidence="Demonstration registry connection timed out or is temporarily offline.",
                reason="The demonstration registry could not be reached. This does not indicate fraud or non-existence.",
                is_demo=True,
            )

        # 2. Check for missing registration identifier -> UNKNOWN
        if not reg_num:
            auth_name = getattr(claim_or_reference, "authority", None) or getattr(
                claim_or_reference, "referenced_authority", "the regulator"
            )
            return VerificationResult(
                id=check_id,
                claim_id=claim_id,
                reference_id=claim_id,
                status=VerificationStatus.UNKNOWN,
                source_name="Demonstration Regulatory Directory (Fictional / Non-Authoritative)",
                source_url=None,
                checked_at=now_iso,
                verification_method="DEMO_REGISTRY_LOOKUP",
                matched_entity=None,
                matched_registration=None,
                evidence=f"Text mentions {auth_name} authorization without specifying an verifiable license or registration number.",
                reason="Insufficient evidence: an authoritative check requires a distinct registration or license identifier.",
                is_demo=True,
            )

        # Normalize registration number for lookup
        reg_key = reg_num.strip().upper()

        # 3. Check if registration exists in synthetic demonstration registry
        if reg_key not in DEMO_REGISTRY:
            return VerificationResult(
                id=check_id,
                claim_id=claim_id,
                reference_id=claim_id,
                status=VerificationStatus.NOT_FOUND,
                source_name="Demonstration Regulatory Directory (Fictional / Non-Authoritative)",
                source_url=None,
                checked_at=now_iso,
                verification_method="DEMO_REGISTRY_LOOKUP",
                matched_entity=None,
                matched_registration=None,
                evidence=f"Queried demonstration database for registration '{reg_num}'. Zero matching records returned.",
                reason="The demonstration registry was successfully queried, but the claimed registration reference was not found. This alone does not constitute fraud.",
                is_demo=True,
            )

        record = DEMO_REGISTRY[reg_key]
        official_owner = record["registered_entity"]

        # 4. Check entity matching (conservative matching)
        if claimed_entity:
            # Normalize names: lowercase, strip punctuation
            norm_claimed = claimed_entity.lower().replace(".", "").replace(",", "").strip()
            norm_official = official_owner.lower().replace(".", "").replace(",", "").strip()

            # Exact or core substring match
            if norm_claimed == norm_official or (len(norm_claimed) > 5 and norm_claimed in norm_official):
                return VerificationResult(
                    id=check_id,
                    claim_id=claim_id,
                    reference_id=claim_id,
                    status=VerificationStatus.VERIFIED,
                    source_name=record["source_name"],
                    source_url=record["source_url"],
                    checked_at=now_iso,
                    verification_method="DEMO_REGISTRY_LOOKUP",
                    matched_entity=official_owner,
                    matched_registration=record["registration_number"],
                    evidence=(
                        f"Active {record['category']} record confirmed in demonstration database for "
                        f"'{record['registration_number']}' belonging to '{official_owner}'."
                    ),
                    reason="Demonstration registry record matches both registration reference and claiming entity name.",
                    is_demo=True,
                )
            else:
                # Contradictory: Registration exists, but belongs to someone else!
                return VerificationResult(
                    id=check_id,
                    claim_id=claim_id,
                    reference_id=claim_id,
                    status=VerificationStatus.CONTRADICTORY,
                    source_name=record["source_name"],
                    source_url=record["source_url"],
                    checked_at=now_iso,
                    verification_method="DEMO_REGISTRY_LOOKUP",
                    matched_entity=official_owner,
                    matched_registration=record["registration_number"],
                    evidence=(
                        f"Demonstration registry indicates registration '{record['registration_number']}' "
                        f"is issued to '{official_owner}', which contradicts the claiming entity '{claimed_entity}'."
                    ),
                    reason="Registration reference exists, but authoritative demonstration records associate it with a different entity.",
                    is_demo=True,
                )

        # If entity name was not provided, but registration exists in demo database
        return VerificationResult(
            id=check_id,
            claim_id=claim_id,
            reference_id=claim_id,
            status=VerificationStatus.VERIFIED,
            source_name=record["source_name"],
            source_url=record["source_url"],
            checked_at=now_iso,
            verification_method="DEMO_REGISTRY_LOOKUP",
            matched_entity=official_owner,
            matched_registration=record["registration_number"],
            evidence=f"Active registration record found in demonstration records for '{record['registration_number']}' ({official_owner}).",
            reason="Demonstration registry contains an active registration matching the claimed number.",
            is_demo=True,
        )
