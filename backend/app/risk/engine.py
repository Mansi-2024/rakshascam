"""Risk Assessment Engine for RakshaScan Phase 5.

Synthesizes evidence records, verification outcomes, and risk signals into a
transparent, deterministic assessment without arbitrary numerical scam scores.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.evidence.engine import EvidenceEngine
from app.risk.models import Assessment, ConcernLevel, RiskCategory, RiskSeverity, RiskSignal
from app.risk.rules import evaluate_risk_rules


class RiskAssessmentEngine:
    """Deterministic assessment engine evaluating risk signals and synthesizing explainable concern levels."""

    def evaluate_assessment(
        self,
        claims: List[Any],
        regulatory_references: List[Any],
        financial_claims: List[Any],
        entities: List[Any],
        verification_results: List[Any],
        evidence_engine: EvidenceEngine,
        fetch_success: bool = True,
    ) -> Assessment:
        """Executes transparent risk assessment synthesis."""
        now_iso = datetime.now(timezone.utc).isoformat()
        assessment_id = f"asmt-{uuid.uuid4().hex[:8]}"

        # 1. Evaluate deterministic risk signals
        signals: List[RiskSignal] = evaluate_risk_rules(
            claims=claims,
            regulatory_references=regulatory_references,
            financial_claims=financial_claims,
            entities=entities,
            verification_results=verification_results,
        )

        # 2. Gather evidence statistics from evidence engine
        ev_summary = evidence_engine.compute_summary(
            claims=claims,
            verification_results=verification_results,
        )

        # 3. Categorize signals by severity and category
        high_signals = [s for s in signals if s.severity == RiskSeverity.HIGH]
        med_signals = [s for s in signals if s.severity == RiskSeverity.MEDIUM]
        low_signals = [s for s in signals if s.severity == RiskSeverity.LOW]

        high_identity_or_reg = [
            s for s in high_signals
            if s.category in [RiskCategory.IDENTITY, RiskCategory.REGULATORY]
        ]
        high_fin_or_manip = [
            s for s in high_signals
            if s.category in [RiskCategory.FINANCIAL, RiskCategory.MANIPULATION]
        ]

        # 4. Deterministic Concern Level Logic
        if not fetch_success or (ev_summary.total_evidence_count < 2 and not claims and not financial_claims):
            level = ConcernLevel.INSUFFICIENT_EVIDENCE
            summary = (
                "Insufficient observable evidence was available to conduct a comprehensive trust evaluation. "
                "The target webpage could not be fully analyzed or contained minimal parseable financial content."
            )
        elif len(high_identity_or_reg) >= 1 or len(high_fin_or_manip) >= 2:
            level = ConcernLevel.HIGH_CONCERN
            if len(high_identity_or_reg) >= 1:
                summary = (
                    "Significant evidence-backed concerns identified: An authoritative registry contradiction "
                    "or corporate identity mismatch was detected alongside high-risk representations."
                )
            else:
                summary = (
                    "Multiple high-severity financial patterns detected: The presentation simultaneously "
                    "promotes unconditional returns and coercive transactional pressures."
                )
        elif (
            len(high_fin_or_manip) == 1
            or len(med_signals) >= 1
            or ev_summary.unverified_claims > 0
            or (claims and ev_summary.unknown_claims > 0)
        ):
            level = ConcernLevel.MODERATE_CONCERN
            summary = (
                "Moderate concerns identified: The presentation features unverified regulatory claims "
                "or aggressive financial language that requires independent third-party confirmation."
            )
        else:
            level = ConcernLevel.LOW_CONCERN
            summary = (
                "Low observable concern: No critical identity contradictions or high-pressure financial promises "
                "were detected in the analyzed public webpage content."
            )

        # 5. Formulate Uncertainty Notes
        uncertainty_notes: List[str] = [
            "This assessment evaluates public on-page observations and linked directory checks; it does not audit private offline operations.",
            "Unverified or unknown claims do NOT indicate fraud; they require independent validation on official regulatory portals.",
            "A registration status of NOT_FOUND does not by itself establish fraud, as registrations may be newly filed or under variant legal spellings.",
            "Linguistic severity categorizes promotional language patterns, not legal culpability or counterparty insolvency.",
        ]

        # 6. Tailor Safe Next Steps
        safe_next_steps: List[str] = []
        if level == ConcernLevel.HIGH_CONCERN:
            safe_next_steps = [
                "Do NOT transfer funds, share bank account numbers, or deposit cryptocurrencies.",
                "Verify the corporate entity and registration number directly on the official SEBI (sebi.gov.in) or MCA (mca.gov.in) directory.",
                "Never make payments to individual savings accounts or personal UPI VPAs for corporate investments.",
                "If pressured by phone or messaging apps, preserve chat transcripts, payment slips, and URLs as evidence.",
            ]
        elif level == ConcernLevel.MODERATE_CONCERN:
            safe_next_steps = [
                "Request the official statutory registration certificate and confirm it directly on regulator portals.",
                "Cross-check whether the domain name is listed in the registered broker or intermediary's official directory profile.",
                "Refuse any demands for advance clearance fees or withdrawal charges.",
            ]
        else:
            safe_next_steps = [
                "Practice standard due diligence before transacting.",
                "Confirm that payment beneficiary names match the officially incorporated business name.",
            ]

        return Assessment(
            assessment_id=assessment_id,
            overall_level=level,
            summary=summary,
            risk_signals=signals,
            evidence_count=ev_summary.total_evidence_count,
            verified_claim_count=ev_summary.verified_claims,
            unverified_claim_count=ev_summary.unverified_claims,
            contradictory_claim_count=ev_summary.contradictory_claims,
            unknown_claim_count=ev_summary.unknown_claims,
            uncertainty_notes=uncertainty_notes,
            safe_next_steps=safe_next_steps,
            generated_at=now_iso,
        )
