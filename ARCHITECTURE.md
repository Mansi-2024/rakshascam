# RakshaScan — System Architecture Specification

> **SANGYAN 2026 Production-Oriented Prototype**  
> *Target Stack: Next.js + TypeScript (Frontend) | FastAPI + Python (Backend) | PostgreSQL (Database)*

---

## 1. System Topology Overview

RakshaScan employs a clean decoupled architecture separating user interaction, deterministic verification pipelines, AI perception, and structured evidence aggregation:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND CLIENT TIER                            │
│  Next.js 14+ (App Router) • TypeScript • Tailwind CSS • Lucide Icons   │
│  - Input Submission (URL, Chat/Text, Screenshot)                       │
│  - Trust Chain Interactive Graph Visualizer                            │
│  - Scam Journey Timeline Reconstructor                                 │
│  - 7-Point Evidence-Based Assessment Dashboard                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS / REST (JSON)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND API & ORCHESTRATION                      │
│                    FastAPI (Python 3.11+) + Pydantic v2                 │
│                                                                        │
│  ┌───────────────────────┐              ┌───────────────────────────┐  │
│  │   Security Gateway    │              │     Task Orchestrator     │  │
│  │ Rate Limiter • CORS   │              │   Async Pipeline Manager  │  │
│  │ SSRF Filter • Auth    │              │  (Validation & Analysis)  │  │
│  └───────────┬───────────┘              └─────────────┬─────────────┘  │
│              └─────────────────┬──────────────────────┘                │
│                                │                                       │
│    ┌───────────────────────────┴──────────────────────────┐            │
│    ▼                                                      ▼            │
│  ┌───────────────────────────────┐     ┌────────────────────────────┐  │
│  │           AI LAYER            │     │     VERIFICATION LAYER     │  │
│  │  (Perception & Extraction)    │     │  (Deterministic Truth)     │  │
│  │  - Entity Extraction          │     │  - DNS / WHOIS / IP Audits │  │
│  │  - Financial Claim Parsing    │     │  - SSL Certificate Chains  │  │
│  │  - OCR & Visual Text (Vision) │     │  - Official MCA Registries │  │
│  │  - Linguistic Classifier      │     │  - SEBI / RBI Databases    │  │
│  │  - Evidence Summarizer        │     │  - Banking / UPI Resolvers │  │
│  └───────────────┬───────────────┘     └──────────────┬─────────────┘  │
│                  │                                    │                │
│                  └─────────────────┬──────────────────┘                │
│                                    │ Normalized Signals                │
│                                    ▼                                   │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        CORE ENGINES                              │  │
│  │                                                                  │  │
│  │  ┌─────────────────────────┐      ┌───────────────────────────┐  │  │
│  │  │     EVIDENCE ENGINE     │      │        RISK ENGINE        │  │  │
│  │  │  - Trust Chain Graph    │      │  - Rule-Based Scoring     │  │  │
│  │  │  - Status Resolution    │      │  - Contradiction Detector │  │  │
│  │  │  - Dossier Generator    │      │  - Scam Journey Matcher   │  │  │
│  │  └─────────────────────────┘      └───────────────────────────┘  │  │
│  └─────────────────────────────────┬────────────────────────────────┘  │
└────────────────────────────────────┼───────────────────────────────────┘
                                     │ Async SQLAlchemy / SQLModel
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENCE TIER                               │
│                   PostgreSQL (Relational + JSONB)                      │
│  - Investigations & Scan Runs         - Registry Cache & Mirror        │
│  - Trust Chain Nodes & Edges          - Evidence Dossiers (JSONB)      │
│  - Extracted Artifacts & Hashes       - Audit Trails & Logs            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Frontend Layer (Next.js & TypeScript)

- **Framework**: Next.js (App Router) with TypeScript for end-to-end type safety.
- **Styling**: Tailwind CSS for responsive, modern design, avoiding generic palettes in favor of clean dark/light accessible themes.
- **UI Components**:
  - `ScanInputPanel`: Supports multi-mode submission (URL inspection, raw text paste, screenshot upload with client-side size validation).
  - `TrustChainVisualizer`: Interactive node-link canvas rendering the 8-node Trust Chain with distinct state colors (`VERIFIED`, `UNVERIFIED`, `CONTRADICTORY`, `UNKNOWN`).
  - `ScamJourneyTimeline`: Phased step progression highlighting detected vs. potential stages of the scam progression.
  - `EvidenceDossierCard`: Accordion and tabbed layout displaying the 7-Point Evidence Assessment with downloadable evidence manifests.
  - `SafeNextStepsPanel`: Clear, actionable, prioritized defensive guidance.

---

## 3. Backend Layer (FastAPI & Python) — Phase 2 & Phase 3 Architecture

- **Framework**: FastAPI (Python 3.11+) taking advantage of asynchronous I/O (`asyncio`) for non-blocking HTTP analysis.
- **Data Validation**: Strict Pydantic v2 schemas for all request payloads, internal data transfers, and response objects.
- **Implemented Backend Layout**:
  - `backend/app/main.py`: FastAPI application entrypoint with CORS middleware, health probes, and API router registration.
  - `backend/app/api/routes/analysis.py`: Endpoint `POST /api/v1/analyze/url` accepting `URLAnalysisRequest` and returning typed `URLAnalysisResponse`.
  - `backend/app/core/security.py`: Zero-trust SSRF validation engine, DNS pre-flight address verification, loopback/private/link-local/metadata IP rejection, and IPv4-mapped IPv6 unwrapping.
  - `backend/app/core/config.py`: Hardened network limits (3s connect timeout, 7s read timeout, 10s total timeout, 5MB response cap, max 3 redirects).
  - `backend/app/schemas/analysis.py`: Typed Pydantic v2 schemas:
    - Phase 2: `URLInputModel`, `FetchResultModel`, `PageModel`, `LinkItemModel`, `ContactSignalsModel`, `DetectedReferencesModel`, `AnalysisMetadataModel`.
    - Phase 3: `EvidenceModel`, `EntityModel`, `ClaimModel`, `RegulatoryReferenceModel`, `FinancialClaimModel`, `IdentityRelationshipModel`.
  - `backend/app/services/url_analyzer.py`: Safe asynchronous HTTP retrieval engine using `httpx.AsyncClient` with manual redirect re-validation, chunked streaming byte cap, and structured analysis orchestration.
  - `backend/app/services/html_extractor.py`: Deterministic BeautifulSoup HTML parser performing structured extraction of:
    - **Entities**: Company (`Private Limited`, etc.), Person (executives with honorifics), Domain.
    - **Claims**: Regulatory, Financial, Identity, Authorization.
    - **Regulatory References**: SEBI, RBI, MCA, NSE, BSE, IRDAI, PFRDA with proximity-associated registration numbers (e.g., `INA000099999`, CIN, GSTIN).
    - **Financial Claims**: 11 deterministic linguistic categories with severity classifications.
    - **Identity Relationships**: Graph connections (`OPERATES_DOMAIN`, `CLAIMS_AUTHORIZATION`, `REFERENCES_REGISTRATION`, `ASSOCIATED_WITH`, `LINKS_TO_EXTERNAL`).
    - **Evidence Anchor Objects**: Traceable `Claim → Evidence → Source` links with context, exact extracted text, and extraction method.
    - **Core Principle**: All extracted claims, references, and relationships retain `verification_status: "UNKNOWN"`. Extraction ≠ Verification.

---

## 4. AI Layer (Perception, NOT Source of Truth)

> **Architectural Guardrail**: The AI Layer is explicitly treated as a **non-authoritative perception component**. It cannot set verification statuses directly.

### Responsibilities:
1. **Entity Extraction**: Identifying company names, brand names, purported directors, claimed license numbers (CIN, SEBI Reg No, RBI NBFC No), email addresses, phone numbers, and Telegram/WhatsApp usernames.
2. **Claim Extraction**: Extracting explicit promises (e.g., "Guaranteed 15% weekly profit", "Zero risk capital guarantee", "SEBI approved algorithmic trading").
3. **Linguistic Classification**: Detecting high-pressure urgency cues, manipulative social-engineering patterns, and deceptive phrasing.
4. **Evidence Summarization**: Synthesizing raw registry diffs and technical findings into clear, plain-language summaries for non-technical users.
5. **Context Explanation**: Explaining *why* a specific gap or contradiction matters in practical financial terms.

---

## 5. Verification Layer (Authoritative & Deterministic) — Phase 4 Architecture

> **Critical Mandate**: *"Verification results are only authoritative when derived from the identified authoritative source."*

The Verification Layer evaluates claims and references against independent, verifiable records rather than textual appearances.

### 5.1 Subsystem Layout (`backend/app/verification/`)
- `base.py`: Declares abstract interface `VerificationAdapter` with `can_verify(item)` and `verify(item, context)`.
- `models.py`: Defines `VerificationResult` and enum `VerificationStatus` (`VERIFIED`, `CONTRADICTORY`, `NOT_FOUND`, `UNKNOWN`, `UNAVAILABLE`).
- `engine.py`: `VerificationEngine` orchestrates adapter dispatch, attaches results to claims while preserving original text and evidence, and provides exception-isolation fallbacks (`UNAVAILABLE`) so failures never crash the scanner.
- `adapters/demo.py`: `DemoVerificationAdapter` provides deterministic evaluations on synthetic test records (`INA000099999`, `Example Wealth Advisors Private Limited`). All results carry `is_demo: true` and are clearly labeled as demonstration fixtures.
- `adapters/official_stubs.py`: Explicit stubs for `SebiRegistryAdapter` and `McaRegistryAdapter` documenting why direct unauthenticated integration is currently marked `UNAVAILABLE` (mandates against scraping, CAPTCHA bypass, and unauthenticated access).

### 5.2 The Five Verification States
1. **`VERIFIED`**: The authoritative source provides positive evidence substantiating the claim (e.g. registration code is active and matches claimant).
2. **`CONTRADICTORY`**: The authoritative source was successfully queried, but contradicts the claim (e.g. registration exists but is assigned to a different legal entity).
3. **`NOT_FOUND`**: The authoritative source was successfully queried, but the claimed entity or registration does not exist. *(Crucial: `NOT_FOUND` does not automatically mean fraud).*
4. **`UNKNOWN`**: Insufficient information exists to initiate or complete a check (e.g. generic claim of government approval with no license number). *(Crucial: `UNKNOWN` does not mean safe).*
5. **`UNAVAILABLE`**: The authoritative registry could not be reached, encountered an internal error, or requires interactive CAPTCHA. *(Crucial: `UNAVAILABLE` does not mean not-found).*

### 5.3 Complete Provenance Guarantee
No verification result is produced without verifiable audit metadata:
- `source_name`: Exact name of the registry or demo provider.
- `source_url`: Official directory endpoint (or internal synthetic mock URI).
- `checked_at`: ISO 8601 UTC timestamp.
- `verification_method`: Query approach used.
- `matched_entity` & `matched_registration`: Exact records retrieved.
- `evidence`: Direct registry excerpt.
- `reason`: Objective, non-prejudicial rationale.

---

## 6. Phase 5: Evidence & Evidence-Backed Risk Assessment Subsystem

### Core Principle
> **"RakshaScan produces evidence-backed concern assessments, not fraud verdicts."**
> Every risk signal must be explainable and backed by traceable evidence. The system never outputs a numerical "scam score" or declares a website a "scam" based on keywords.

### 6.1. The Evidence Engine (`backend/app/evidence/`)
- **Immutable Evidence Records (`EvidenceRecord`)**:
  - `evidence_id`: Globally unique identifier (`ev_<uuid>`).
  - `source_type`: Origin classification (`WEBPAGE_BODY`, `META_TAG`, `OFFICIAL_REGISTRY`, `HTTP_HEADER`).
  - `source_url`: URL or endpoint where the evidence was directly observed.
  - `extracted_text`: Exact verbatim excerpt as observed on the source (raw evidence is never replaced by AI summary).
  - `context`: Surrounding sentences or contextual snippet.
  - `extraction_method`: Strategy (`regex_pattern`, `css_selector`, `authoritative_query`).
  - `related_claim_id` & `related_entity_id`: Foreign keys tying evidence directly to extracted claims or entities.
  - `created_at`: UTC timestamp.
- **Evidence Indexing & Summary**:
  - `EvidenceEngine` indexes all records by ID, Claim ID, and Entity ID.
  - Computes `EvidenceSummary` quantifying verified, unverified, contradictory, and unknown claims.

### 6.2. The Risk Signal Engine (`backend/app/risk/`)
- **Risk Signal Structure (`RiskSignal`)**:
  - `signal_id`, `category` (`IDENTITY`, `REGULATORY`, `FINANCIAL`, `MANIPULATION`, `TECHNICAL`, `BEHAVIORAL`), `severity` (`LOW`, `MEDIUM`, `HIGH`).
  - `title`, `description`, `explanation` (factual, non-prejudicial rationale).
  - `evidence_ids`, `claim_ids`, `verification_ids`: Full audit trace.
  - `confidence` (`LOW`, `MEDIUM`, `HIGH`): Confidence in signal *detection*, not fraud probability.
- **Deterministic Rules Evaluated (`rules.py`)**:
  - **Rule 1 — Guaranteed return language**: Triggered on `GUARANTEED_RETURN` (`FINANCIAL`, `HIGH`).
  - **Rule 2 — Risk-free language**: Triggered on `RISK_FREE` (`FINANCIAL`, `HIGH`).
  - **Rule 3 — Double-money language**: Triggered on `DOUBLE_MONEY` (`FINANCIAL`, `HIGH`).
  - **Rule 4 — Deposit pressure**: Triggered on `DEPOSIT_PRESSURE` (`MANIPULATION`, `HIGH`).
  - **Rule 5 — Withdrawal fee / additional payment**: Triggered on `WITHDRAWAL_FEE` / `ADDITIONAL_PAYMENT` (`FINANCIAL`, `HIGH`).
  - **Rule 6 — Urgency language**: Triggered on `URGENCY` / `ACT_NOW` (`MANIPULATION`, `MEDIUM`).
  - **Rule 7 — Regulatory claim requiring verification**: Claim status `UNKNOWN` or `UNAVAILABLE` (`REGULATORY`, `MEDIUM`). Factual note: Does not call claim false.
  - **Rule 8 — Regulatory contradiction**: Claim status `CONTRADICTORY` (`REGULATORY`, `HIGH`). Factual mismatch explanation; never states "This is a scam".
  - **Rule 9 — Registration not found**: Verification status `NOT_FOUND` (`REGULATORY`, `MEDIUM`). Explicitly states: *"Not found does not by itself establish fraud."*
  - **Rule 10 — Entity identity mismatch**: Claimed registration belongs to an alternate entity (`IDENTITY`, `HIGH`). Traces claimed entity, registration, and authoritative matched entity.
- **Signal Deduplication**:
  - Collapses multiple occurrences of identical rule categories/patterns into a single primary signal.
  - Preserves union of all supporting `evidence_ids` and `claim_ids`.

### 6.3. The Assessment Engine (`backend/app/risk/engine.py`)
- **Overall Concern Levels (`ConcernLevel`)**:
  - `INSUFFICIENT_EVIDENCE`: Less than 2 evidence items observed or page text too sparse to formulate a conclusion.
  - `LOW_CONCERN`: No high-severity signals and at most 1 low/medium signal without regulatory contradictions.
  - `MODERATE_CONCERN`: Multiple medium-severity signals, unverified claims, or unconfirmed regulatory registrations.
  - `HIGH_CONCERN`: One or more high-severity regulatory/identity contradictions or multiple high-severity financial/manipulation signals.
- **Uncertainty Preservation**:
  - Explicitly states boundaries: `NOT_FOUND ≠ FRAUD`, `UNKNOWN ≠ SAFE`, `UNAVAILABLE ≠ NOT_FOUND`.
  - Appends actionable, non-destructive Safe Next Steps (e.g., cross-check on SEBI portal, consult independent SEBI-registered advisor).

---

## 8. Phase 6 Architecture: The Financial Trust Chain (`app.trust_chain`)

The **Financial Trust Chain** models identity provenance and dependency resolution across eight structural tiers:
```
Claim ──▶ Entity ──▶ Registration ──▶ Official Identity ──▶ Website ──▶ App ──▶ Social Account ──▶ Payment Identity
```

### 8.1 Data Models (`app/trust_chain/models.py`)
- **`TrustChainNode`**:
  - `node_id: str`
  - `node_type: TrustChainNodeType` (`CLAIM`, `ENTITY`, `REGISTRATION`, `OFFICIAL_IDENTITY`, `WEBSITE`, `APP`, `SOCIAL_ACCOUNT`, `PAYMENT_IDENTITY`)
  - `label: str`
  - `value: str`
  - `status: TrustChainStatus` (`VERIFIED`, `UNVERIFIED`, `CONTRADICTORY`, `UNKNOWN`, `UNAVAILABLE`, `NOT_OBSERVED`)
  - `evidence_ids: List[str]`
  - `verification_ids: List[str]`
  - `metadata: Dict[str, Any]`
- **`TrustChainRelationship`**:
  - `relationship_id: str`
  - `source_node_id: str`
  - `target_node_id: str`
  - `relationship_type: TrustChainRelationshipType` (`CLAIMS`, `REGISTERED_AS`, `IDENTIFIED_AS`, `OPERATES`, `ASSOCIATED_WITH`, `LINKS_TO`, `USES`, `RECEIVES_PAYMENT`)
  - `status: TrustChainStatus`
  - `evidence_ids: List[str]`
  - `verification_ids: List[str]`
  - `explanation: str`
- **`TrustChainSummary`**:
  - Dynamically calculates: `total_nodes`, `total_relationships`, `verified_count`, `unverified_count`, `contradictory_count`, `unknown_count`, `unobserved_count`, and `summary_text`.
- **`TrustChainGraph`**: Encapsulates nodes, relationships, and the dynamic summary.

### 8.2 Strict Architectural Rules
1. **Evidence-Backed Linkage**: *"Trust Chain relationships are established only when supported by available evidence."* Missing links are designated `UNKNOWN` or `NOT_OBSERVED`; they are never fabricated.
2. **Strict Status Non-Propagation**: Node statuses do not cascade across independent relationships. Verification of a statutory license does not verify an unlisted website domain.
3. **Objective Discrepancy Reporting**: Contradictions between claimed and authoritative records are explicitly explained without applying emotive or prejudicial labels like "SCAM".

---

## 9. Phase 7 Architecture: Scam Journey Reconstruction (`app.journey`)

**Scam Journey Reconstruction** synthesizes observable on-page assertions, linguistic cues, and infrastructure points into a sequential 6-stage behavioral interaction pattern.

> **Architecture Principle**: *"Scam Journey Reconstruction represents a possible/reconstructed interaction pattern and is not a determination of fraud."*

### 9.1 Data Models (`app/journey/models.py`)
- **`ScamJourney`**:
  - `journey_id: str`
  - `pattern_title: str` ("Possible scam journey pattern")
  - `confidence: JourneyConfidence` (`LOW`, `MEDIUM`, `HIGH`) — Reflects evidence completeness in matching an analytical model, NOT a probability of fraud.
  - `stages: List[ScamJourneyStage]`
  - `evidence_ids: List[str]`
  - `uncertainty_notes: List[str]`
  - `disclaimer: str` — Mandatory non-prejudicial disclaimer.
  - `summary_text: str` — Dynamic stage completeness summary (e.g., "4 of 6 stages supported by available evidence.").
- **`ScamJourneyStage`**:
  - `stage_id: str`, `order: int` (1 to 6)
  - `stage_type: StageType` (`INITIAL_CONTACT`, `FINANCIAL_CLAIM`, `WEBSITE`, `COMMUNICATION_CHANNEL`, `DEPOSIT_REQUEST`, `WITHDRAWAL_ISSUE`)
  - `title: str`, `description: str`
  - `status: StageStatus` (`OBSERVED`, `SUSPECTED`, `NOT_OBSERVED`, `UNKNOWN`)
  - `evidence_ids: List[str]`, `signal_ids: List[str]`
  - `confidence: str` (`LOW`, `MEDIUM`, `HIGH`)
  - `why_present: str`, `uncertainty: Optional[str]`

### 9.2 Builder Synthesis (`app/journey/builder.py`)
- Integrates outputs from `RiskAssessmentEngine`, `html_extractor`, and `VerificationEngine`.
- Maps risk signals deterministically:
  - `DEPOSIT_PRESSURE` ──▶ `DEPOSIT_REQUEST`
  - `WITHDRAWAL_FEE` / `ADDITIONAL_PAYMENT` ──▶ `WITHDRAWAL_ISSUE`
  - `GUARANTEED_RETURN` / `RISK_FREE` / `DOUBLE_MONEY` ──▶ `FINANCIAL_CLAIM`
  - `URGENCY` / `ACT_NOW` ──▶ `INITIAL_CONTACT` (SUSPECTED)
- Distinguishes observed facts (explicit text) from suspected patterns (inferred from pressure/urgency).
- Verbatim mandatory disclaimer rendered across API and UI.

---

## 10. Data Flow: From Submission to Dossier

```
1. [User Input (URL / Message / Screenshot)] ─┐
                                            │
2. [Security Gateway & Ingestion Normalizer] ─▼
                                     ┌─────────────────────────┐
                                     │ NormalizedAnalysisInput │
                                     └────────────┬────────────┘
                       ┌──────────────────────────┴──────────────────────────┐
                       ▼                                                     ▼
             ┌───────────────────┐                                 ┌───────────────────┐
             │ Structured Extract│                                 │ Verification Layer│
             │ - Extracts claims │                                 │ - Resolves domain │
             │ - Extracts entities│                                 │ - Queries records │
             │ - Traceable Ev ID │                                 │ - Validates SSL   │
             └─────────┬─────────┘                                 └─────────┬─────────┘
                       │ Claims & Entities                                   │ Ground Truth
                       └──────────────────────────┬──────────────────────────┘
                                                  ▼
                                     ┌─────────────────────────┐
                                     │     Evidence Engine     │
                                     │  - Cross-validates data │
                                     │  - Anchors provenance   │
                                     │  - Generates Proof Tree │
                                     └────────────┬────────────┘
                                                  ▼
                                     ┌─────────────────────────┐
                                     │       Risk Engine       │
                                     │  - Detects Conflicts    │
                                     │  - 10 Assessment Rules  │
                                     └────────────┬────────────┘
                                                  ▼
                                     ┌─────────────────────────┐
                                     │   Financial Trust Chain │
                                     │   & Scam Journey Builder│
                                     └────────────┬────────────┘
                                                  ▼
                                     ┌─────────────────────────┐
                                     │  Unified API Response   │
                                     │  & Dashboard Delivery   │
                                     └─────────────────────────┘
```

---

## 11. Multi-Input Ingestion Architecture (Phase 8)

Phase 8 establishes a normalized ingestion layer (`backend/app/ingestion/`) so that copied messages, uploaded screenshots, and live website URLs feed into a single unified structured extraction, verification, risk assessment, Trust Chain, and Scam Journey pipeline.

### 11.1 Ingestion Models (`app/ingestion/models.py`)
- **`AnalysisInputType`**: `URL`, `MESSAGE`, `SCREENSHOT`.
- **`NormalizedAnalysisInput`**:
  - `input_type: AnalysisInputType`
  - `source_text: Optional[str]` — Raw original text submitted or OCR-extracted.
  - `source_url: Optional[str]` — Validated HTTP URL or pseudo-scheme (`message://submitted`, `screenshot://submitted`).
  - `extracted_text: str` — Safely normalized text body.
  - `source_type: str` — Concrete provenance label (`PAGE_TEXT`, `USER_SUBMITTED_MESSAGE`, `SCREENSHOT_OCR`).
  - `detected_urls: List[str]` — Structured URLs detected in text without recursive auto-crawling.
  - `metadata: Dict[str, Any]` — Ingestion telemetry (e.g. image dimensions, OCR engine label, file size).

### 11.2 Text Message Ingestion (`app/ingestion/text.py`)
- **Validation**: Enforces 15,000 character maximum limit and rejects empty or whitespace-only inputs.
- **Safe Normalization**: Strips dangerous non-printable ASCII control characters while preserving formatting line breaks.
- **URL Discovery**: Parses raw HTTP/HTTPS/WWW links into structured links without automated crawling.
- **Provenance**: Generates evidence records with `source_type = "USER_SUBMITTED_MESSAGE"`.

### 11.3 Screenshot & Local OCR Ingestion (`app/ingestion/image.py`)
- **Format & Size Controls**: Enforces a 10MB payload cap and restricts MIME types to `image/png`, `image/jpeg`, and `image/webp`.
- **Image Header Verification**: Uses Pillow (`verify()`) to reject corrupted files or decompression bombs (max 8000x8000 pixels).
- **100% Local Processing**: Executes local offline OCR or metadata text extraction; never transfers user images to cloud vision APIs.
- **Zero Disk Storage**: Operates entirely in memory (`io.BytesIO`); zero disk writes, zero database image persistence.
- **Explicit Uncertainty**: Injects explicit OCR uncertainty notes without synthetic text alteration.
- **Provenance**: Generates evidence records with `source_type = "SCREENSHOT_OCR"`.

### 11.4 Unified Analyzer (`app/services/unified_analyzer.py`)
- Standardizes execution across all input modalities:
  `analyze_message_service(text)` ──▶ `NormalizedAnalysisInput` ──▶ `analyze_normalized_input()`
  `analyze_screenshot_service(bytes)` ──▶ `NormalizedAnalysisInput` ──▶ `analyze_normalized_input()`
- Reuses `extract_comprehensive_analysis`, `VerificationEngine`, `EvidenceEngine`, `RiskAssessmentEngine`, `TrustChainBuilder`, `ScamJourneyBuilder`, and `SafeResponseEngine` with zero duplicate logic.

---

## 12. Safe Response & Recovery Architecture (Phase 9)

Phase 9 implements an evidence-aware interpretation and action engine (`backend/app/response/`) answering: *"What should the user safely do next?"*.

### 12.1 Module Structure
- `backend/app/response/models.py`: Pydantic data schemas:
  - `ResponseMode`: `PRE_TRANSACTION`, `SUSPICIOUS_CONTENT`, `POSSIBLE_ACTIVE_SCAM`, `POST_INCIDENT`, `INFORMATIONAL`, `INSUFFICIENT_EVIDENCE`.
  - `ActionState`: `SAFE_TO_CONTINUE_WITH_VERIFICATION`, `PAUSE_AND_VERIFY`, `HIGH_CAUTION`, `POST_INCIDENT_GUIDANCE`, `INSUFFICIENT_EVIDENCE`.
  - `SafeActionType`: `PAUSE`, `VERIFY`, `DO_NOT_SHARE_CREDENTIALS`, `DO_NOT_INSTALL_UNKNOWN_APP`, `DO_NOT_SEND_ADDITIONAL_MONEY`, `PRESERVE_EVIDENCE`, `CONTACT_OFFICIAL_CHANNEL`, `REPORT`, `CONTACT_BANK_OR_PAYMENT_PROVIDER`, `MONITOR`, `SEEK_HUMAN_ASSISTANCE`.
  - `ActionRecommendation`: Strongly-typed action card with title, explanation, deterministic reason, and traceable evidence IDs & verification IDs.
  - `IncidentTimeline` & `IncidentTimelineEvent`: Chronological milestone reconstruction.
  - `RecoveryGuidance` & `RecoveryStep`: 5-step structured post-incident playbook.
  - `UserIncidentState`: Ephemeral user facts (`sent_money`, `shared_credentials`).
- `backend/app/response/rules.py`:
  - `evaluate_action_state_and_mode()`: Deterministic mapping from risk signals, concern levels, and user declarations to ActionState.
  - `collect_recommended_actions()`: Priority-ordered safe actions with required explanation and evidence/verification IDs.
  - `build_recovery_guidance()`: 5-step mitigation guidance with jurisdictional reporting advice.
  - `build_incident_timeline()`: Reconstructs milestones strictly from observed evidence and user input without inventing events.
- `backend/app/response/engine.py`: `SafeResponseEngine.generate_response()` synthesizing assessment, signals, verification outcomes, and user state into `SafeResponse`.

### 12.2 Integration Flow
The Safe Response and Recovery module integrates directly into the unified response payload:
```
Analysis Input ──▶ Extraction ──▶ Verification ──▶ Risk Assessment
                      │
                      ▼
               Trust Chain & Scam Journey
                      │
                      ▼
               SafeResponseEngine
                      │
                      ▼
         URLAnalysisResponse (safe_response + recovery_guidance)
```

---

## 13. Bharat-First / Multilingual UX Architecture (Phase 10)

Phase 10 provides a localized client experience for Indian retail investors across diverse linguistic backgrounds.

### 13.1 Architecture Overview
- `frontend/lib/i18n/translations.ts`: Central trilingual dictionary with standardized keys across:
  - English (`en`)
  - Hindi (`hi`)
  - Marathi (`mr`)
- `frontend/lib/i18n/LanguageContext.tsx`: React Context providing reactive language state, instant UI switching, and `simplifyText` plain-language transformer.
- `frontend/lib/i18n/index.ts`: Package exports.

### 13.2 Plain-Language Transformer
- Implements a deterministic plain-language transformer for key regulatory statements (e.g. simplifying *"Authoritative corroboration was unavailable"* to *"We could not confirm this claim using the available official source"*).
- Preserves epistemic uncertainty; never converts unverified claims into definitive accusations.

### 13.3 Technical Token Invariance
- Statutory identifiers, registration strings (e.g. `INA000099999`, CIN), URLs, emails, phone numbers, evidence IDs, and verification IDs remain untranslated and exact across all language views.

---

## 14. Production Hardening & Operational Security Architecture (Phase 11)

Phase 11 introduces comprehensive defenses, in-process rate limiting, input size controls, and security headers:

### 14.1 In-Process Sliding-Window Rate Limiting
- **Module**: `backend/app/core/rate_limit.py`.
- **Mechanism**: Thread-safe sliding-window bucket algorithm operating entirely in-process without external Redis or cache requirements.
- **Client Identification**: Extracts IP from `X-Forwarded-For` proxy headers or fallback socket address.
- **Buckets**:
  - `url`: 30 requests/minute default (`RATE_LIMIT_URL_PER_MINUTE`).
  - `message`: 30 requests/minute default (`RATE_LIMIT_MESSAGE_PER_MINUTE`).
  - `screenshot`: 15 requests/minute default (`RATE_LIMIT_SCREENSHOT_PER_MINUTE`).
- **HTTP 429 Status**: Emits standard `429 Too Many Requests` responses with `Retry-After` calculation.

### 14.2 Multi-Layer Ingestion Validation
- **Length & Sizing Caps**:
  - URLs: Capped at 2,048 characters (`MAX_URL_LENGTH`), enforcing HTTP 413.
  - Messages: Capped at 15,000 characters (`MAX_MESSAGE_CHARACTERS`), enforcing HTTP 413.
  - Images: Capped at 10 MB (`MAX_IMAGE_BYTES`) and 8000x8000 pixels (`MAX_IMAGE_DIMENSION`), enforcing HTTP 413.
- **Header Magic Bytes Verification**: Validates file magic signatures (`PNG`, `JPEG`, `WEBP`) before passing to Pillow to eliminate polyglot attacks.
- **In-Memory Buffer Release**: Screenshot bytes are read strictly in-memory into `io.BytesIO` and immediately discarded after text extraction.

### 14.3 HTTP Security Middleware
- Standardizes defensive response headers across all FastAPI endpoints via `SecurityHeadersMiddleware`:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `X-XSS-Protection: 1; mode=block`
  - `Permissions-Policy: geolocation=(), camera=(), microphone=()`

### 14.4 Privacy-Preserving Telemetry & Structured Logging
- **Module**: `backend/app/core/logging.py`.
- **Zero Raw Data Retention**: Never logs submitted messages, OCR text, image buffers, passwords, PINs, or credentials.
- **Query Parameter Redaction**: Sanitizes URLs in logs, replacing sensitive query parameters (`token`, `auth`, `key`, `password`, `otp`, `pin`, `cvv`) with `[REDACTED]`.

---

## 15. Demo vs Production Verification Boundaries

The verification architecture strictly enforces the distinction between demonstration mock data and real-world statutory authority:

1. **Current Hackathon State (Demonstration Mode)**:
   - Evaluated using `DemoVerificationAdapter` on seeded synthetic fixtures (`INA000099999`, `INA000088888`, `U67190MH2021PTC369999`).
   - Every verification record returns `is_demo: true` and is rendered in the UI with a prominent warning: *"Demonstration verification source — not a live statutory lookup"*.
   - No unauthorized web scraping of CAPTCHA-protected government portals (SEBI, MCA, RBI) is executed.
2. **Production Roadmap State**:
   - Official read-only API connectors (MCA21 API, SEBI intermediary directory webhooks) will plug into the `VerificationAdapter` interface as modular statutory providers.
   - When official services are unavailable, the system reports `UNAVAILABLE` rather than fabricating synthetic legitimacy or attempting brittle browser scraping.



