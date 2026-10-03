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
| **Phase 0: Foundation** *(Current)* | Project Blueprint & Safety Baseline | Repository structure, architecture specifications, security definitions, and configuration blueprints. |
| **Phase 1: Ingestion & Core Models** | Data Schema & Entity Extraction | Input ingestion contracts (URL, text, screenshot metadata), basic Pydantic validation schemas, and database migrations. |
| **Phase 2: Deterministic Verification** | Regulatory & Domain Checks | Registrars, DNS/SSL inspection, sandbox request boundaries, and regulator blacklist/whitelist matchers. |
| **Phase 3: Trust Chain & Risk Engine** | Relationship Graph & Scoring | Multi-node Trust Chain resolution, status flags (`VERIFIED`, `UNVERIFIED`, `CONTRADICTORY`, `UNKNOWN`), and evidence graph synthesis. |
| **Phase 4: Scam Journey Reconstruction** | Behavioral Pipeline Mapping | Temporal pattern matching across user contact milestones to highlight probable attack progressions. |
| **Phase 5: Interactive UX & Final Polish** | Next.js Interface & SANGYAN Demo | Comprehensive evidence dashboard, interactive chain visualizer, exportable PDF/JSON evidence dossier, and audit trail. |

---

## 5. Setup & Development Placeholders

### Prerequisites
- Node.js 18+ & npm / pnpm
- Python 3.11+
- PostgreSQL 15+

### Environment Configuration
```bash
# Clone the repository
git clone <repo-url>
cd rakshascan

# Prepare environment variables from template
cp .env.example .env
```

*(Detailed frontend and backend installation steps will be activated during subsequent implementation phases.)*

---

## 6. Core Security Principles

- **Zero-Trust Network Execution**: Ingested URLs and resources are never queried naively. All network interactions pass through SSRF-guarded, rate-limited, and sandboxed isolated handlers.
- **No Malicious Execution**: Webpage analysis is performed without executing unsafe client-side payloads; untrusted uploads are stripped of executable attributes and quarantined.
- **Privacy by Design**: Sensitive user input, financial account numbers, or personal identifying information (PII) are scrubbed and anonymized at intake.
- **Auditable Proof**: Assessment decisions are backed by deterministic verification records, preventing hallucinations from steering user financial actions.
