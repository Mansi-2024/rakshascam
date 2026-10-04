# RakshaScan 🛡️🔍

> **AI-Powered Financial Scam & Trust-Verification Platform**  
> *Production-Oriented Hackathon Prototype for SANGYAN 2026*

---

## 1. Project Overview

**RakshaScan** is an evidence-based financial scam prevention and trust verification platform. In an era where deepfakes, spoofed regulatory credentials, cloned trading platforms, and coordinated investment syndicates target citizens, RakshaScan provides an adversarial-aware, objective verification engine before users commit money or share sensitive credentials.

Unlike simplistic scanners that generate binary `"SCAM"` or `"SAFE"` labels, RakshaScan produces an **evidence-based assessment** rooted in institutional registries, deterministic cross-validation, and auditable proof chains.

---

## 2. Core Purpose & Philosophy

1. **AI is an Assistant, Not the Source of Truth**:
   - AI models excel at entity extraction, claim parsing, OCR comprehension, and linguistic triage.
   - **Verification authority belongs strictly to deterministic logic and official authoritative records** (e.g., MCA corporate registries, SEBI/RBI lists, verified DNS/WHOIS records, banking identifiers).
2. **Evidence Over Speculation**:
   - Every finding provides reproducible artifacts: timestamps, verified domain records, registration mismatches, and cryptographic or official checks.
3. **Actionable Resilience**:
   - Beyond inspection, RakshaScan guides users with immediate, context-aware safe next steps (e.g., verifying via official regulator portals, blocking payment conduits, filing cybercrime reports).

---

## 3. High-Level Architecture

The platform is designed with a clear separation of concerns across a modern, decoupled stack:

```
[ Frontend: Next.js + TypeScript + Tailwind CSS ]
                       │
                 (REST / JSON API)
                       │
                       ▼
[ Backend API Gateway: FastAPI (Python 3.11+) ]
   │                 │                   │
   ▼                 ▼                   ▼
[ AI Extraction ] [ Verification ]   [ Evidence & Risk Engine ]
  (Claims, OCR,     (Registries,        (Trust Chain Graph,
   Entities)         DNS, SSL)           Scam Journey Engine)
                       │
                       ▼
         [ PostgreSQL Storage Layer ]
```

- **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy/SQLModel.
- **Database**: PostgreSQL with structured JSONB support for evidence trees and graph edges.
- **Analysis Modules (Phased)**: Playwright (sandboxed browser capture), Tesseract/Vision OCR, Domain/DNS analyzers, Official Registry adapters.

---

## 4. Development Phases

RakshaScan follows a structured, milestone-driven roadmap:

| Phase | Focus | Objectives |
| :--- | :--- | :--- |
| **Phase 1: Ingestion & Core Models** *(Complete)* | Frontend Ingestion Shell & UX Baseline | Next.js prototype, multi-mode input card, interactive trust chain visualizer, 7-point evidence dossier preview. |
| **Phase 2: Safe URL Analysis** *(Complete)* | Safe Ingestion & Structured HTML Extraction | FastAPI backend, zero-trust SSRF validation, DNS pre-flight filtering, safe HTTP stream reader, deterministic signal extraction. |
| **Phase 3: Structured Intelligence & Evidence** *(Complete)* | Entity, Claim & Relationship Extraction | Deterministic extraction of Entities, Claims, Regulatory References, Financial Claims (11 categories), Identity Relationships, and anchored Evidence objects (`verification_status: UNKNOWN`). |
| **Phase 4: Authoritative Verification Architecture** *(Complete)* | Verification Subsystem & Statutory Adapters | Modular adapter pipeline; strict states (`VERIFIED`, `CONTRADICTORY`, `NOT_FOUND`, `UNKNOWN`, `UNAVAILABLE`); isolated demo adapters; explicit stubs for live directories. |
| **Phase 5: Evidence-Backed Risk Assessment Engine** *(Complete)* | Unified Evidence & Risk Assessment Subsystem | Combines EvidenceEngine and RiskAssessmentEngine; 10 deterministic risk rules; 4 concern levels (`LOW_CONCERN`, `MODERATE_CONCERN`, `HIGH_CONCERN`, `INSUFFICIENT_EVIDENCE`); signal deduplication; uncertainty notes; no numerical scam score. |
| **Phase 6: The Financial Trust Chain** *(Complete)* | End-to-End Dependency Resolution | 8-node Trust Chain resolution, status resolution (`VERIFIED`, `UNVERIFIED`, `CONTRADICTORY`, `UNKNOWN`, `NOT_OBSERVED`), contradiction highlighting, strict non-propagation rules, dynamic summary. |
| **Phase 7: Scam Journey Behavioral Reconstruction** *(Complete)* | 6-Stage Timeline Mapping & Defensive Playbooks | 6-stage lifecycle reconstruction from observed evidence and risk signals; observed vs suspected distinction; journey confidence (LOW/MEDIUM/HIGH); mandatory non-prejudicial disclaimer. |
| **Phase 8: Multi-Input Ingestion** *(Complete)* | Message & Local Screenshot OCR Ingestion | Normalized input abstraction (`app.ingestion`), safe text validation, local/offline OCR for PNG/JPEG/WEBP screenshots, non-crawling URL extraction, in-memory processing, evidence traceability (`USER_SUBMITTED_MESSAGE`, `SCREENSHOT_OCR`), unified intelligence pipeline execution. |
| **Phase 9: Safe Response & Recovery** *(Complete)* | Evidence-Aware Action Engine & Recovery Protocols | Deterministic Safe Response module (`app.response`), 5 contextual action states, traceable recommendations, 5-stage post-incident recovery drawer, interactive user state toggles (money sent / credentials shared), and evidence-backed incident timeline. |
| **Phase 10: Bharat-First Multilingual UX** *(Complete)* | Trilingual Localization & Plain-Language Mode | Trilingual language architecture supporting English (`en`), Hindi (`hi`), and Marathi (`mr`); prominent language switcher without re-analysis; Plain-Language mode toggle simplifying regulatory jargon while strictly preserving epistemic uncertainty. |
| **Phase 11: Production Hardening** *(Complete)* | Security Hardening, In-Process Rate Limiting & Demo vs Production Distinction | Sliding window rate limiting, request & payload caps (URL 2048 chars, Message 15k chars, Image 10MB/8000px), magic bytes validation, security headers middleware, environment configuration, sanitized logging, and explicit "Demo vs Production" documentation. |
| **Phase 12: Demo & Submission Readiness** *(Complete)* | Freeze, Demonstration Flow, Presentation Guide & Submission Finalization | Code freeze, 3–5 min demo guide ([docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md)), multimodal fictional demo scenarios, final privacy audit, error-path QA, and 125/125 regression tests passing. |





---

## 5. Phase 2 Implementation: Safe URL Analysis

Phase 2 introduces RakshaScan's first live backend capability: a zero-trust, SSRF-hardened FastAPI service that safely ingests target URLs and extracts structured website information without executing client-side scripts.

### 5.1 What the Analyzer DOES:
- **Strict URL Validation**: Enforces `http://` and `https://` schemes; rejects `javascript:`, `file:`, `data:`, `ftp:`, etc.
- **SSRF & DNS Pre-flight Filtering**: Rejects loopback (`127.0.0.0/8`, `::1`), private RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), link-local, carrier-grade NAT, multicast, and cloud metadata (`169.254.169.254`).
- **Resource Constraints**: 3s connect timeout, 7s read timeout, 10s total timeout, max 3 manual redirect hops with re-verification, and 5 MB stream cap.
- **Structured Extraction**: Extracts page title, meta description, language, canonical URL, headings, clean text excerpt, internal/external links, emails, phone numbers, and deterministic mentions of regulatory and financial claims.
- **Explicit Status**: Emits `ANALYSIS COMPLETE` with timestamps and extraction metadata.

### 5.2 What the Analyzer DOES NOT Claim:
- **No Scam or Legitimacy Verdicts**: It does **NOT** declare a website as "SCAM", "SAFE", or "VERIFIED".
- **Extraction is Not Verification**: Finding the phrase "SEBI Registered" merely records that the text was observed; it does **NOT** verify whether the claimed entity holds that registration.
- **No Script Execution**: Does **NOT** execute remote JavaScript, submit forms, or download executable payloads.
- **No Financial Advice**: Does **NOT** provide investment advice or legal opinions.

### 5.3 Backend Quickstart

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Run backend test suite (15 unit tests)
python -m pytest tests -v

# 3. Start FastAPI server on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 5.4 API Endpoint Example

**Request:**
`POST /api/v1/analyze/url`
```json
{
  "url": "https://example-finance.test"
}
```

**Response:**
```json
{
  "input": {
    "url": "https://example-finance.test",
    "normalized_url": "https://example-finance.test/"
  },
  "fetch": {
    "success": true,
    "status_code": 200,
    "content_type": "text/html; charset=utf-8",
    "final_url": "https://example-finance.test/",
    "redirect_hops": 0,
    "response_time_ms": 12.5,
    "error_message": null
  },
  "page": {
    "title": "Example Wealth Advisors | High Yield Investment Opportunities",
    "description": "Exclusive private wealth advisory offering guaranteed returns...",
    "language": "en",
    "canonical_url": "https://example-finance.test",
    "headings": ["Example Wealth Advisors Private Limited", ...],
    "text_excerpt": "..."
  },
  "links": [
    {
      "url": "https://example-finance.test/about",
      "text": "About Us",
      "internal": true
    }
  ],
  "contact_signals": {
    "emails": ["info@example-finance.test"],
    "phone_numbers": ["+91 98765 43210"]
  },
  "detected_references": {
    "entities": [{"phrase": "Example Wealth Advisors Private Limited", "category": "entity", "source": "page_text"}],
    "registration_numbers": [{"phrase": "INA000099999", "category": "registration_number", "source": "page_text"}],
    "regulatory_mentions": [{"phrase": "SEBI registered", "category": "regulatory_mention", "source": "page_text"}],
    "financial_claims": [{"phrase": "guaranteed returns", "category": "financial_claim", "source": "page_text"}]
  },
  "analysis_metadata": {
    "analysis_version": "phase-2",
    "timestamp": "2026-10-03T15:00:00Z",
    "status": "ANALYSIS COMPLETE",
    "notice": "Extraction is informational only. Extracted signals do NOT constitute verification or legal determination."
  }
}
```

---

## 6. Phase 3 Implementation: Structured Intelligence & Evidence Layer

Phase 3 transforms raw extracted webpage signals into structured, typed intelligence objects ready for downstream verification.

### 6.1 Core Principle: Extraction ≠ Verification
- **Every claim, reference, and relationship carries `verification_status: "UNKNOWN"`**.
- Finding "SEBI registered" means: **REGULATORY CLAIM DETECTED**; it does **NOT** mean SEBI VERIFIED.
- The UI explicitly displays **OBSERVED** and **Verification: UNKNOWN**.
- Severity ratings on financial phrases reflect linguistic risk characteristics, not a fraud verdict.

### 6.2 Structured Intelligence Models
1. **`Entity`**: Detects structured entities with associated evidence:
   - `COMPANY`: Corporate suffixes (`Private Limited`, `LLP`, `Limited`, etc.).
   - `PERSON`: Formal titles and executive roles (`Dr. R. Sharma`, etc.).
   - `DOMAIN`: Host domain anchor.
2. **`Claim`**: Anchors assertions (`REGULATORY`, `FINANCIAL`, `IDENTITY`, `AUTHORIZATION`) with subject entity IDs and authority links.
3. **`RegulatoryReference`**: Maps regulator mentions (`SEBI`, `RBI`, `MCA`, `NSE`, `BSE`, `IRDAI`, `PFRDA`) and associates proximate registration numbers (`INA000099999`, CIN, GSTIN).
4. **`FinancialClaim`**: Deterministically classifies 11 financial language patterns:
   - `GUARANTEED_RETURN`, `RISK_FREE`, `DOUBLE_MONEY`, `HIGH_RETURN`, `FIXED_RETURN`
   - `URGENCY`, `LIMITED_TIME`, `ACT_NOW`
   - `DEPOSIT_PRESSURE`, `WITHDRAWAL_FEE`, `ADDITIONAL_PAYMENT`
5. **`IdentityRelationship`**: Maps relationships between entities, domains, and regulatory registrations (`OPERATES_DOMAIN`, `CLAIMS_AUTHORIZATION`, `REFERENCES_REGISTRATION`, `ASSOCIATED_WITH`, `LINKS_TO_EXTERNAL`).
6. **`Evidence`**: Foundational `Claim → Evidence → Source` traceability model capturing `evidence_id`, `source_type`, `source_url`, `extracted_text`, `context`, and `extraction_method`.

### 6.3 Test Suite & Verification
The backend test suite includes 27 comprehensive tests:
- 15 Phase 2 tests (SSRF, URL validation, stream limits, redirects, Phase 2 HTML extraction).
- 12 Phase 3 tests (entity extraction, regulatory reference association, 11 financial claim types, claim construction, evidence anchoring, identity relationships, unknown verification status).

```bash
# Run all 27 unit tests
python -m pytest backend/tests -v
```

---

## 7. Phase 4 Implementation: Authoritative Verification Architecture

Phase 4 introduces the modular verification subsystem that transforms extracted claims from `UNKNOWN` into evidence-backed verification states when authoritative data is available.

> **Critical Mandate**: *"Verification results are only authoritative when derived from the identified authoritative source."*

### 7.1 Verification States
The platform rigorously distinguishes five objective verification states:
- **`VERIFIED`**: Authoritative source provides active evidence supporting the claim.
- **`CONTRADICTORY`**: Authoritative source was queried, but contains records inconsistent with the claim (e.g. registration assigned to a different entity).
- **`NOT_FOUND`**: The authoritative source was successfully queried, but the claimed entity/registration could not be found. *(NOT_FOUND must NOT automatically mean FRAUD).*
- **`UNKNOWN`**: Insufficient information exists to determine the result (e.g. general regulator mention without a specific license number). *(UNKNOWN must NOT mean SAFE).*
- **`UNAVAILABLE`**: The authoritative source could not be reached, timed out, or requires interactive human/CAPTCHA sessions. *(UNAVAILABLE must NOT mean NOT_FOUND).*

### 7.2 Modular Verification Adapters
- **`VerificationAdapter`**: Abstract base interface defining `can_verify(item)` and `verify(item, context)`.
- **`DemoVerificationAdapter`**: Operates strictly on synthetic, fictional test data (e.g., `INA000099999` and `Example Wealth Advisors Private Limited`). All results are explicitly marked with `is_demo: true` and labeled `[DEMO VERIFICATION]`.
- **`SebiRegistryAdapter` & `McaRegistryAdapter`**: Explicit stubs reporting `UNAVAILABLE` because official portals require interactive CAPTCHA, viewstates, or restricted enterprise API credentials. RakshaScan strictly refuses to blindly scrape, bypass CAPTCHA, or fabricate regulator confirmations.

### 7.3 Provenance & Non-Prejudicial Explanations
Every `VerificationResult` guarantees complete provenance:
- `source_name` & `source_url`
- `checked_at` (ISO 8601 UTC timestamp)
- `verification_method`
- `matched_entity` & `matched_registration`
- `evidence` (concrete excerpt from registry record)
- `reason` (objective explanation; never proclaims "this is a scam")
- `is_demo` (boolean flag)

### 7.4 Test Suite & Verification
The backend test suite includes 60 comprehensive unit tests:
- 15 Phase 2 tests (SSRF, URL validation, stream limits, redirects, HTML extraction).
- 12 Phase 3 tests (entity extraction, regulatory reference association, 11 financial claim types, claim construction, evidence anchoring, identity relationships).
- 11 Phase 4 tests (demo verified, demo contradictory, demo not-found, unknown on missing ID, unavailable on failure, exact registration normalization, entity mismatch, contradictory registration ownership, provenance preservation, original claim preservation, exception isolation).
- 22 Phase 5 tests (evidence creation/provenance/preservation, 10 deterministic risk rules, signal deduplication, 4 assessment concern levels, uncertainty preservation, no numerical scam scores, no fraud declarations).

```bash
# Run all 60 unit tests
python -m pytest backend/tests -v
```

---

## 8. Phase 5 Implementation: Evidence-Backed Risk Assessment Engine

Phase 5 unifies the **Evidence Engine** and **Risk Assessment Engine** into a deterministic, transparent assessment subsystem.

> **Core Principle**: *"RakshaScan produces evidence-backed concern assessments, not fraud verdicts."*  
> The platform never proclaims "This is a scam" or outputs an arbitrary numerical scam score. Every signal is anchored to observed text, evidence IDs, and verification provenance.

### 8.1 Architecture (`backend/app/evidence/` & `backend/app/risk/`)
- **`EvidenceEngine`**: Manages immutable `EvidenceRecord` objects, maintains claim/entity cross-indexing, and generates quantitative audit summaries (`total_evidence_count`, `verified_claims`, `contradictory_claims`, `unverified_claims`, `unknown_claims`).
- **`RiskAssessmentEngine`**: Evaluates 10 deterministic risk rules, deduplicates signals, and synthesizes explainable concern levels.

### 8.2 The 10 Deterministic Risk Rules
1. **Rule 1 (Guaranteed Return)**: Triggers `FINANCIAL / HIGH` on promised yields (e.g., "18% guaranteed return monthly").
2. **Rule 2 (Risk-Free Language)**: Triggers `FINANCIAL / HIGH` on zero-risk / capital protection claims.
3. **Rule 3 (Double-Money Language)**: Triggers `FINANCIAL / HIGH` on rapid capital multiplication phrasing.
4. **Rule 4 (Deposit Pressure)**: Triggers `MANIPULATION / HIGH` on immediate funding thresholds or coercive countdowns.
5. **Rule 5 (Withdrawal Fee / Advance Payment)**: Triggers `FINANCIAL / HIGH` on demands for advance tax/margin payments to release balances.
6. **Rule 6 (Urgency / Act Now)**: Triggers `MANIPULATION / MEDIUM` on artificial scarcity or limited-slot pressure.
7. **Rule 7 (Regulatory Claim Requiring Verification)**: Triggers `REGULATORY / MEDIUM` when statutory authorization is unverified. *(Explicitly notes: unverified does NOT mean false).*
8. **Rule 8 (Regulatory Contradiction)**: Triggers `REGULATORY / HIGH` when verification contradicts claimed ownership. *(Explains the factual mismatch objectively without stating "this is a scam").*
9. **Rule 9 (Registration Not Found)**: Triggers `REGULATORY / MEDIUM` when official query yields zero records. *(Explicitly states: NOT_FOUND does not by itself establish fraud).*
10. **Rule 10 (Identity Mismatch)**: Triggers `IDENTITY / HIGH` when an active registration belongs to a completely different legal entity.

### 8.3 Explainable Concern Levels
- **`HIGH_CONCERN`**: Triggered by 1+ high-severity regulatory/identity contradictions or 2+ independent high-severity financial/manipulation signals.
- **`MODERATE_CONCERN`**: Triggered by unverified statutory claims, urgency pressure, or isolated financial promises requiring third-party validation.
- **`LOW_CONCERN`**: Triggered when public content shows standard business descriptions without high-risk promises or contradictions.
- **`INSUFFICIENT_EVIDENCE`**: Triggered when the page contains minimal parseable financial content or retrieval was unsuccessful.

---

## 10. Phase 6 Implementation: The Financial Trust Chain

Phase 6 introduces RakshaScan's first signature product feature: the **Financial Trust Chain** (`backend/app/trust_chain/`).

> **Mandatory Rule**: *"Trust Chain relationships are established only when supported by available evidence."*  
> The system represents what is known from structured analysis artifacts; it **never invents missing links** or manufactures fictitious connections.

### 10.1 The 8-Node Core Chain
The Trust Chain traces identity dependencies along the sequence:
```
Claim ──▶ Entity ──▶ Registration ──▶ Official Identity ──▶ Website ──▶ App ──▶ Social Account ──▶ Payment Identity
```

### 10.2 Node & Relationship Statuses
1. **`VERIFIED`**: Substantiated by authoritative institutional directory records or cryptographic matching.
2. **`UNVERIFIED`**: Claimed on-page or linked, but third-party confirmation is pending or absent.
3. **`CONTRADICTORY`**: Explicit conflict between claimed values and authoritative records (e.g., claimed registration number is officially assigned to a different legal entity).
4. **`UNKNOWN`**: Insufficient evidence observed to determine the relationship.
5. **`NOT_OBSERVED`**: Vector was checked during ingestion, but no supporting evidence was observed on the public website.
6. **`UNAVAILABLE`**: Directory lookup was temporarily unreachable or restricted.

### 10.3 Strict Status Non-Propagation Rule
Statuses do **NOT** automatically cascade across unrelated nodes:
- `REGISTRATION = VERIFIED` does **NOT** make `WEBSITE = VERIFIED`.
- `WEBSITE = VERIFIED` does **NOT** make `ENTITY = VERIFIED`.
Every node and relationship maintains its own distinct provenance, `evidence_ids`, and `verification_ids`.

### 10.4 Contradiction Reporting Without Prejudicial Labelling
When an authoritative discrepancy is confirmed, the Trust Chain explicitly reports:
`CONTRADICTORY: Registration is associated with a different entity in official directory records.`  
The system **never labels the entity "SCAM"**; it reports the factual contradiction objectively.

---

## 11. Phase 7 Implementation: Scam Journey Reconstruction

Phase 7 introduces RakshaScan's second signature feature: **Scam Journey Reconstruction** (`backend/app/journey/`).

> **Mandatory Statement**: *"Scam Journey Reconstruction represents a possible/reconstructed interaction pattern and is not a determination of fraud."*

### 11.1 The 6-Stage Behavioral Reconstruction Lifecycle
1. **`01 INITIAL_CONTACT`**: Unsolicited promotional outreach, sponsored ads, cold calls, or artificial urgency cues.
2. **`02 FINANCIAL_CLAIM`**: Contractual profit guarantees, zero-risk assertions, or rapid capital doubling promises.
3. **`03 WEBSITE`**: Public landing platform hosting corporate personas, testimonials, and marketing claims.
4. **`04 COMMUNICATION_CHANNEL`**: Direct off-platform communication vectors (hotlines, email desks, WhatsApp/Telegram links).
5. **`05 DEPOSIT_REQUEST`**: Direct mandates urging immediate capital transfers, institutional settlement desk deposits, or quota locking.
6. **`06 WITHDRAWAL_ISSUE`**: Prerequisites demanding upfront tax clearance fees or additional margin deposits before funds are released.

### 11.2 Stage Statuses: Observed vs. Suspected vs. Unknown
- **`OBSERVED`**: Explicit concrete textual or contact signal evidence detected on the page (e.g., deposit mandate text, contact phone numbers).
- **`SUSPECTED`**: Inferred from linguistic urgency cues or high-pressure allocations characteristic of outbound targeting.
- **`NOT_OBSERVED`**: Verified to have zero matching linguistic patterns or clauses on the page.
- **`UNKNOWN`**: External vector not visible in standalone public webpage analysis (e.g., private outbound chat DMs).

### 11.3 Journey Confidence vs. Fraud Probability
- **Journey Confidence** (`LOW`, `MEDIUM`, `HIGH`) measures **how strongly the available evidence supports reconstruction of the interaction pattern**.
- `HIGH` journey reconstruction confidence **does NOT mean a high probability of fraud**; it denotes evidence completeness in matching an analytical behavioral model.

### 11.4 Prominent Mandatory Disclaimer
Displayed verbatim in the backend model and prominently on the user interface:
> *"This represents a reconstructed pattern, not a determination that a specific case is fraudulent."*

---

## 12. Phase 8 Implementation: Multi-Input Ingestion

Phase 8 expands RakshaScan beyond URL-only inspection into a comprehensive multi-input platform supporting:
1. **User-Submitted Financial Message & Chat Text** (`POST /api/v1/analyze/message`)
2. **Uploaded Screenshot / Image OCR** (`POST /api/v1/analyze/screenshot`)
3. **Safe Website URL Analysis** (`POST /api/v1/analyze/url`)

### 12.1 The Unified Intelligence Pipeline
Rather than fragmenting analysis across separate pipelines, all input modes feed through a **single shared intelligence pipeline**:

```
[ Website URL ] ───────▶ Safe Fetch (SSRF-hardened) ─┐
[ Copied Message ] ────▶ Normalization & Validation ──┼─▶ [ NormalizedAnalysisInput ]
[ Screenshot OCR ] ────▶ Local In-Memory OCR ─────────┘               │
                                                                       ▼
                                                          Structured Extraction
                                                                       ▼
                                                          Statutory Verification
                                                                       ▼
                                                          Evidence Engine & Risk Assessment
                                                                       ▼
                                                          Financial Trust Chain
                                                                       ▼
                                                          Scam Journey Reconstruction
                                                                       ▼
                                                          Unified Analysis Response
```

### 12.2 Message Ingestion Rules & Safe Normalization
- Enforces a 15,000 character maximum limit and rejects empty/whitespace submissions.
- Safely strips dangerous non-printable ASCII control characters without altering substantive financial terms.
- Detects raw URLs and stores them as structured links without automated recursive crawling.
- Emits evidence records with `source_type = "USER_SUBMITTED_MESSAGE"` for full provenance.

### 12.3 Screenshot OCR & Privacy-by-Design
- **100% Local / Offline Processing**: Never sends images to cloud vision or third-party OCR services.
- **In-Memory Processing**: Operates entirely within RAM (`io.BytesIO`); zero disk writes, zero database storage of uploaded screenshot images.
- **File Validation**: Enforces a 10MB file size limit, 8000x8000 pixel dimensions cap, and restricts formats to PNG, JPEG, and WEBP.
- **Explicit OCR Uncertainty**: Exposes explicit disclaimer notices:
  > *"Text extracted from the screenshot may contain OCR errors or omissions. Verify important identifiers against authoritative statutory sources."*
- Emits evidence records with `source_type = "SCREENSHOT_OCR"` and preserves extraction engine metadata.

---

## 13. Phase 9 Implementation: Safe Response & Recovery

Phase 9 extends RakshaScan from answering *"What did we find?"* to answering *"What should the user safely do next?"*.

### 13.1 Design Principles
- **Deterministic & Explainable**: Core action recommendations are generated by rule-based engines in `app.response.rules`, not black-box LLMs.
- **Action States (No Scam Scores)**:
  - `SAFE_TO_CONTINUE_WITH_VERIFICATION`
  - `PAUSE_AND_VERIFY`
  - `HIGH_CAUTION`
  - `POST_INCIDENT_GUIDANCE`
  - `INSUFFICIENT_EVIDENCE`
- **Traceable Actions**: Every action recommendation includes an actionable title, clear explanation, deterministic reason, and linked evidence IDs / verification IDs.
- **Zero Payment Assumption**: Uses conditional phrasing (*"If you have already transferred money..."*); never assumes funds were transferred unless explicitly declared by the user.

### 13.2 Post-Incident Recovery Protocols
When withdrawal friction, advance fee demands, or user-declared transfers occur, a structured 5-stage recovery protocol is activated:
1. **Stop Further Money Transfers**: Refuse advance fee demands, unlock taxes, or clearance deposits.
2. **Preserve Documentation**: Save unedited chat transcripts, payment handles (UPI IDs/bank accounts), URLs, and transaction IDs (UTR/RRN). Strictly warns users **NOT** to save or upload OTPs, passwords, or PINs.
3. **Contact Financial Provider**: Notify official bank/app support immediately through verified channels to initiate transaction disputes or account freezes within the golden hour.
4. **File Official Report**: Guidance for official jurisdictional channels (National Cyber Crime Reporting Portal at `cybercrime.gov.in` / helpline `1930`).
5. **Secure Compromised Accounts**: Change net banking passwords and UPI PINs from an independent, secure device and remove unverified APKs.

### 13.3 Reconstructed Incident Timeline
An evidence-anchored timeline organizing observed milestones (`WEBSITE_VISITED`, `CLAIM_RECEIVED`, `COMMUNICATION_STARTED`, `PAYMENT_REQUESTED`) alongside user-declared events (`PAYMENT_MADE`, `USER_REPORTED`), with zero invented intermediate steps.

---

## 14. Phase 10 Implementation: Bharat-First Multilingual UX

Phase 10 introduces a lightweight, zero-latency localization layer designed for Indian retail investors.

### 14.1 Trilingual Architecture
- Supports **English (`en`)**, **Hindi (`hi`)**, and **Marathi (`mr`)**.
- Built on client-side state without re-running backend analysis or altering structured intelligence records.
- Prominent language switcher in Navbar and mobile drawer with instant UI re-rendering.

### 14.2 Plain-Language Mode ("Simple explanation")
- Optional toggle that translates dense regulatory and statutory jargon into accessible plain language (e.g., *"We could not confirm this claim using the available official source"* instead of *"Authoritative corroboration was unavailable"*).
- Simplifies phrasing while strictly preserving epistemic uncertainty.

### 14.3 Regional Language Safety
- **Strict Uncertainty Preservation**: Never translates unverified claims into definitive accusations (e.g., translates to *"यह दावा स्वतंत्र रूप से सत्यापित नहीं किया जा सका"*, never *"यह फर्जी है"*).
- **Exact Token Preservation**: Statutory identifiers (CIN, SEBI registration numbers, MCA IDs), URLs, phone numbers, evidence IDs, and verification IDs remain untranslated and exact.


---

## 15. Phase 11: Production Hardening & Deployment Preparation

Phase 11 hardens the RakshaScan architecture for reliable demonstration and production readiness:

### 15.1 In-Process Rate Limiting
- **Sliding-Window Limiter**: Built-in in-process sliding-window rate limiter (`app.core.rate_limit`) with zero external infrastructure dependencies.
- **Configurable Buckets**:
  - URL Analysis: 30 requests/minute (configurable via `RATE_LIMIT_URL_PER_MINUTE`).
  - Message Analysis: 30 requests/minute (configurable via `RATE_LIMIT_MESSAGE_PER_MINUTE`).
  - Screenshot Analysis: 15 requests/minute (configurable via `RATE_LIMIT_SCREENSHOT_PER_MINUTE`).
- **HTTP 429 Responses**: Returns structured JSON error payloads with `Retry-After` response headers.

### 15.2 Strict Request Sizing & Format Validation
- **URL Bounds**: Maximum 2,048 characters (`MAX_URL_LENGTH`), enforcing HTTP 413.
- **Message Bounds**: Maximum 15,000 characters (`MAX_MESSAGE_CHARACTERS`), enforcing HTTP 413.
- **Screenshot Bounds**: Maximum 10 MB (`MAX_IMAGE_BYTES`) and 8000x8000 pixel cap (`MAX_IMAGE_DIMENSION`), enforcing HTTP 413.
- **Magic Bytes Validation**: Enforces header magic numbers (`\x89PNG\r\n\x1a\n` for PNG, `\xff\xd8\xff` for JPEG, `RIFF...WEBP` for WEBP) to eliminate polyglot and extension spoofing vulnerabilities.
- **Zero Permanent Storage**: Screenshot images are processed in-memory via `io.BytesIO` buffers and immediately released; no disk writes, no database saves.

### 15.3 Security Headers & CORS
- **Security Headers Middleware**: Attaches `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-XSS-Protection: 1; mode=block`, and `Permissions-Policy: geolocation=(), camera=(), microphone=()`.
- **Production CORS**: Configured via `CORS_ORIGINS` environment variable with `allow_credentials=False` to prevent unnecessary credential exposure.
- **Health Check**: `GET /health` returns `{"status": "ok"}` without exposing infrastructure internals.

### 15.4 Privacy-Preserving Telemetry & Sanitized Logging
- **Zero-Retention Principle**: Never logs raw message text, OCR transcripts, screenshot bytes, passwords, OTPs, PINs, or banking credentials.
- **Query Parameter Redaction**: Automatically scrubs sensitive URL parameters (`token`, `auth`, `key`, `password`, `otp`, `pin`, `cvv`) in operational logs.

### 15.5 Deployment Commands & Environment Variables
- **Backend Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
  ```
- **Frontend Build & Start**:
  ```bash
  cd frontend
  npm run build
  npm start
  ```
- **Required Production Environment Variables**:
  - `ENVIRONMENT=production`
  - `CORS_ORIGINS=https://rakshascan.yourdomain.com`
  - `NEXT_PUBLIC_API_BASE_URL=https://api.rakshascan.yourdomain.com`
  - `RATE_LIMITING_ENABLED=True`

---

## 16. Demo vs Production Distinction

> [!IMPORTANT]
> **Statutory Disclaimer on Verification Data Sources**:
> In the current hackathon MVP build, regulatory verification against SEBI, MCA, and RBI databases is powered by **demonstration and synthetic test registries** (`DemoVerificationAdapter`).
> 
> - **Synthetic Records**: Sample identifiers (e.g. `INA000099999`, `U67190MH2021PTC369999`) reference fictional test fixtures explicitly marked with `is_demo: true` and labeled *"Demonstration verification source — not a live statutory lookup"*.
> - **No Fabricated Authority**: RakshaScan does **not** scrape CAPTCHA-protected government portals or claim real-time authoritative validation where official statutory APIs are unavailable.
> - **Production Roadmap**: Production deployments will integrate with official government open data APIs (MCA21 V3, SEBI intermediary webhooks, DigiLocker financial verification) as authentic read-only adapters.

---

## 17. Test Suite Coverage (125 Unit & Integration Tests)

The backend test suite covers 125 comprehensive tests:
- 15 Phase 2 tests (SSRF, URL validation, stream limits, redirects, HTML extraction).
- 12 Phase 3 tests (entity extraction, regulatory references, 11 financial claim types, evidence anchoring).
- 11 Phase 4 tests (statutory verification states, demo adapters, directory mismatches).
- 22 Phase 5 tests (evidence engine, 10 deterministic risk rules, 4 concern levels, non-prejudicial outputs).
- 10 Phase 6 tests (Trust Chain node creation, relationships, verified/contradictory/unknown handling, non-propagation, traceability, dynamic summary counts).
- 9 Phase 7 tests (Scam Journey stages, observed vs suspected distinction, confidence levels, mandatory disclaimer, zero fabrication).
- 21 Phase 8 tests (message validation, empty/oversized rejection, financial claims, urgency, deposit pressure, withdrawal fees, evidence traceability, screenshot PNG/JPEG validation, MIME rejection, oversized image rejection, in-memory privacy, OCR evidence, trust chain integration, scam journey integration, non-crawling URL extraction, FastAPI endpoints).
- 14 Phase 9 tests (low concern informational guidance, moderate pause/verify, high caution safety actions, guaranteed return pause, deposit pressure, withdrawal fee post-incident, additional payment guidance, evidence traceability, no unsupported reasons, no automatic payment assumption, user declared payment activation, user declared no payment, user not sure cautious guidance, timeline event restraint, API safe response integration).
- 11 Phase 11 tests (health check probe, security headers middleware, CORS configuration, sliding window rate limiter, URL 413 length cap, message 413 length cap, screenshot 413 payload cap, magic bytes image verification, logging privacy sanitizer, SSRF cloud metadata block, demo verification explicit labeling).

```bash
# Run all 125 backend tests
python -m pytest backend/tests -v
```

---

## 18. Security Controls & Known Limitations

### Security Status
- **Zero Active Penetration**: RakshaScan operates strictly on passive, public webpage content, uploaded user snippets, and authoritative directories.
- **Strict SSRF Immunity**: Enforces RFC 1918 / loopback / cloud metadata IP blocks at DNS resolution and at each redirect hop.
- **In-Process Abuse Defense**: Sliding window rate limits safeguard expensive OCR and URL analysis.
- **Payload Limits**: Strict HTTP 413 boundaries prevent memory exhaustion from oversized submissions.
- **Magic Bytes Validation**: Cryptographic/header validation eliminates disguised executable uploads.
- **Zero Credential Collection**: Prominently warns users never to upload OTPs, passwords, PINs, or banking authentication secrets.
- **No Cloud Vision Leakage**: Image OCR runs completely locally and offline without external data transfer.
- **Client-Side Incident State**: User-reported transaction states are strictly ephemeral in the browser and never stored to backend databases.

### Known Limitations
1. **Public Surface Analysis**: RakshaScan evaluates observable claims and configured statutory directories; it cannot audit private offline meetings or closed group chats without victim-submitted artifacts.
2. **Third-Party Regulator Availability**: Live regulator registries that require interactive CAPTCHAs report `UNAVAILABLE` rather than attempting unauthorized automated bypasses.
3. **Analytical Model**: Safe Response and Scam Journey Reconstruction provide consumer education regarding documented patterns, not judicial or prosecutorial proof.
4. **OCR Misread Probability**: Optical text extraction from low-resolution or skewed screenshots may introduce character inaccuracies in complex alphanumeric registration codes.

---

## 19. Hackathon Demonstration Guide & Judge Evaluation

For live evaluations, video recordings, and step-by-step walkthroughs, consult the comprehensive guide:

👉 **[docs/DEMO_GUIDE.md](docs/DEMO_GUIDE.md)**

It provides:
- Recommended 3–5 minute pitch sequence.
- Exact pre-tested fictional inputs for messages, screenshots, and URLs.
- Step-by-step breakdown of how each intelligence layer (Extraction, Verification, Risk, Trust Chain, Journey, Safe Response, Recovery) renders.
- Vernacular switching demo instructions.
- Failover plans and local execution commands.





