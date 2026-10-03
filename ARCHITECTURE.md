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

## 3. Backend Layer (FastAPI & Python)

- **Framework**: FastAPI (Python 3.11+) taking advantage of asynchronous I/O (`asyncio`) for parallel analysis pipelines.
- **Data Validation**: Strict Pydantic v2 schemas for all request payloads, internal data transfers, and response objects.
- **Core Modules**:
  - `api/v1/endpoints/`: Clean REST endpoints for scans, health checks, report retrieval, and registry inquiries.
  - `services/orchestrator.py`: Coordinates the parallel dispatch of AI extraction and deterministic verification.
  - `services/ai_layer/`: Encapsulated extraction and summarization modules.
  - `services/verification/`: Pluggable adapters for registrars, network protocols, and regulatory sources.
  - `services/engines/`: Implementation of the Evidence Engine, Risk Engine, Trust Chain, and Scam Journey matcher.

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

## 5. Verification Layer (Authoritative & Deterministic)

The Verification Layer provides the ground truth through verifiable, auditable checks:

### Deterministic Subsystems:
1. **Infrastructure & Network Verification**:
   - Domain age and registrar inspection via RDAP/WHOIS.
   - DNS record resolution (A, AAAA, MX, TXT/SPF/DKIM) to verify email sender legitimacy.
   - SSL/TLS certificate chain auditing (Issuer, SAN match, validity span, Let's Encrypt vs. Extended Validation).
   - ASN and IP geolocation checks to uncover suspicious offshore routing for domestic financial services.
2. **Official Regulatory Registry Adapters**:
   - **MCA Adapter**: Corporate Identity Number (CIN) format validation and lookup against active company master data.
   - **SEBI Adapter**: Cross-referencing claimed registration numbers against registered Stock Brokers, Portfolio Managers, Research Analysts, and Investment Advisers.
   - **RBI Adapter**: Checking Non-Banking Financial Company (NBFC) registers and Payment System Operator approvals.
3. **Payment Identity Cross-Validation**:
   - Checking whether beneficiary UPI VPAs or bank accounts match the registered corporate entity name or resolve to unverified individual accounts.

---

## 6. Core Engines

### 6.1. The Evidence Engine
- Collects raw outputs from both the AI Layer and the Verification Layer.
- Constructs the **Trust Chain Graph**:
  - Connects nodes: `Claim` → `Entity` → `Registration` → `Official Identity` → `Website` → `App` → `Social Account` → `Payment Identity`.
  - Determines node and edge statuses based strictly on deterministic rules:
    - `VERIFIED`: Both claim and official record exist and match.
    - `UNVERIFIED`: Claim exists without matching official verification.
    - `CONTRADICTORY`: Claim directly contradicts authoritative records.
    - `UNKNOWN`: Incomplete or unresolvable node.
- Compiles the final **7-Point Evidence Assessment**.

### 6.2. The Risk Engine
- Evaluates systemic risk without relying on subjective arbitrary scores.
- Heuristic Rules evaluate:
  - Severity of broken links in the Trust Chain.
  - Presence of high-risk contradictions (e.g., claimed SEBI license belonging to a different firm, or domain registered < 14 days ago).
  - Unrealistic financial promises (e.g., guaranteed returns on equity/crypto).
  - High-pressure channels (e.g., sole communication via private Telegram or WhatsApp).
- Reconstructs the **Scam Journey**:
  - Compares identified evidence markers against common scam archetypes (e.g., "Pig Butchering / Task Scam", "Fake IPO Share Allocation", "Unauthorized Forex/Crypto App").
  - Identifies the current observed milestone and projected future trap stages.

---

## 7. Data Flow: From Submission to Dossier

```
1. [User Input] ───────────────────────────┐
                                           │
2. [Security Gateway: SSRF & Limits] ──────▼
                                     ┌─────────────┐
                                     │ Raw Payload │
                                     └──────┬──────┘
                       ┌────────────────────┴───────────────────┐
                       ▼                                        ▼
             ┌───────────────────┐                    ┌───────────────────┐
             │     AI Layer      │                    │ Verification Layer│
             │ - Extracts claims │                    │ - Resolves domain │
             │ - Extracts entities│                    │ - Queries records │
             │ - Parses text/OCR │                    │ - Validates SSL   │
             └─────────┬─────────┘                    └─────────┬─────────┘
                       │ Claims & Entities                      │ Ground Truth
                       └────────────────────┬───────────────────┘
                                            ▼
                               ┌─────────────────────────┐
                               │     Evidence Engine     │
                               │  - Cross-validates data │
                               │  - Solves Trust Chain   │
                               │  - Generates Proof Tree │
                               └────────────┬────────────┘
                                            ▼
                               ┌─────────────────────────┐
                               │       Risk Engine       │
                               │  - Detects Conflicts    │
                               │  - Maps Scam Journey    │
                               │  - Computes Heuristics  │
                               └────────────┬────────────┘
                                            ▼
                               ┌─────────────────────────┐
                               │  PostgreSQL Storage     │
                               │  (Store Scan & Dossier) │
                               └────────────┬────────────┘
                                            ▼
                               ┌─────────────────────────┐
                               │ UI Dashboard Delivery   │
                               │ (Interactive Evidence)  │
                               └─────────────────────────┘
```
