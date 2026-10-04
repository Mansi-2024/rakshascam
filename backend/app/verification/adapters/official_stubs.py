"""Official regulatory adapter stubs and investigation findings for RakshaScan Phase 4.

==================================================
REAL AUTHORITATIVE SOURCES INVESTIGATION SUMMARY
==================================================

1. SEBI (Securities and Exchange Board of India):
   - Public Directory: https://www.sebi.gov.in/intermediaries.html
   - Investigation: SEBI's intermediary lookup is served via dynamic session-based
     ASP.NET forms protected by anti-bot headers and viewstates. No public,
     unauthenticated REST API or OpenAPI endpoint is officially published for third parties.
   - Compliance with Safety Rules:
     - "Do NOT scrape a website blindly."
     - "Do NOT bypass CAPTCHA or authentication."
     - "Do NOT use unofficial third-party databases as authoritative sources."
   - Conclusion: Adapter strictly reports UNAVAILABLE rather than fabricating results
     or performing fragile, non-authoritative web scraping.

2. MCA (Ministry of Corporate Affairs - India):
   - Public Directory: https://www.mca.gov.in/content/mca/global/en/mca/master-data/MDS.html
   - Investigation: MCA v3 portal enforces interactive visual CAPTCHAs and session tokens.
     Official programmatic access (API Setu / Corporate Affairs Master Data API) requires
     government-sponsored institutional API credentials and enterprise OAuth signing.
   - Conclusion: Adapter strictly reports UNAVAILABLE for unauthenticated requests.

3. RBI (Reserve Bank of India):
   - Public Directory: https://rbi.org.in/scripts/BS_NBFCList.aspx
   - Investigation: RBI publishes monthly periodic spreadsheet/PDF catalogs of approved
     and cancelled NBFCs rather than a real-time HTTP query API.
   - Conclusion: Real-time query is UNAVAILABLE until authoritative bulk roster ingestion
     is introduced in a subsequent phase.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.verification.base import VerificationAdapter
from app.verification.models import VerificationResult, VerificationStatus


class SebiRegistryAdapter(VerificationAdapter):
    """SEBI registry adapter reporting explicit UNAVAILABLE status in compliance

    with the non-scraping and non-fabrication mandates.
    """

    @property
    def adapter_name(self) -> str:
        return "SebiRegistryAdapter"

    @property
    def is_demo(self) -> bool:
        return False

    def can_verify(self, claim_or_reference: Any) -> bool:
        authority = getattr(claim_or_reference, "authority", None) or getattr(
            claim_or_reference, "referenced_authority", None
        )
        return authority == "SEBI"

    async def verify(
        self,
        claim_or_reference: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        claim_id = getattr(claim_or_reference, "id", None)
        reg_num = (
            getattr(claim_or_reference, "registration_number", None)
            or getattr(claim_or_reference, "registration_reference", None)
        )
        now_iso = datetime.now(timezone.utc).isoformat()

        return VerificationResult(
            id=f"verif-sebi-{uuid.uuid4().hex[:8]}",
            claim_id=claim_id,
            reference_id=claim_id,
            status=VerificationStatus.UNAVAILABLE,
            source_name="Securities and Exchange Board of India (SEBI)",
            source_url="https://www.sebi.gov.in/intermediaries.html",
            checked_at=now_iso,
            verification_method="OFFICIAL_REGISTRY_INVESTIGATION",
            matched_entity=None,
            matched_registration=reg_num,
            evidence="SEBI official intermediary registry requires interactive web session; no public unauthenticated machine-readable API is available.",
            reason="Authoritative SEBI integration is currently UNAVAILABLE without authenticated enterprise access or interactive human verification. Result is not fabricated.",
            is_demo=False,
        )


class McaRegistryAdapter(VerificationAdapter):
    """MCA registry adapter reporting explicit UNAVAILABLE status."""

    @property
    def adapter_name(self) -> str:
        return "McaRegistryAdapter"

    @property
    def is_demo(self) -> bool:
        return False

    def can_verify(self, claim_or_reference: Any) -> bool:
        authority = getattr(claim_or_reference, "authority", None) or getattr(
            claim_or_reference, "referenced_authority", None
        )
        return authority == "MCA"

    async def verify(
        self,
        claim_or_reference: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        claim_id = getattr(claim_or_reference, "id", None)
        reg_num = (
            getattr(claim_or_reference, "registration_number", None)
            or getattr(claim_or_reference, "registration_reference", None)
        )
        now_iso = datetime.now(timezone.utc).isoformat()

        return VerificationResult(
            id=f"verif-mca-{uuid.uuid4().hex[:8]}",
            claim_id=claim_id,
            reference_id=claim_id,
            status=VerificationStatus.UNAVAILABLE,
            source_name="Ministry of Corporate Affairs (MCA)",
            source_url="https://www.mca.gov.in/content/mca/global/en/mca/master-data/MDS.html",
            checked_at=now_iso,
            verification_method="OFFICIAL_REGISTRY_INVESTIGATION",
            matched_entity=None,
            matched_registration=reg_num,
            evidence="MCA Master Data search requires interactive CAPTCHA validation and partner credentials. Public open API is unavailable.",
            reason="Authoritative MCA verification is UNAVAILABLE in this phase. The system does not bypass CAPTCHA or fabricate company records.",
            is_demo=False,
        )
