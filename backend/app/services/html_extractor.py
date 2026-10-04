"""Structured HTML extraction engine for RakshaScan Phase 2 & Phase 3.

Extracts visible text, metadata, links, contact signals, and builds structured:
- Entities (Company, Person, Organization, Domain)
- Regulatory References & Associated Registrations
- Financial Claims with linguistic severity classification
- Generalized Claims
- Identity Relationships
- Traceable Evidence records

CORE PRINCIPLE: Extraction is NOT verification.
All verification statuses default to 'UNKNOWN'.
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

from app.schemas.analysis import (
    ClaimModel,
    ContactSignalsModel,
    DetectedReferencesModel,
    EntityEvidence,
    EntityModel,
    EvidenceModel,
    ExtractedSignalModel,
    FinancialClaimModel,
    IdentityRelationshipModel,
    LinkItemModel,
    PageModel,
    RegulatoryReferenceModel,
)

# =========================================================================
# PHASE 2 & 3 PATTERNS & DICTIONARIES
# =========================================================================

FINANCIAL_CLAIM_CATEGORIES: Dict[str, Dict] = {
    "GUARANTEED_RETURN": {
        "phrases": [
            "guaranteed returns",
            "guaranteed return",
            "guaranteed investment opportunity",
            "guaranteed investment",
            "guaranteed profit",
            "guaranteed monthly return",
            "guaranteed annual return",
            "assured returns",
            "assured return",
            "assured profit",
            "guaranteed payout",
            "guaranteed income",
            "guaranteed earnings",
        ],
        "severity": "HIGH",
    },
    "RISK_FREE": {
        "phrases": [
            "risk-free investment",
            "risk free investment",
            "risk-free",
            "risk free",
            "zero risk",
            "no risk",
            "100% principal protection",
            "principal protection",
            "capital guarantee",
            "capital protection",
            "safe and secure investment",
        ],
        "severity": "HIGH",
    },
    "DOUBLE_MONEY": {
        "phrases": [
            "double your money",
            "double your investment",
            "2x return",
            "2x profit",
            "multiply capital",
            "triple your investment",
        ],
        "severity": "HIGH",
    },
    "HIGH_RETURN": {
        "phrases": [
            "20% monthly",
            "25% monthly",
            "30% monthly",
            "35% monthly",
            "40% monthly",
            "50% monthly",
            "300% annual",
            "abnormal profit",
            "high yield",
            "extraordinary returns",
            "daily return",
            "daily profit",
        ],
        "severity": "HIGH",
    },
    "FIXED_RETURN": {
        "phrases": [
            "fixed returns",
            "fixed return",
            "fixed monthly payout",
            "fixed daily interest",
            "fixed interest",
        ],
        "severity": "MEDIUM",
    },
    "URGENCY": {
        "phrases": [
            "urgent",
            "act now",
            "hurry",
            "last chance",
            "fast action required",
            "limited slots",
            "quota filling fast",
            "slots remaining",
            "seats left",
            "slots left",
        ],
        "severity": "MEDIUM",
    },
    "LIMITED_TIME": {
        "phrases": [
            "limited time",
            "limited period",
            "expires today",
            "valid for 24 hours",
            "exclusive window",
            "limited opportunity",
        ],
        "severity": "MEDIUM",
    },
    "ACT_NOW": {
        "phrases": [
            "act now",
            "claim now",
            "join immediately",
            "start earning today",
            "invest today",
        ],
        "severity": "MEDIUM",
    },
    "DEPOSIT_PRESSURE": {
        "phrases": [
            "deposit immediately",
            "deposit today",
            "deposit to activate",
            "deposit now",
            "send capital to",
            "send capital",
            "transfer to upi",
            "initial deposit required",
            "minimum deposit to unlock",
            "send money to claim quota",
            "fund account now",
            "pay to upi",
        ],
        "severity": "HIGH",
    },
    "WITHDRAWAL_FEE": {
        "phrases": [
            "refundable processing tax",
            "refundable tax payment",
            "refundable tax",
            "processing tax",
            "tax payment to withdraw",
            "withdrawal tax",
            "tax clearance fee",
            "fee to release funds",
            "unlock withdrawal",
            "processing charge to withdraw",
            "pay 20% regulatory tax",
            "withdrawal fee",
            "clearance deposit",
        ],
        "severity": "HIGH",
    },
    "ADDITIONAL_PAYMENT": {
        "phrases": [
            "additional fee required",
            "recharge wallet to unfreeze",
            "margin call payment",
            "top up to withdraw",
            "additional payment",
        ],
        "severity": "HIGH",
    },
}

# Legacy flat lists for Phase 2 backward compatibility
FINANCIAL_CLAIM_PHRASES = [
    phrase
    for category in FINANCIAL_CLAIM_CATEGORIES.values()
    for phrase in category["phrases"]
]

REGULATORY_AUTHORITY_PATTERNS = [
    ("SEBI", "Securities and Exchange Board of India", r"\b(?:sebi|securities and exchange board of india)\b"),
    ("RBI", "Reserve Bank of India", r"\b(?:rbi|reserve bank of india)\b"),
    ("MCA", "Ministry of Corporate Affairs", r"\b(?:mca|ministry of corporate affairs)\b"),
    ("NSE", "National Stock Exchange", r"\b(?:nse|national stock exchange)\b"),
    ("BSE", "Bombay Stock Exchange", r"\b(?:bse|bombay stock exchange)\b"),
    ("IRDAI", "Insurance Regulatory and Development Authority", r"\b(?:irdai|irda)\b"),
    ("PFRDA", "Pension Fund Regulatory and Development Authority", r"\b(?:pfrda)\b"),
    ("GOVERNMENT", "Government Authority", r"\b(?:government approved|govt approved|state authorized)\b"),
]

REGULATORY_PHRASES = [
    "sebi registered",
    "sebi approved",
    "government approved",
    "authorized",
    "licensed",
    "sebi",
    "rbi",
    "mca",
    "irdai",
    "amfi",
    "iso certified",
]

# Registration number formats
REG_PATTERNS = [
    (r"\bIN[A-Z]\d{8,9}\b", "SEBI Registration Number Format", "SEBI"),
    (r"\b[UL]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}\b", "MCA CIN Format", "MCA"),
    (r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}\b", "GSTIN Format", "GSTN"),
]

# Contact info patterns
EMAIL_REGEX = re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")
PHONE_REGEX = re.compile(r"(?:\+91[\s.-]?)?[6-9]\d{4}[\s.-]?\d{5}\b")

# Corporate entity patterns (Indian company law and standard suffixes)
COMPANY_ENTITY_REGEX = re.compile(
    r"\b([A-Z][A-Za-z0-9&.,\s]{1,40}?\s+(?:Private Limited|Pvt\.?\s*Ltd\.?|Limited|Ltd\.?|LLP|Inc\.?|Corp\.?))\b"
)

# Person naming patterns (executive roles or salutations)
PERSON_ENTITY_REGEX = re.compile(
    r"\b(?:(?:Chief Strategist|Managing Director|Director|Founder|CEO|Partner|Analyst)[:\s]+)?((?:Dr\.|Mr\.|Mrs\.|Ms\.)\s+(?:[A-Z]\.?|[A-Z][a-z]+)\s+[A-Z][a-z]+)\b"
)


def extract_context_snippet(full_text: str, start_idx: int, end_idx: int, window: int = 60) -> str:
    """Extract a small snippet of text surrounding the match."""
    left = max(0, start_idx - window)
    right = min(len(full_text), end_idx + window)
    snippet = full_text[left:right].strip().replace("\n", " ")
    return f"...{snippet}..." if left > 0 or right < len(full_text) else snippet


def clean_entity_name(raw_name: str) -> str:
    """Clean company names from leading noise."""
    cleaned = re.sub(r"^(?:Welcome to|About|Contact|Discover|Join|Our|The)\s+", "", raw_name.strip(), flags=re.I)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" ,.-")


# =========================================================================
# PHASE 2 BASE EXTRACTION (PRESERVED FOR BACKWARD COMPATIBILITY)
# =========================================================================

def extract_html_information(
    html_content: str, base_url: str
) -> Tuple[PageModel, List[LinkItemModel], ContactSignalsModel, DetectedReferencesModel]:
    """Parse HTML and extract metadata, clean text, links, and Phase 2 signals.

    Preserves exact 4-tuple signature for backward compatibility.
    """
    (
        page_data,
        links,
        contact_signals,
        detected_references,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = extract_comprehensive_analysis(html_content, base_url)
    return page_data, links, contact_signals, detected_references


# =========================================================================
# PHASE 3 STRUCTURED INTELLIGENCE PIPELINE
# =========================================================================

def extract_comprehensive_analysis(
    html_content: str,
    base_url: str = "",
    default_source_type: str = "PAGE_TEXT",
    input_type: str = "URL",
) -> Tuple[
    PageModel,
    List[LinkItemModel],
    ContactSignalsModel,
    DetectedReferencesModel,
    List[EntityModel],
    List[ClaimModel],
    List[RegulatoryReferenceModel],
    List[FinancialClaimModel],
    List[IdentityRelationshipModel],
    List[EvidenceModel],
]:
    """Comprehensive extraction pipeline providing Phase 2 base signals AND Phase 3 structured intelligence."""
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Page Metadata
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    elif input_type == "MESSAGE":
        title = "User Submitted Financial Message"
    elif input_type == "SCREENSHOT":
        title = "User Submitted Screenshot OCR Text"
    else:
        title = None

    meta_desc = None
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if not desc_tag:
        desc_tag = soup.find("meta", attrs={"property": re.compile(r"^og:description$", re.I)})
    if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"].strip()

    html_tag = soup.find("html")
    language = html_tag.get("lang", "").strip() if html_tag and html_tag.get("lang") else None

    canonical_url = None
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    if canonical_tag and canonical_tag.get("href"):
        canonical_url = urljoin(base_url, canonical_tag["href"].strip())

    headings: List[str] = []
    for h in soup.find_all(["h1", "h2", "h3"], limit=15):
        h_text = h.get_text(strip=True)
        if h_text and len(h_text) < 200:
            headings.append(h_text)

    # 2. Extract Visible Text (decompose head and non-visual tags)
    for tag in soup(["head", "script", "style", "noscript", "svg", "canvas", "iframe"]):
        tag.decompose()

    body_text = soup.get_text(separator=" ", strip=True)
    normalized_body = re.sub(r"\s+", " ", body_text)
    text_excerpt = normalized_body[:1000] if normalized_body else None

    # 3. Links
    links: List[LinkItemModel] = []
    seen_urls: Set[str] = set()
    base_parts = urlsplit(base_url)
    base_domain = base_parts.hostname or ""

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href or href.startswith(("#", "javascript:", "data:")):
            continue

        resolved_url = urljoin(base_url, href)
        if resolved_url in seen_urls:
            continue
        seen_urls.add(resolved_url)

        link_text = a_tag.get_text(strip=True) or href
        link_parts = urlsplit(resolved_url)
        is_internal = bool(
            link_parts.hostname
            and (
                link_parts.hostname == base_domain
                or link_parts.hostname.endswith(f".{base_domain}")
            )
        )

        links.append(
            LinkItemModel(
                url=resolved_url,
                text=link_text[:120],
                internal=is_internal,
            )
        )
        if len(links) >= 50:
            break

    # Discover raw text URLs (for messages, chat snippets, or OCR text)
    raw_url_regex = re.compile(r"https?://[a-zA-Z0-9.-]+(?::\d+)?(?:/[^\s<>\"]*)?", re.I)
    for m in raw_url_regex.finditer(normalized_body):
        raw_u = m.group(0).rstrip(".,;:)\"'!?")
        if raw_u not in seen_urls:
            seen_urls.add(raw_u)
            link_parts = urlsplit(raw_u)
            is_internal = bool(
                base_domain
                and link_parts.hostname
                and (
                    link_parts.hostname == base_domain
                    or link_parts.hostname.endswith(f".{base_domain}")
                )
            )
            links.append(
                LinkItemModel(
                    url=raw_u,
                    text=raw_u[:120],
                    internal=is_internal,
                )
            )
            if len(links) >= 50:
                break

    # 4. Contact Signals
    emails: Set[str] = set()
    for a_tag in soup.find_all("a", href=re.compile(r"^mailto:", re.I)):
        mail_target = a_tag["href"].split(":", 1)[1].split("?")[0].strip().lower()
        if mail_target and EMAIL_REGEX.match(mail_target):
            emails.add(mail_target)

    for match in EMAIL_REGEX.finditer(normalized_body):
        emails.add(match.group(0).lower())

    phone_numbers: Set[str] = set()
    for a_tag in soup.find_all("a", href=re.compile(r"^tel:", re.I)):
        tel_target = a_tag["href"].split(":", 1)[1].strip()
        if tel_target:
            phone_numbers.add(tel_target)

    for match in PHONE_REGEX.finditer(normalized_body):
        cleaned_phone = match.group(0).strip()
        phone_numbers.add(cleaned_phone)

    contact_signals = ContactSignalsModel(
        emails=sorted(list(emails)),
        phone_numbers=sorted(list(phone_numbers)),
    )

    # 5. Evidence Registry & Structured Collections
    evidence_list: List[EvidenceModel] = []
    evidence_counter = 0

    def add_evidence(
        source_type: str, extracted_text: str, context: str, method: str
    ) -> str:
        nonlocal evidence_counter
        evidence_counter += 1
        ev_id = f"ev-{evidence_counter}"
        # Propagate custom source_type for user-submitted message or screenshot OCR
        actual_source_type = (
            default_source_type
            if default_source_type != "PAGE_TEXT" and source_type in ("PAGE_TEXT", "METADATA", "CONTACT", "LINK")
            else source_type
        )
        evidence_list.append(
            EvidenceModel(
                id=ev_id,
                source_type=actual_source_type,
                source_url=base_url,
                extracted_text=extracted_text,
                context=context,
                extraction_method=method,
            )
        )
        return ev_id

    # Register top-level source evidence object if message or screenshot OCR
    if default_source_type == "SCREENSHOT_OCR":
        add_evidence(
            "SCREENSHOT_OCR",
            normalized_body[:500] if normalized_body else "Submitted screenshot",
            "Optical text extracted from user submitted screenshot using local OCR",
            "LOCAL_OCR_EXTRACTION",
        )
    elif default_source_type == "USER_SUBMITTED_MESSAGE":
        add_evidence(
            "USER_SUBMITTED_MESSAGE",
            normalized_body[:500] if normalized_body else "Submitted message",
            "Full text content of user submitted message",
            "MESSAGE_SUBMISSION",
        )

    # ---------------------------------------------------------------------
    # Phase 3: Registration Code Detection
    # ---------------------------------------------------------------------
    extracted_reg_codes: List[Tuple[str, str, str, int, int]] = []
    # (code, label, authority, start, end)
    for pattern_str, label, auth in REG_PATTERNS:
        pattern = re.compile(pattern_str)
        for match in pattern.finditer(normalized_body):
            code = match.group(0)
            extracted_reg_codes.append((code, label, auth, match.start(), match.end()))

    # ---------------------------------------------------------------------
    # Phase 3: Entity Extraction
    # ---------------------------------------------------------------------
    entities_list: List[EntityModel] = []
    seen_entity_names: Set[str] = set()
    entity_counter = 0

    # Domain Entity
    if base_domain:
        entity_counter += 1
        dom_ev_id = add_evidence(
            "METADATA",
            base_domain,
            f"Normalized target domain from input URL: {base_url}",
            "DOMAIN_EXTRACTION",
        )
        entities_list.append(
            EntityModel(
                id=f"ent-{entity_counter}",
                name=base_domain,
                entity_type="DOMAIN",
                source="metadata",
                evidence=EntityEvidence(
                    text=base_domain,
                    context=f"Operating domain: {base_domain}",
                ),
                evidence_id=dom_ev_id,
            )
        )

    # Company Entities
    for match in COMPANY_ENTITY_REGEX.finditer(normalized_body):
        raw_company = match.group(1).strip()
        cleaned_company = clean_entity_name(raw_company)
        if len(cleaned_company) >= 4 and cleaned_company.lower() not in seen_entity_names:
            seen_entity_names.add(cleaned_company.lower())
            entity_counter += 1
            ctx = extract_context_snippet(normalized_body, match.start(), match.end())
            ev_id = add_evidence("PAGE_TEXT", cleaned_company, ctx, "COMPANY_PATTERN")
            entities_list.append(
                EntityModel(
                    id=f"ent-{entity_counter}",
                    name=cleaned_company,
                    entity_type="COMPANY",
                    source="page_text",
                    evidence=EntityEvidence(
                        text=cleaned_company,
                        context=ctx,
                    ),
                    evidence_id=ev_id,
                )
            )

    # Person Entities (e.g. Dr. R. Sharma)
    for match in PERSON_ENTITY_REGEX.finditer(normalized_body):
        person_name = match.group(1).strip()
        if person_name.lower() not in seen_entity_names and len(person_name) > 4:
            seen_entity_names.add(person_name.lower())
            entity_counter += 1
            ctx = extract_context_snippet(normalized_body, match.start(), match.end())
            ev_id = add_evidence("PAGE_TEXT", person_name, ctx, "PERSON_PATTERN")
            entities_list.append(
                EntityModel(
                    id=f"ent-{entity_counter}",
                    name=person_name,
                    entity_type="PERSON",
                    source="page_text",
                    evidence=EntityEvidence(
                        text=person_name,
                        context=ctx,
                    ),
                    evidence_id=ev_id,
                )
            )

    # ---------------------------------------------------------------------
    # Phase 3: Regulatory References & Registration Association
    # ---------------------------------------------------------------------
    regulatory_refs: List[RegulatoryReferenceModel] = []
    reg_counter = 0

    for auth_code, auth_name, pattern_str in REGULATORY_AUTHORITY_PATTERNS:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        for match in pattern.finditer(normalized_body):
            reg_counter += 1
            m_start, m_end = match.start(), match.end()
            ctx = extract_context_snippet(normalized_body, m_start, m_end, window=90)
            raw_text = match.group(0)

            # Determine claim_type from surrounding window
            local_window = normalized_body[max(0, m_start - 70) : min(len(normalized_body), m_end + 70)].lower()
            if "registered" in local_window or "registration" in local_window:
                claim_type = "REGISTERED"
            elif "approved" in local_window:
                claim_type = "APPROVED"
            elif "licensed" in local_window or "license" in local_window:
                claim_type = "LICENSED"
            elif "authorized" in local_window or "authorisation" in local_window:
                claim_type = "AUTHORIZED"
            else:
                claim_type = "REGULATORY_MENTION"

            # Associate nearby registration number if present within 140 chars
            associated_reg: Optional[str] = None
            for reg_code, _, reg_auth, r_start, r_end in extracted_reg_codes:
                if abs(m_start - r_start) <= 140:
                    associated_reg = reg_code
                    break

            ev_id = add_evidence("PAGE_TEXT", raw_text, ctx, "REGULATORY_PATTERN")
            regulatory_refs.append(
                RegulatoryReferenceModel(
                    id=f"reg-{reg_counter}",
                    authority=auth_code,
                    claim_type=claim_type,
                    registration_number=associated_reg,
                    raw_text=raw_text,
                    context=ctx,
                    verification_status="UNKNOWN",
                    evidence_id=ev_id,
                )
            )

    # Deduplicate regulatory references by authority and registration_number
    unique_reg_refs: List[RegulatoryReferenceModel] = []
    seen_reg_keys = set()
    for r in regulatory_refs:
        key = (r.authority, r.claim_type, r.registration_number)
        if key not in seen_reg_keys:
            seen_reg_keys.add(key)
            unique_reg_refs.append(r)

    # ---------------------------------------------------------------------
    # Phase 3: Financial Claim Classification
    # ---------------------------------------------------------------------
    financial_claims: List[FinancialClaimModel] = []
    fin_counter = 0
    seen_fin_phrases = set()

    for category_name, cat_info in FINANCIAL_CLAIM_CATEGORIES.items():
        for phrase in cat_info["phrases"]:
            p_pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
            for match in p_pattern.finditer(normalized_body):
                matched_phrase = match.group(0)
                key = (category_name, matched_phrase.lower())
                if key in seen_fin_phrases:
                    continue
                seen_fin_phrases.add(key)

                fin_counter += 1
                ctx = extract_context_snippet(normalized_body, match.start(), match.end())
                ev_id = add_evidence("PAGE_TEXT", matched_phrase, ctx, "FINANCIAL_PATTERN")

                financial_claims.append(
                    FinancialClaimModel(
                        id=f"fin-{fin_counter}",
                        claim_text=matched_phrase,
                        claim_type=category_name,
                        severity=cat_info["severity"],
                        evidence_text=matched_phrase,
                        context=ctx,
                        verification_status="UNKNOWN",
                        evidence_id=ev_id,
                    )
                )

    # Dynamic regex matching for deposit pressure with specific amounts
    deposit_amount_regex = re.compile(
        r"\bdeposit\s+(?:(?:₹|rs\.?|inr|\$)\s*)?\d+[,\d]*\s+(?:today|immediately|now|to\s+activate)",
        re.IGNORECASE,
    )
    for m in deposit_amount_regex.finditer(normalized_body):
        matched_str = m.group(0)
        key = ("DEPOSIT_PRESSURE", matched_str.lower())
        if key not in seen_fin_phrases:
            seen_fin_phrases.add(key)
            fin_counter += 1
            ctx = extract_context_snippet(normalized_body, m.start(), m.end(), window=80)
            ev_id = add_evidence("PAGE_TEXT", matched_str, ctx, "FINANCIAL_DEPOSIT_PATTERN")
            financial_claims.append(
                FinancialClaimModel(
                    id=f"fin-{fin_counter}",
                    claim_text=matched_str,
                    claim_type="DEPOSIT_PRESSURE",
                    severity="HIGH",
                    evidence_text=matched_str,
                    context=ctx,
                    verification_status="UNKNOWN",
                    evidence_id=ev_id,
                )
            )

    # ---------------------------------------------------------------------
    # Phase 3: Claims Construction (Generalized Claims)
    # ---------------------------------------------------------------------
    claims_list: List[ClaimModel] = []
    claim_counter = 0

    primary_company_id = next(
        (e.id for e in entities_list if e.entity_type == "COMPANY"),
        None,
    )

    # Synthesize regulatory claims
    for reg in unique_reg_refs:
        claim_counter += 1
        claim_text = (
            f"Claims {reg.authority} {reg.claim_type.lower()}"
            + (f" under License No. {reg.registration_number}" if reg.registration_number else "")
        )
        claims_list.append(
            ClaimModel(
                id=f"clm-{claim_counter}",
                claim_text=claim_text,
                claim_type="REGULATORY",
                subject_entity_id=primary_company_id,
                referenced_authority=reg.authority,
                registration_reference=reg.registration_number,
                source="page_text",
                evidence_text=reg.raw_text,
                verification_status="UNKNOWN",
                evidence_id=reg.evidence_id,
            )
        )

    # Synthesize financial claims (high severity claims)
    for fin in financial_claims:
        if fin.severity == "HIGH":
            claim_counter += 1
            claims_list.append(
                ClaimModel(
                    id=f"clm-{claim_counter}",
                    claim_text=f"Promotes {fin.claim_type.replace('_', ' ').lower()}: '{fin.claim_text}'",
                    claim_type="FINANCIAL",
                    subject_entity_id=primary_company_id,
                    referenced_authority=None,
                    registration_reference=None,
                    source="page_text",
                    evidence_text=fin.evidence_text,
                    verification_status="UNKNOWN",
                    evidence_id=fin.evidence_id,
                )
            )

    # ---------------------------------------------------------------------
    # Phase 3: Identity Relationships
    # ---------------------------------------------------------------------
    relationships_list: List[IdentityRelationshipModel] = []
    rel_counter = 0

    company_entity = next((e for e in entities_list if e.entity_type == "COMPANY"), None)
    domain_entity = next((e for e in entities_list if e.entity_type == "DOMAIN"), None)
    person_entities = [e for e in entities_list if e.entity_type == "PERSON"]

    # 1. Company -> Operates -> Domain
    if company_entity and domain_entity:
        rel_counter += 1
        relationships_list.append(
            IdentityRelationshipModel(
                id=f"rel-{rel_counter}",
                source_entity_id=company_entity.id,
                relationship_type="OPERATES_DOMAIN",
                target_id_or_value=domain_entity.name,
                description=f"Entity '{company_entity.name}' appears to operate domain '{domain_entity.name}'",
                verification_status="UNKNOWN",
                evidence_id=company_entity.evidence_id,
            )
        )

    # 2. Company -> Claims Authorization -> Regulatory Authority
    for reg in unique_reg_refs:
        if company_entity:
            rel_counter += 1
            relationships_list.append(
                IdentityRelationshipModel(
                    id=f"rel-{rel_counter}",
                    source_entity_id=company_entity.id,
                    relationship_type="CLAIMS_AUTHORIZATION",
                    target_id_or_value=f"{reg.authority} ({reg.claim_type})",
                    description=f"Entity '{company_entity.name}' claims {reg.authority} {reg.claim_type.lower()}",
                    verification_status="UNKNOWN",
                    evidence_id=reg.evidence_id,
                )
            )

    # 3. Company -> References Registration -> Registration Number
    for reg in unique_reg_refs:
        if company_entity and reg.registration_number:
            rel_counter += 1
            relationships_list.append(
                IdentityRelationshipModel(
                    id=f"rel-{rel_counter}",
                    source_entity_id=company_entity.id,
                    relationship_type="REFERENCES_REGISTRATION",
                    target_id_or_value=reg.registration_number,
                    description=f"Entity '{company_entity.name}' references regulatory identifier '{reg.registration_number}'",
                    verification_status="UNKNOWN",
                    evidence_id=reg.evidence_id,
                )
            )

    # 4. Person -> Associated With -> Company
    for person in person_entities:
        if company_entity:
            rel_counter += 1
            relationships_list.append(
                IdentityRelationshipModel(
                    id=f"rel-{rel_counter}",
                    source_entity_id=person.id,
                    relationship_type="ASSOCIATED_WITH",
                    target_id_or_value=company_entity.name,
                    description=f"Person '{person.name}' identified as key person or executive of '{company_entity.name}'",
                    verification_status="UNKNOWN",
                    evidence_id=person.evidence_id,
                )
            )

    # 5. Domain -> Links To -> External Domains
    external_domains_seen = set()
    for link in links:
        if not link.internal:
            link_host = urlsplit(link.url).hostname
            if link_host and link_host not in external_domains_seen:
                external_domains_seen.add(link_host)
                rel_counter += 1
                link_ev_id = add_evidence(
                    "LINK",
                    link.url,
                    f"Outbound link with anchor '{link.text}' to external host {link_host}",
                    "LINK_EXTRACTION",
                )
                relationships_list.append(
                    IdentityRelationshipModel(
                        id=f"rel-{rel_counter}",
                        source_entity_id=domain_entity.name if domain_entity else base_domain,
                        relationship_type="LINKS_TO_EXTERNAL",
                        target_id_or_value=link_host,
                        description=f"Domain links externally to '{link_host}' ({link.url})",
                        verification_status="UNKNOWN",
                        evidence_id=link_ev_id,
                    )
                )

    # ---------------------------------------------------------------------
    # Phase 2 Detected References Adapter (Preserved)
    # ---------------------------------------------------------------------
    phase2_entities = [
        ExtractedSignalModel(
            phrase=e.name,
            category="entity",
            source=e.source,
            context=e.evidence.context,
        )
        for e in entities_list
        if e.entity_type == "COMPANY"
    ]

    phase2_reg_numbers = [
        ExtractedSignalModel(
            phrase=code,
            category="registration_number",
            source="page_text",
            context=f"[{label}] {extract_context_snippet(normalized_body, start, end)}",
        )
        for code, label, _, start, end in extracted_reg_codes
    ]

    phase2_reg_mentions: List[ExtractedSignalModel] = []
    seen_p2_reg = set()
    for phrase in REGULATORY_PHRASES:
        pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
        for match in pattern.finditer(normalized_body):
            matched = match.group(0)
            if matched.lower() not in seen_p2_reg:
                seen_p2_reg.add(matched.lower())
                phase2_reg_mentions.append(
                    ExtractedSignalModel(
                        phrase=matched,
                        category="regulatory_mention",
                        source="page_text",
                        context=extract_context_snippet(normalized_body, match.start(), match.end()),
                    )
                )

    phase2_fin_claims = [
        ExtractedSignalModel(
            phrase=f.claim_text,
            category="financial_claim",
            source="page_text",
            context=f.context,
        )
        for f in financial_claims
    ]

    detected_references = DetectedReferencesModel(
        entities=phase2_entities,
        registration_numbers=phase2_reg_numbers,
        regulatory_mentions=phase2_reg_mentions,
        financial_claims=phase2_fin_claims,
    )

    page_data = PageModel(
        title=title,
        description=meta_desc,
        language=language,
        canonical_url=canonical_url,
        headings=headings,
        text_excerpt=text_excerpt,
    )

    return (
        page_data,
        links,
        contact_signals,
        detected_references,
        entities_list,
        claims_list,
        unique_reg_refs,
        financial_claims,
        relationships_list,
        evidence_list,
    )
