# RakshaScan — Product Specification

> **SANGYAN 2026 Hackathon Prototype**  
> *Evidence-Based Financial Scam and Trust-Verification Platform*

---

## 1. Problem Statement

Financial fraud and investment scams in India and globally have evolved into sophisticated, multi-stage industrial operations:
1. **Regulatory Impersonation**: Fraudulent entities fabricate registration certificates (e.g., claiming registration with SEBI, RBI, MCA, or international regulators like FCA).
2. **Disconnected Trust Vectors**: A legitimate business name is often juxtaposed with an unrelated newly-registered domain, a fake APK download link, an unauthorized Telegram group, or a mule UPI/bank account.
3. **Binary Failure of Existing Scanners**: Traditional antivirus or link scanners return uninformative "Safe" or "Dangerous" badges. If a domain was created 48 hours ago, traditional blocklists report it as "clean", giving victims a false sense of security.
4. **Lack of Actionable Redirection**: When users suspect fraud, they rarely receive concrete, evidence-backed steps on how to independently confirm claims through official channels or safeguard their assets.

---

## 2. Target Users

- **Retail Investors & Consumers**: Everyday citizens encountering high-yield investment schemes, IPO share allocation groups, forex trading apps, or loan offerings on WhatsApp, Telegram, Instagram, or SMS.
- **Vulnerable Demographics & First-Time Digital Users**: Individuals targeted by fake financial advisors or high-pressure deposit requests.
- **Cybercrime Responders & Fact-Checkers**: Analysts and investigators seeking rapid, standardized, evidence-backed dossiers cross-referencing claims against institutional realities.

---

## 3. Product Goals & Non-Goals

### Product Goals
- **Objective Verification**: Shift from opaque "AI opinion" to explicit, verifiable evidence chains.
- **Multi-Vector Ingestion**: Allow users to inspect URLs, screenshot evidence, chat snippets, corporate names, or payment handles.
- **Institutional Alignment**: Benchmark claims against legitimate regulatory databases (MCA, SEBI, RBI) and infrastructure records (DNS, SSL, WHOIS, ASN).
- **Explainable Trust Degradation**: Show the exact link in the chain where legitimacy breaks down (e.g., "Company name is valid, but the website domain was registered 3 days ago in another jurisdiction").
- **Prescriptive Next Steps**: Provide context-specific, safe defensive protocols for every detected risk level.

### Non-Goals
- **Not a Black-Box Oracle**: RakshaScan does not output a simplistic single-word verdict ("SAFE" / "SCAM") that asks users for blind faith.
- **Not a Law-Enforcement Substitute**: The platform provides evidence dossiers; it does not issue binding judicial determinations.
- **Not an Active Penetration Tool**: RakshaScan analyzes public metadata, claims, and verified registries; it never attacks, exploits, or actively engages with suspicious infrastructure.
- **AI is Not the Arbiter**: AI models do not decide truth; they parse and summarize. Truth is determined by authoritative verification logic.

---

## 4. Core User Journey

1. **Submission**: User inputs a financial artifact (URL, raw text message, or screenshot of an offer/chat).
2. **Parsing & Entity Extraction (AI Layer)**: System extracts purported entities, license numbers, promised returns, URLs, phone numbers, and payment handles.
3. **Deterministic Verification (Verification Layer)**: Backend queries authoritative databases, performs DNS/WHOIS audits, inspects domain age, checks SSL certificates, and searches official regulatory directories.
4. **Trust Chain Resolution**: Entities and infrastructure are linked into a structured dependency chain.
5. **Scam Journey Mapping**: Identified behavioral stages are mapped against documented fraud lifecycles.
6. **Dossier Presentation**: The user receives an interactive **Evidence-Based Assessment Dashboard** detailing verified facts, unverified assertions, contradictions, and safe next steps.

---

## 5. Core Features

### 5.0. Feature 0: Structured Intelligence & Evidence Layer (Phase 3 Foundation)

Before authoritative verification (Phase 4) can occur, raw webpage observations must be converted into traceable, structured intelligence representations.

#### The Core Principle: Extraction ≠ Verification
- **Observed Signal**: Text, claims, or regulatory badges present on a target webpage.
- **Verification**: Cross-checking with authoritative registries (SEBI, MCA, RBI) to confirm legal existence, active licensing, and identity alignment.
- **Initial Verification Status**: Every extracted claim, reference, and relationship carries `verification_status: "UNKNOWN"`.
- **Severity ≠ Fraud**: Severity on financial claims reflects the linguistic intensity of promises or urgency, not a determination of fraud.

#### Structured Intelligence Objects:
1. **`Entity`**:
   - Types: `COMPANY`, `PERSON`, `ORGANIZATION`, `DOMAIN`, `UNKNOWN`.
   - Captures contextual evidence and extraction source.
2. **`Claim`**:
   - Types: `REGULATORY`, `FINANCIAL`, `IDENTITY`, `AUTHORIZATION`, `OTHER`.
   - Links the claim to a `subject_entity_id`, `referenced_authority`, `registration_reference`, and source evidence.
3. **`RegulatoryReference`**:
   - Identifies mentions of regulatory bodies (`SEBI`, `RBI`, `MCA`, `NSE`, `BSE`, `IRDAI`, `PFRDA`, `GOVERNMENT`).
   - Links nearby registration numbers (e.g., `INA000099999`, CIN, GSTIN) via spatial context proximity.
4. **`FinancialClaim`**:
   - 11 deterministic linguistic categories: `GUARANTEED_RETURN`, `RISK_FREE`, `DOUBLE_MONEY`, `HIGH_RETURN`, `FIXED_RETURN`, `URGENCY`, `LIMITED_TIME`, `ACT_NOW`, `DEPOSIT_PRESSURE`, `WITHDRAWAL_FEE`, `ADDITIONAL_PAYMENT`.
   - Severity tags: `LOW`, `MEDIUM`, `HIGH`.
5. **`IdentityRelationship`**:
   - Semantic graph edges: `OPERATES_DOMAIN`, `CLAIMS_AUTHORIZATION`, `REFERENCES_REGISTRATION`, `ASSOCIATED_WITH`, `LINKS_TO_EXTERNAL`.
   - Carries `verification_status: "UNKNOWN"`.
6. **`Evidence`**:
   - Foundation of the **Claim → Evidence → Source** chain: captures `evidence_id`, `source_type`, `source_url`, `extracted_text`, `context`, and `extraction_method`.

---

### 5.0.1. Feature 0.1: Authoritative Verification Subsystem (Phase 4 Foundation)

Transforms selected extracted claims from `UNKNOWN` into evidence-backed verification states when authoritative data is actually available.

#### Core Verification Mandate:
*"Verification results are only authoritative when derived from the identified authoritative source."*

#### Distinct Verification States:
- **`VERIFIED`**: Authoritative source provides positive evidence substantiating the claim.
- **`CONTRADICTORY`**: Authoritative source provides evidence inconsistent with the claim (e.g. registration belongs to a different legal entity).
- **`NOT_FOUND`**: Authoritative source was queried, but entity/registration was not found (`NOT_FOUND` ≠ Fraud).
- **`UNKNOWN`**: Insufficient information exists to query (e.g. general regulator mention without license number; `UNKNOWN` ≠ Safe).
- **`UNAVAILABLE`**: Authoritative source is unreachable or requires interactive human/CAPTCHA sessions (`UNAVAILABLE` ≠ Not Found).

#### Non-Fabrication & Security Rules:
- **Demo Mode**: Synthetically tested via `DemoVerificationAdapter` on fictional fixtures (`INA000099999`). Clearly tagged `is_demo: true` and labeled `[DEMO VERIFICATION]`.
- **Real Regulators**: When official public OpenAPI endpoints are absent, adapters report `UNAVAILABLE` rather than executing brittle unauthenticated scrapers or CAPTCHA bypasses.
- **Provenance Guaranteed**: Every verification result records `source_name`, `source_url`, `checked_at`, `verification_method`, `evidence`, and objective non-prejudicial `reason`.

---

### 5.0.2. Feature 0.2: Evidence-Backed Risk Assessment Subsystem (Phase 5)

Transforms extracted claims, verbatim evidence records, and verification states into an explainable, evidence-backed assessment without arbitrary numerical scoring.

#### Guiding Mandate:
> **"RakshaScan produces evidence-backed concern assessments, not fraud verdicts."**
> A risk signal without supporting evidence is invalid. The system never proclaims "This is a scam" based on keyword detection.

#### Assessment Concern Levels:
1. **`INSUFFICIENT_EVIDENCE`**: Insufficient observed textual content or evidence items (< 2 records) to formulate a reliable assessment.
2. **`LOW_CONCERN`**: No high-severity signals observed; at most minor low-risk observations with no regulatory contradictions.
3. **`MODERATE_CONCERN`**: Multiple medium-severity signals, unverified regulatory assertions, or unconfirmed license numbers.
4. **`HIGH_CONCERN`**: One or more high-severity regulatory/identity contradictions or multiple independent high-severity financial/manipulation claims.

#### 10 Deterministic Risk Rules:
- **Rule 1 (Guaranteed Return)**: `GUARANTEED_RETURN` → `FINANCIAL`, `HIGH`.
- **Rule 2 (Risk-Free Language)**: `RISK_FREE` → `FINANCIAL`, `HIGH`.
- **Rule 3 (Double-Money Language)**: `DOUBLE_MONEY` → `FINANCIAL`, `HIGH`.
- **Rule 4 (Deposit Pressure)**: `DEPOSIT_PRESSURE` → `MANIPULATION`, `HIGH`.
- **Rule 5 (Withdrawal Fee / Extra Payment)**: `WITHDRAWAL_FEE` / `ADDITIONAL_PAYMENT` → `FINANCIAL`, `HIGH`.
- **Rule 6 (Urgency / Act Now)**: `URGENCY` / `ACT_NOW` → `MANIPULATION`, `MEDIUM`.
- **Rule 7 (Regulatory Claim Requiring Verification)**: Claim with status `UNKNOWN` or `UNAVAILABLE` → `REGULATORY`, `MEDIUM` (does not declare claim false).
- **Rule 8 (Regulatory Contradiction)**: Claim with status `CONTRADICTORY` → `REGULATORY`, `HIGH` (states factual mismatch).
- **Rule 9 (Registration Not Found)**: Verification status `NOT_FOUND` → `REGULATORY`, `MEDIUM` (explicitly notes that *not found does not by itself establish fraud*).
- **Rule 10 (Entity Identity Mismatch)**: Registration belongs to a different entity → `IDENTITY`, `HIGH`.

#### Signal Deduplication:
- Redundant occurrences of matching linguistic patterns (e.g. multiple guaranteed return phrases) are consolidated into a single primary signal.
- Full traceability is preserved: union of all supporting `evidence_ids` and `claim_ids` is retained.

#### Epistemic Boundaries & Uncertainty:
- The assessment explicitly surfaces epistemic boundaries: `NOT_FOUND ≠ FRAUD`, `UNKNOWN ≠ SAFE`, `UNAVAILABLE ≠ NOT_FOUND`.
- Provides tailored, actionable Safe Next Steps (SEBI portal checks, consulting certified professionals) rather than aggressive or irreversible directives.

---

### 5.1. Feature A: The Financial Trust Chain

The cornerstone of RakshaScan is the **Financial Trust Chain**. Legitimate financial operations maintain an unbroken, verifiable link from their marketing claims down to their payment processing infrastructure:

```
[ Claim ]
    │
    ▼
[ Entity ]
    │
    ▼
[ Registration / Regulatory License ]
    │
    ▼
[ Official Identity ]
    │
    ▼
[ Official Website ]
    │
    ▼
[ Official Mobile App ]
    │
    ▼
[ Verified Social Account / Channel ]
    │
    ▼
[ Payment Identity (UPI / Bank Account) ]
```

#### Trust Chain Architecture & Data Model:
- **Core Principle**: *"Trust Chain relationships are established only when supported by available evidence."*
- **8 Node Tiers**: `CLAIM`, `ENTITY`, `REGISTRATION`, `OFFICIAL_IDENTITY`, `WEBSITE`, `APP`, `SOCIAL_ACCOUNT`, `PAYMENT_IDENTITY`.
- **Node & Relationship Statuses**:
  - **`VERIFIED`**: Independently substantiated by authoritative institutional records or cryptographic proof (e.g., domain matches official SEBI-registered broker directory).
  - **`UNVERIFIED`**: Claimed on-page, but no independent public or regulatory record could confirm it.
  - **`CONTRADICTORY`**: Explicit mismatch detected between the claim and reality (e.g., claimed registration number belongs to a different legal entity). Contradiction is reported explicitly without applying non-evidentiary "SCAM" labels.
  - **`UNKNOWN`**: Insufficient data available to evaluate the node without further evidence.
  - **`NOT_OBSERVED`**: Checked during analysis, but no supporting evidence was observed on the public website.
  - **`UNAVAILABLE`**: Directory lookup was temporarily unreachable or restricted.
- **Strict Status Non-Propagation**: Node statuses do not cascade across independent relationships (e.g., `REGISTRATION = VERIFIED` does not automatically verify `WEBSITE`).
- **Dynamic Graph Summary**: Summarizes total relationships, verified, unverified, contradictory, unknown, and unobserved counts computed strictly from the active graph.

---

### 5.2. Feature B: Scam Journey Reconstruction

Scams typically adhere to predictable social-engineering progressions. RakshaScan reconstructs the user's encounter as a **reconstructed interaction pattern based on available evidence**:

> **Mandatory Principle**: *"Scam Journey Reconstruction represents a possible/reconstructed interaction pattern and is not a determination of fraud."*

```
[ 01 INITIAL_CONTACT ]
      │ (Unsolicited promotional outreach / urgency pressure cues)
      ▼
[ 02 FINANCIAL_CLAIM ]
      │ (Guaranteed returns / risk-free promises / capital doubling)
      ▼
[ 03 WEBSITE ]
      │ (Public platform presenting branding, personas, and plans)
      ▼
[ 04 COMMUNICATION_CHANNEL ]
      │ (Private phone desks, direct hotlines, WhatsApp / Telegram channels)
      ▼
[ 05 DEPOSIT_REQUEST ]
      │ (Immediate capital mandates, priority settlement desks, quota locking)
      ▼
[ 06 WITHDRAWAL_ISSUE ]
        (Advance tax clearance fees, margin maintenance preconditions)
```

#### Stage Statuses:
- **`OBSERVED`**: Explicit concrete textual or contact signal evidence detected on the page.
- **`SUSPECTED`**: Inferred from linguistic urgency cues or high-pressure allocations characteristic of outbound targeting.
- **`NOT_OBSERVED`**: Checked during analysis, but no matching linguistic patterns or clauses were present.
- **`UNKNOWN`**: External vector not visible in standalone public webpage analysis (e.g., private outbound chat DMs).

#### Journey Reconstruction Confidence (LOW / MEDIUM / HIGH):
- Confidence reflects **how strongly the available evidence supports reconstruction of the analytical model**, NOT a probability of fraud.
- `HIGH` confidence means 4 or more stages are supported by observed/suspected signals.

#### Mandatory Disclaimer:
Prominently displayed verbatim across all API payloads and visual components:
> *"This represents a reconstructed pattern, not a determination that a specific case is fraudulent."*


---

### 5.3. Feature C: The 7-Point Evidence-Based Assessment

Instead of a generic risk score, every RakshaScan report answers seven critical questions:

| # | Assessment Section | Content & Function |
|---|---|---|
| **1** | **What Was Detected** | Plain-language inventory of all extracted entities, promises (e.g., "10% daily guaranteed returns"), registration numbers, contact handles, and domains. |
| **2** | **What Could Be Independently Verified** | Claims directly matching official records (e.g., "Domain registered in 2021", "CIN matches an active entity on MCA"). |
| **3** | **What Could Not Be Verified** | Assertions lacking independent substantiation (e.g., "Claims SEBI registered investment adviser RIA-09876, but no record exists on sebi.gov.in"). |
| **4** | **What Appears Contradictory** | Explicit red-flag conflicts (e.g., claiming to be 'HDFC Securities' but collecting funds via a personal Gmail-hosted UPI VPA). |
| **5** | **Why a Warning Was Raised** | Transparent, non-technical explanation of underlying heuristics and regulatory rules triggered. |
| **6** | **Supporting Evidence Dossier** | Timestamps, raw registry responses, WHOIS registration ages, DNS records, and visual snapshots. |
| **7** | **Appropriate Safe Next Steps** | Actionable defensive protocol customized to the severity and context of the analysis. |

---

### 5.4. Feature D: Multi-Input Ingestion (Phase 8)

Expands verification capabilities from standalone URLs to ubiquitous real-world attack vectors:

1. **User-Submitted Chat & Message Ingestion**:
   - Accepts copied messages from WhatsApp, Telegram, SMS, email, and social networks up to 15,000 characters.
   - Extracts entities, regulatory assertions, financial claims, and urgency cues.
   - Emits evidence records tagged with `source_type: "USER_SUBMITTED_MESSAGE"`.
2. **Screenshot & Visual OCR Ingestion**:
   - Accepts PNG, JPEG, and WEBP screenshot artifacts up to 10MB and 8000x8000 pixels.
   - 100% offline local optical character recognition via in-memory buffers (`io.BytesIO`).
   - Zero disk persistence, zero permanent database storage, zero cloud vision transmission.
   - Emits evidence records tagged with `source_type: "SCREENSHOT_OCR"` and preserves OCR uncertainty notices.
3. **Structured Non-Crawling URL Discovery**:
   - Detects URLs embedded in text messages or OCR transcripts.
   - Formats URLs as structured `links` for display and evidence association.
   - Strictly refuses automated recursive crawling to avoid DoS amplification and uncontrolled SSRF traversal.
4. **Single Unified Intelligence Pipeline**:
   - All input modes normalize into `NormalizedAnalysisInput` and execute the identical structured extraction, verification, risk assessment, Trust Chain, and Scam Journey engines.

---

### 5.5. Feature E: Safe Response & Recovery System (Phase 9)

Extends analysis output from *"What did we find?"* to *"What should the user safely do next?"*:

1. **Action States (Not Fraud Verdicts)**:
   - `SAFE_TO_CONTINUE_WITH_VERIFICATION`: Low concern baseline.
   - `PAUSE_AND_VERIFY`: Moderate concern, unverified credentials, or high return promises.
   - `HIGH_CAUTION`: Significant conflicting evidence, deposit pressure, or impersonation signals.
   - `POST_INCIDENT_GUIDANCE`: Withdrawal fee friction, advance fee demands, or user-declared payment.
   - `INSUFFICIENT_EVIDENCE`: Gaps prevent safe evaluation.
2. **Context-Aware Deterministic Recommendations**:
   - Every recommendation (`PAUSE`, `VERIFY`, `DO_NOT_SEND_ADDITIONAL_MONEY`, `DO_NOT_SHARE_CREDENTIALS`, `PRESERVE_EVIDENCE`, `CONTACT_BANK_OR_PAYMENT_PROVIDER`, `REPORT`) includes an actionable title, plain-language explanation, deterministic reason, and linked evidence/verification IDs.
3. **Structured Post-Incident Recovery Protocols**:
   - **Stop Further Money Transfers**: Refuse demands for release fees, processing taxes, or unlock deposits.
   - **Preserve Documentation**: Retain unedited screenshots, payment handles, and bank reference IDs (UTR/RRN). Strictly forbids saving passwords, PINs, or OTPs.
   - **Contact Financial Provider**: Directs victim to official bank/app customer support within the golden hour.
   - **Report via Official Channels**: National Cyber Crime Reporting Portal (`cybercrime.gov.in`) or helpline `1930`.
   - **Account Security**: Step-by-step password and UPI PIN resets from clean, independent devices.
4. **User Interactive Control**:
   - User-declared facts (*"Have you already transferred money?"*, *"Have you shared sensitive credentials?"*) dynamically activate tailored recovery guidance without backend database persistence.
5. **Incident Timeline**:
   - Reconstructs observed submission milestones and user declarations with zero unevidenced events.

---

### 5.6. Feature F: Bharat-First Multilingual Experience (Phase 10)

Empowers non-English speaking citizens across India with accessible, vernacular safety guidance:

1. **Trilingual Localization**:
   - Native language support for **English (`en`)**, **Hindi (`hi`)**, and **Marathi (`mr`)**.
   - Instant, client-side language switching without re-triggering analysis or altering underlying intelligence data.
2. **Plain-Language Mode ("Simple explanation")**:
   - One-click toggle transforming dense statutory terminology into accessible explanations without loss of nuance.
3. **Regional Language Safety & Epistemic Boundaries**:
   - Translates with strict preservation of uncertainty (e.g. *"यह दावा स्वतंत्र रूप से सत्यापित नहीं किया जा सका"* rather than *"यह फर्जी है"*).
   - Regulatory license codes, CINs, URLs, phone numbers, payment handles, and evidence IDs remain untouched and exact across all languages.

---

### 5.7. Feature G: Production Hardening & Abuse Defense (Phase 11)

Protects system resources, preserves user privacy, and standardizes production operational controls:

1. **In-Process Sliding Window Rate Limiting**:
   - Throttles requests by client IP across independent buckets (`url`: 30/min, `message`: 30/min, `screenshot`: 15/min).
   - Emits HTTP 429 with standard `Retry-After` headers.
2. **Strict Request Boundary Enforcement**:
   - Enforces maximum sizing bounds (URL: 2048 chars, Message: 15,000 chars, Image: 10MB/8000px) returning HTTP 413.
   - Enforces file magic header signatures (`PNG`, `JPEG`, `WEBP`) to block polyglots.
3. **Defensive Response Headers**:
   - `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-XSS-Protection: 1; mode=block`.
4. **Zero-Retention Telemetry**:
   - Privacy-sanitizing operational logger redacts authentication parameters (`token`, `auth`, `password`, `key`) from URLs and completely excludes user content/transcripts from logs.

---

## 6. Safe Next-Step Guidance Matrix

When risks or unverified links are identified, RakshaScan provides context-specific defensive playbooks:

- **Verification Protocol**: Direct links to official regulatory lookup tools (e.g., SEBI Recognized Intermediaries Portal, RBI Kehta Hai directory, MCA Company Master Data).
- **Asset Protection Measures**: Explicit instructions *never* to transfer funds to personal UPI handles or download third-party `.apk` packages.
- **Reporting Channels**: Pre-formatted incident summaries ready to copy-paste into the National Cyber Crime Reporting Portal (`cybercrime.gov.in`) or report via helpline `1930`.
- **Communication Containment**: Instructions on securing compromised messaging accounts and preserving chat logs as evidence.

---

## 7. Demo vs Production Specification

- **Current Prototype State**: Operates against synthetic fixtures (`DemoVerificationAdapter`). Every claim verification outcome is explicitly flagged with `is_demo: true` and labeled in the user interface as *"Demonstration verification source — not a live statutory lookup"*.
- **No Unauthorized Scrapers**: RakshaScan does not perform brittle or unauthorized screen-scraping against CAPTCHA-guarded government portals (SEBI, RBI, MCA).
- **Production Integration**: Future production environments will connect to official statutory registry APIs via authenticated, read-only connector adapters.



