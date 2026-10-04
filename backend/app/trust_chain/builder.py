"""Trust Chain Builder for RakshaScan Phase 6.

Constructs an evidence-backed Financial Trust Chain representing verifiable identity
relationships without synthetic fabrication or erroneous status propagation.
"""

from typing import Any, Dict, List, Optional
import uuid

from app.trust_chain.models import (
    TrustChainGraph,
    TrustChainNode,
    TrustChainNodeType,
    TrustChainRelationship,
    TrustChainRelationshipType,
    TrustChainStatus,
    TrustChainSummary,
)


class TrustChainBuilder:
    """Builds an evidence-backed Financial Trust Chain graph from structured analysis artifacts."""

    def build_trust_chain(
        self,
        claims: List[Any],
        regulatory_references: List[Any],
        financial_claims: List[Any],
        entities: List[Any],
        verification_results: List[Any],
        evidence: List[Any],
        links: List[Any],
        page_data: Any,
        target_url: str,
        contact_signals: Any,
    ) -> TrustChainGraph:
        """Constructs 8-node Trust Chain and rigorously proven relationships."""
        nodes: List[TrustChainNode] = []
        relationships: List[TrustChainRelationship] = []

        # Index verification results by claim_id and reference_id
        verif_by_cid: Dict[str, Any] = {}
        verif_by_rid: Dict[str, Any] = {}
        for vr in verification_results:
            cid = getattr(vr, "claim_id", None) or (vr.get("claim_id") if isinstance(vr, dict) else None)
            rid = getattr(vr, "reference_id", None) or (vr.get("reference_id") if isinstance(vr, dict) else None)
            if cid:
                verif_by_cid[cid] = vr
            if rid:
                verif_by_rid[rid] = vr

        # -------------------------------------------------------------
        # 1. NODE: CLAIM
        # -------------------------------------------------------------
        claim_node_id = "node-claim"
        primary_claim_text = "No regulatory or financial claims declared"
        claim_status = TrustChainStatus.UNKNOWN
        claim_ev_ids: List[str] = []
        claim_verif_ids: List[str] = []

        if regulatory_references:
            reg_0 = regulatory_references[0]
            primary_claim_text = getattr(reg_0, "raw_text", "") or (reg_0.get("raw_text", "") if isinstance(reg_0, dict) else "")
            ev_id = getattr(reg_0, "evidence_id", None) or (reg_0.get("evidence_id") if isinstance(reg_0, dict) else None)
            if ev_id:
                claim_ev_ids.append(ev_id)
            reg_id = getattr(reg_0, "id", None) or (reg_0.get("id") if isinstance(reg_0, dict) else None)
            vr = verif_by_rid.get(reg_id)
            if vr:
                vr_id = getattr(vr, "id", "") or (vr.get("id", "") if isinstance(vr, dict) else "")
                claim_verif_ids.append(vr_id)
                vr_status = getattr(vr, "status", "") or (vr.get("status", "") if isinstance(vr, dict) else "")
                vr_status_str = getattr(vr_status, "value", str(vr_status)).upper()
                if vr_status_str == "VERIFIED":
                    claim_status = TrustChainStatus.VERIFIED
                elif vr_status_str == "CONTRADICTORY":
                    claim_status = TrustChainStatus.CONTRADICTORY
                elif vr_status_str in ["NOT_FOUND", "UNVERIFIED"]:
                    claim_status = TrustChainStatus.UNVERIFIED
                else:
                    claim_status = TrustChainStatus.UNKNOWN
            else:
                claim_status = TrustChainStatus.UNVERIFIED
        elif claims:
            c_0 = claims[0]
            primary_claim_text = getattr(c_0, "claim_text", "") or (c_0.get("claim_text", "") if isinstance(c_0, dict) else "")
            ev_id = getattr(c_0, "evidence_id", None) or (c_0.get("evidence_id") if isinstance(c_0, dict) else None)
            if ev_id:
                claim_ev_ids.append(ev_id)
            claim_status = TrustChainStatus.UNVERIFIED
        elif financial_claims:
            fc_0 = financial_claims[0]
            primary_claim_text = getattr(fc_0, "claim_text", "") or (fc_0.get("claim_text", "") if isinstance(fc_0, dict) else "")
            ev_id = getattr(fc_0, "evidence_id", None) or (fc_0.get("evidence_id") if isinstance(fc_0, dict) else None)
            if ev_id:
                claim_ev_ids.append(ev_id)
            claim_status = TrustChainStatus.UNVERIFIED

        claim_node = TrustChainNode(
            node_id=claim_node_id,
            node_type=TrustChainNodeType.CLAIM.value,
            label="Claimed Authorization",
            value=primary_claim_text,
            status=claim_status.value,
            evidence_ids=claim_ev_ids,
            verification_ids=claim_verif_ids,
            metadata={"source": "page_text"},
        )
        nodes.append(claim_node)

        # -------------------------------------------------------------
        # 2. NODE: ENTITY
        # -------------------------------------------------------------
        entity_node_id = "node-entity"
        primary_entity_name = "No identified legal entity"
        entity_status = TrustChainStatus.UNKNOWN
        entity_ev_ids: List[str] = []
        entity_id_val: Optional[str] = None

        if entities:
            e_0 = entities[0]
            primary_entity_name = getattr(e_0, "name", "") or (e_0.get("name", "") if isinstance(e_0, dict) else "")
            entity_id_val = getattr(e_0, "id", None) or (e_0.get("id") if isinstance(e_0, dict) else None)
            ev_id = getattr(e_0, "evidence_id", None) or (e_0.get("evidence_id") if isinstance(e_0, dict) else None)
            if ev_id:
                entity_ev_ids.append(ev_id)
            # Entity name alone from page is unverified until corroborated by authoritative identity
            entity_status = TrustChainStatus.UNKNOWN
        else:
            entity_status = TrustChainStatus.NOT_OBSERVED

        entity_node = TrustChainNode(
            node_id=entity_node_id,
            node_type=TrustChainNodeType.ENTITY.value,
            label="Claimed Entity",
            value=primary_entity_name,
            status=entity_status.value,
            evidence_ids=entity_ev_ids,
            verification_ids=[],
            metadata={"entity_id": entity_id_val} if entity_id_val else {},
        )
        nodes.append(entity_node)

        # -------------------------------------------------------------
        # 3. NODE: REGISTRATION
        # -------------------------------------------------------------
        reg_node_id = "node-registration"
        reg_number = "No statutory registration stated"
        reg_status = TrustChainStatus.UNKNOWN
        reg_ev_ids: List[str] = []
        reg_verif_ids: List[str] = []
        matched_auth_entity: Optional[str] = None
        has_reg_claim = False

        if regulatory_references:
            for rr in regulatory_references:
                num = getattr(rr, "registration_number", None) or (rr.get("registration_number") if isinstance(rr, dict) else None)
                if num:
                    reg_number = num
                    has_reg_claim = True
                    ev_id = getattr(rr, "evidence_id", None) or (rr.get("evidence_id") if isinstance(rr, dict) else None)
                    if ev_id:
                        reg_ev_ids.append(ev_id)
                    rid = getattr(rr, "id", None) or (rr.get("id") if isinstance(rr, dict) else None)
                    vr = verif_by_rid.get(rid)
                    if vr:
                        vr_id = getattr(vr, "id", "") or (vr.get("id", "") if isinstance(vr, dict) else "")
                        reg_verif_ids.append(vr_id)
                        v_st = getattr(vr, "status", "") or (vr.get("status", "") if isinstance(vr, dict) else "")
                        v_st_str = getattr(v_st, "value", str(v_st)).upper()
                        matched_auth_entity = getattr(vr, "matched_entity", None) or (vr.get("matched_entity") if isinstance(vr, dict) else None)
                        if v_st_str == "VERIFIED":
                            reg_status = TrustChainStatus.VERIFIED
                        elif v_st_str == "CONTRADICTORY":
                            reg_status = TrustChainStatus.CONTRADICTORY
                        elif v_st_str in ["NOT_FOUND", "UNVERIFIED"]:
                            reg_status = TrustChainStatus.UNVERIFIED
                        elif v_st_str == "UNAVAILABLE":
                            reg_status = TrustChainStatus.UNAVAILABLE
                    else:
                        reg_status = TrustChainStatus.UNVERIFIED
                    break

        if not has_reg_claim:
            reg_status = TrustChainStatus.NOT_OBSERVED

        reg_node = TrustChainNode(
            node_id=reg_node_id,
            node_type=TrustChainNodeType.REGISTRATION.value,
            label="Registration Reference",
            value=reg_number,
            status=reg_status.value,
            evidence_ids=reg_ev_ids,
            verification_ids=reg_verif_ids,
            metadata={"authority": "SEBI/MCA" if has_reg_claim else "NONE"},
        )
        nodes.append(reg_node)

        # -------------------------------------------------------------
        # 4. NODE: OFFICIAL_IDENTITY
        # -------------------------------------------------------------
        official_node_id = "node-official-identity"
        official_identity_val = "Statutory registry identity not established"
        official_status = TrustChainStatus.UNKNOWN
        official_verif_ids = list(reg_verif_ids)

        if matched_auth_entity:
            official_identity_val = matched_auth_entity
            if reg_status == TrustChainStatus.VERIFIED:
                official_status = TrustChainStatus.VERIFIED
            elif reg_status == TrustChainStatus.CONTRADICTORY:
                # Contradiction: Registration belongs to a different entity
                official_status = TrustChainStatus.CONTRADICTORY
            else:
                official_status = TrustChainStatus.UNKNOWN
        elif reg_status == TrustChainStatus.UNVERIFIED:
            official_identity_val = "Record Not Found in Official Directory"
            official_status = TrustChainStatus.UNVERIFIED
        elif not has_reg_claim:
            official_identity_val = "No Registration Asserted"
            official_status = TrustChainStatus.NOT_OBSERVED

        official_node = TrustChainNode(
            node_id=official_node_id,
            node_type=TrustChainNodeType.OFFICIAL_IDENTITY.value,
            label="Official Directory Identity",
            value=official_identity_val,
            status=official_status.value,
            evidence_ids=[],
            verification_ids=official_verif_ids,
            metadata={"matched_entity": matched_auth_entity or "NONE"},
        )
        nodes.append(official_node)

        # -------------------------------------------------------------
        # 5. NODE: WEBSITE
        # -------------------------------------------------------------
        website_node_id = "node-website"
        website_ev_ids: List[str] = []

        if target_url and target_url.startswith(("http://", "https://")):
            website_val = target_url
            website_status = TrustChainStatus.UNVERIFIED
            if evidence:
                website_ev_ids.append(evidence[0].id if hasattr(evidence[0], "id") else evidence[0]["id"])
        elif links:
            website_val = links[0].url
            website_status = TrustChainStatus.UNVERIFIED
            if evidence:
                website_ev_ids.append(evidence[0].id if hasattr(evidence[0], "id") else evidence[0]["id"])
        else:
            website_val = "Not Observed in Submitted Content"
            website_status = TrustChainStatus.NOT_OBSERVED

        website_node = TrustChainNode(
            node_id=website_node_id,
            node_type=TrustChainNodeType.WEBSITE.value,
            label="Observed Website / Domain",
            value=website_val,
            status=website_status.value,
            evidence_ids=website_ev_ids,
            verification_ids=[],
            metadata={"domain_whitelisted": False},
        )
        nodes.append(website_node)

        # -------------------------------------------------------------
        # 6. NODE: APP
        # -------------------------------------------------------------
        app_node_id = "node-app"
        app_links: List[str] = []
        if links:
            for lk in links:
                url_str = getattr(lk, "url", "") or (lk.get("url", "") if isinstance(lk, dict) else "")
                if any(x in url_str.lower() for x in ["play.google.com", "apps.apple.com", ".apk"]):
                    app_links.append(url_str)

        if app_links:
            app_val = app_links[0]
            app_status = TrustChainStatus.UNVERIFIED
            app_ev = website_ev_ids
        else:
            app_val = "No mobile application observed"
            app_status = TrustChainStatus.NOT_OBSERVED
            app_ev = []

        app_node = TrustChainNode(
            node_id=app_node_id,
            node_type=TrustChainNodeType.APP.value,
            label="Mobile Application",
            value=app_val,
            status=app_status.value,
            evidence_ids=app_ev,
            verification_ids=[],
            metadata={"app_links_count": len(app_links)},
        )
        nodes.append(app_node)

        # -------------------------------------------------------------
        # 7. NODE: SOCIAL_ACCOUNT
        # -------------------------------------------------------------
        social_node_id = "node-social"
        social_channels: List[str] = []
        if links:
            for lk in links:
                url_str = getattr(lk, "url", "") or (lk.get("url", "") if isinstance(lk, dict) else "")
                for domain in ["t.me", "telegram.me", "wa.me", "api.whatsapp.com", "twitter.com", "x.com", "instagram.com", "youtube.com"]:
                    if domain in url_str.lower():
                        social_channels.append(url_str)
                        break

        # Check contact signals for phone/whatsapp
        phone_nums = getattr(contact_signals, "phone_numbers", []) or (contact_signals.get("phone_numbers", []) if isinstance(contact_signals, dict) else [])
        if phone_nums:
            social_channels.append(f"Phone/WhatsApp Desk: {phone_nums[0]}")

        if social_channels:
            social_val = social_channels[0]
            social_status = TrustChainStatus.UNVERIFIED
            social_ev = website_ev_ids
        else:
            social_val = "No external social or messaging channels observed"
            social_status = TrustChainStatus.NOT_OBSERVED
            social_ev = []

        social_node = TrustChainNode(
            node_id=social_node_id,
            node_type=TrustChainNodeType.SOCIAL_ACCOUNT.value,
            label="Social / Messaging Account",
            value=social_val,
            status=social_status.value,
            evidence_ids=social_ev,
            verification_ids=[],
            metadata={"channels_count": len(social_channels)},
        )
        nodes.append(social_node)

        # -------------------------------------------------------------
        # 8. NODE: PAYMENT_IDENTITY
        # -------------------------------------------------------------
        payment_node_id = "node-payment"
        # Check financial claims for payment instructions or deposit mentions
        payment_instructions: List[str] = []
        for fc in financial_claims:
            c_type = getattr(fc, "claim_type", "") or (fc.get("claim_type", "") if isinstance(fc, dict) else "")
            c_text = getattr(fc, "claim_text", "") or (fc.get("claim_text", "") if isinstance(fc, dict) else "")
            if c_type in ["DEPOSIT_PRESSURE", "ADDITIONAL_PAYMENT", "WITHDRAWAL_FEE"]:
                payment_instructions.append(c_text)

        payment_ev_ids: List[str] = []
        if payment_instructions:
            payment_val = f"Observed Deposit Instruction: {payment_instructions[0]}"
            payment_status = TrustChainStatus.UNVERIFIED
            # Connect to evidence of that financial claim
            for fc in financial_claims:
                e_id = getattr(fc, "evidence_id", None) or (fc.get("evidence_id") if isinstance(fc, dict) else None)
                if e_id and e_id not in payment_ev_ids:
                    payment_ev_ids.append(e_id)
        else:
            payment_val = "No direct payment identity observed on page"
            payment_status = TrustChainStatus.NOT_OBSERVED

        payment_node = TrustChainNode(
            node_id=payment_node_id,
            node_type=TrustChainNodeType.PAYMENT_IDENTITY.value,
            label="Payment / Settlement Identity",
            value=payment_val,
            status=payment_status.value,
            evidence_ids=payment_ev_ids,
            verification_ids=[],
            metadata={"has_payment_identity": bool(payment_instructions)},
        )
        nodes.append(payment_node)

        # -------------------------------------------------------------
        # RELATIONSHIPS CONSTRUCTION (Rigorously evidence-backed)
        # -------------------------------------------------------------

        # Rel 1: CLAIM -> ENTITY (CLAIMS)
        if entities and (regulatory_references or claims or financial_claims):
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-claim-entity-{uuid.uuid4().hex[:6]}",
                    source_node_id=claim_node_id,
                    target_node_id=entity_node_id,
                    relationship_type=TrustChainRelationshipType.CLAIMS.value,
                    status=TrustChainStatus.UNVERIFIED.value,
                    evidence_ids=claim_ev_ids + entity_ev_ids,
                    verification_ids=[],
                    explanation=f"Page asserts regulatory/financial representations on behalf of entity '{primary_entity_name}'. Corporate attribution remains unverified.",
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-claim-entity-{uuid.uuid4().hex[:6]}",
                    source_node_id=claim_node_id,
                    target_node_id=entity_node_id,
                    relationship_type=TrustChainRelationshipType.CLAIMS.value,
                    status=TrustChainStatus.UNKNOWN.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="Insufficient evidence to associate declared claims with an identified legal entity.",
                )
            )

        # Rel 2: ENTITY -> REGISTRATION (REGISTERED_AS)
        if entities and has_reg_claim:
            rel_status = reg_status.value
            if reg_status == TrustChainStatus.CONTRADICTORY:
                rel_explanation = f"Contradiction: Registration '{reg_number}' is associated with a different entity in official statutory directory."
            elif reg_status == TrustChainStatus.VERIFIED:
                rel_explanation = f"Entity '{primary_entity_name}' is verified under registration '{reg_number}' in official directory."
            elif reg_status == TrustChainStatus.UNVERIFIED:
                rel_explanation = f"Entity '{primary_entity_name}' cites registration '{reg_number}', but record could not be confirmed in regulatory database."
            else:
                rel_explanation = f"Entity registration relationship status is {reg_status.value}."

            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-entity-reg-{uuid.uuid4().hex[:6]}",
                    source_node_id=entity_node_id,
                    target_node_id=reg_node_id,
                    relationship_type=TrustChainRelationshipType.REGISTERED_AS.value,
                    status=rel_status,
                    evidence_ids=entity_ev_ids + reg_ev_ids,
                    verification_ids=reg_verif_ids,
                    explanation=rel_explanation,
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-entity-reg-{uuid.uuid4().hex[:6]}",
                    source_node_id=entity_node_id,
                    target_node_id=reg_node_id,
                    relationship_type=TrustChainRelationshipType.REGISTERED_AS.value,
                    status=TrustChainStatus.NOT_OBSERVED.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="No supporting evidence was observed establishing a statutory registration number for this entity.",
                )
            )

        # Rel 3: REGISTRATION -> OFFICIAL_IDENTITY (IDENTIFIED_AS)
        if has_reg_claim:
            if reg_status == TrustChainStatus.CONTRADICTORY:
                rel_status = TrustChainStatus.CONTRADICTORY.value
                rel_explanation = f"Directory record shows registration '{reg_number}' is legally assigned to '{matched_auth_entity}', not '{primary_entity_name}'."
            elif reg_status == TrustChainStatus.VERIFIED:
                rel_status = TrustChainStatus.VERIFIED.value
                rel_explanation = f"Statutory directory matches registration '{reg_number}' to authorized record '{matched_auth_entity}'."
            elif reg_status == TrustChainStatus.UNVERIFIED:
                rel_status = TrustChainStatus.UNVERIFIED.value
                rel_explanation = f"Registration '{reg_number}' returned no matching record in statutory registry."
            else:
                rel_status = TrustChainStatus.UNKNOWN.value
                rel_explanation = "Unable to determine official regulatory identity."

            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-reg-official-{uuid.uuid4().hex[:6]}",
                    source_node_id=reg_node_id,
                    target_node_id=official_node_id,
                    relationship_type=TrustChainRelationshipType.IDENTIFIED_AS.value,
                    status=rel_status,
                    evidence_ids=reg_ev_ids,
                    verification_ids=reg_verif_ids,
                    explanation=rel_explanation,
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-reg-official-{uuid.uuid4().hex[:6]}",
                    source_node_id=reg_node_id,
                    target_node_id=official_node_id,
                    relationship_type=TrustChainRelationshipType.IDENTIFIED_AS.value,
                    status=TrustChainStatus.NOT_OBSERVED.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="No registration was declared; official statutory identity cannot be looked up.",
                )
            )

        # Rel 4: ENTITY -> WEBSITE (OPERATES)
        # Note: Do not automatically propagate status. Even if registration is verified,
        # website domain is not automatically verified without an authoritative domain whitelist entry.
        if website_status == TrustChainStatus.NOT_OBSERVED:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-entity-website-{uuid.uuid4().hex[:6]}",
                    source_node_id=entity_node_id,
                    target_node_id=website_node_id,
                    relationship_type=TrustChainRelationshipType.OPERATES.value,
                    status=TrustChainStatus.NOT_OBSERVED.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="No website or web portal link was observed in the submitted content.",
                )
            )
        elif entities:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-entity-website-{uuid.uuid4().hex[:6]}",
                    source_node_id=entity_node_id,
                    target_node_id=website_node_id,
                    relationship_type=TrustChainRelationshipType.OPERATES.value,
                    status=TrustChainStatus.UNVERIFIED.value,
                    evidence_ids=entity_ev_ids + website_ev_ids,
                    verification_ids=[],
                    explanation=f"Website claims affiliation with entity '{primary_entity_name}'. The domain is not registered in official regulator directory profiles.",
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-entity-website-{uuid.uuid4().hex[:6]}",
                    source_node_id=entity_node_id,
                    target_node_id=website_node_id,
                    relationship_type=TrustChainRelationshipType.OPERATES.value,
                    status=TrustChainStatus.UNKNOWN.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="Insufficient evidence to associate website domain with a distinct corporate entity.",
                )
            )

        # Rel 5: WEBSITE -> APP (LINKS_TO)
        if app_links:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-website-app-{uuid.uuid4().hex[:6]}",
                    source_node_id=website_node_id,
                    target_node_id=app_node_id,
                    relationship_type=TrustChainRelationshipType.LINKS_TO.value,
                    status=TrustChainStatus.UNVERIFIED.value,
                    evidence_ids=website_ev_ids,
                    verification_ids=[],
                    explanation=f"Website links to external application package '{app_val}'. Application developer credentials remain unverified.",
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-website-app-{uuid.uuid4().hex[:6]}",
                    source_node_id=website_node_id,
                    target_node_id=app_node_id,
                    relationship_type=TrustChainRelationshipType.LINKS_TO.value,
                    status=TrustChainStatus.NOT_OBSERVED.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="No supporting evidence was observed linking this website to a mobile application.",
                )
            )

        # Rel 6: WEBSITE -> SOCIAL_ACCOUNT (ASSOCIATED_WITH)
        if social_channels:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-website-social-{uuid.uuid4().hex[:6]}",
                    source_node_id=website_node_id,
                    target_node_id=social_node_id,
                    relationship_type=TrustChainRelationshipType.ASSOCIATED_WITH.value,
                    status=TrustChainStatus.UNVERIFIED.value,
                    evidence_ids=website_ev_ids,
                    verification_ids=[],
                    explanation=f"Website provides direct communication handles ({social_val}). Group moderation and ownership are unverified.",
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-website-social-{uuid.uuid4().hex[:6]}",
                    source_node_id=website_node_id,
                    target_node_id=social_node_id,
                    relationship_type=TrustChainRelationshipType.ASSOCIATED_WITH.value,
                    status=TrustChainStatus.NOT_OBSERVED.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="No supporting evidence was observed linking this website to external social media or messaging channels.",
                )
            )

        # Rel 7: WEBSITE -> PAYMENT_IDENTITY (RECEIVES_PAYMENT)
        # Never fabricate payment identity links.
        if payment_instructions:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-website-payment-{uuid.uuid4().hex[:6]}",
                    source_node_id=website_node_id,
                    target_node_id=payment_node_id,
                    relationship_type=TrustChainRelationshipType.RECEIVES_PAYMENT.value,
                    status=TrustChainStatus.UNVERIFIED.value,
                    evidence_ids=payment_ev_ids,
                    verification_ids=[],
                    explanation="Webpage contains direct capital deposit instructions. Beneficiary account identity is not established.",
                )
            )
        else:
            relationships.append(
                TrustChainRelationship(
                    relationship_id=f"rel-website-payment-{uuid.uuid4().hex[:6]}",
                    source_node_id=website_node_id,
                    target_node_id=payment_node_id,
                    relationship_type=TrustChainRelationshipType.RECEIVES_PAYMENT.value,
                    status=TrustChainStatus.NOT_OBSERVED.value,
                    evidence_ids=[],
                    verification_ids=[],
                    explanation="No supporting evidence connects this website or entity to an observed payment identity.",
                )
            )

        # -------------------------------------------------------------
        # SUMMARY CALCULATION (Strictly dynamically calculated)
        # -------------------------------------------------------------
        total_rel = len(relationships)
        verified_cnt = sum(1 for r in relationships if r.status == TrustChainStatus.VERIFIED.value)
        unverified_cnt = sum(1 for r in relationships if r.status == TrustChainStatus.UNVERIFIED.value)
        contradictory_cnt = sum(1 for r in relationships if r.status == TrustChainStatus.CONTRADICTORY.value)
        unknown_cnt = sum(1 for r in relationships if r.status == TrustChainStatus.UNKNOWN.value)
        unobserved_cnt = sum(1 for r in relationships if r.status in [TrustChainStatus.NOT_OBSERVED.value, TrustChainStatus.UNAVAILABLE.value])

        summary_text = (
            f"{total_rel} relationships analyzed: {verified_cnt} verified, {unverified_cnt} unverified, "
            f"{contradictory_cnt} contradictory, {unknown_cnt} unknown, {unobserved_cnt} unobserved."
        )

        summary = TrustChainSummary(
            total_nodes=len(nodes),
            total_relationships=total_rel,
            verified_count=verified_cnt,
            unverified_count=unverified_cnt,
            contradictory_count=contradictory_cnt,
            unknown_count=unknown_cnt,
            unobserved_count=unobserved_cnt,
            summary_text=summary_text,
        )

        return TrustChainGraph(
            nodes=nodes,
            relationships=relationships,
            summary=summary,
        )
