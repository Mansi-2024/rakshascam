# RakshaScan — Hackathon Demonstration & Judge Evaluation Guide

> **Project Title:** RakshaScan  
> **One-Line Description:** Evidence-based, multimodal financial trust verification and scam-resilience platform for Indian retail investors.  
> **Target Audience:** Non-institutional investors, citizens navigating WhatsApp/Telegram investment groups, SMS offers, and suspicious financial advisory websites across Bharat.

---

## 1. Recommended Demonstration Scenario

The primary recommended demonstration uses a **Fictional High-Yield Investment Offer** presented via copied message or screenshot. This scenario directly reflects the real-world fraud vectors targeted at retail citizens across India (unregistered advisories, fake SEBI claims, guaranteed returns, deposit pressure, and advance withdrawal fees).

### Why this is the optimal demo:
1. **Multimodal Capability:** Exercises WhatsApp/SMS copied text and local OCR screenshot ingestion.
2. **Deterministic Intelligence:** Triggers 6 distinct signal categories simultaneously without speculative scoring.
3. **End-to-End Pipeline:** Traverses Extraction → Statutory Verification → Risk Assessment → Financial Trust Chain → Scam Journey Reconstruction → Safe Response → Recovery Playbook.
4. **Bharat-First UX:** Showcases instant vernacular switching across **English**, **हिन्दी (Hindi)**, and **मराठी (Marathi)** alongside the **Plain-Language ("Simple explanation")** mode.

---

## 2. Exact Demonstration Inputs

### Option A: Copied Financial Message (Primary Recommended Demo)
Click **Load Fictional Example** under the **Copied Message** tab or paste the following text:

```text
URGENT: SEBI approved guaranteed investment opportunity.
Earn 25% monthly with zero risk.
Only 10 investor slots remaining.
Deposit ₹20,000 today to activate your account.
To withdraw your profit, pay a refundable processing tax.
Official portal: https://example-finance.test
```

### Option B: Local Screenshot OCR
Under the **Screenshot OCR** tab, click **Load Fictional Example**. RakshaScan dynamically generates a synthetic promotional banner image in-memory with embedded text and executes 100% local, offline OCR.

### Option C: Website URL Analysis
Under the **Website URL** tab, click the fictional demonstration target `https://example-finance.test`. The system executes safe HTTP ingestion with full SSRF protection.

---

## 3. Expected Analysis Flow & Screen-by-Screen Progression

```
[User Input] 
      │
      ▼
[Phase 8 Multi-Input Normalization]
      │
      ▼
[Structured Extraction] (Entities, Claims, Regulatory Refs, Signals)
      │
      ▼
[Statutory Verification] (Synthetic Seeded Fixture Lookup)
      │
      ▼
[Evidence-Backed Risk Assessment] (HIGH_CONCERN + Primary Reasons)
      │
      ▼
[Financial Trust Chain] (8-Node Relationship Resolution)
      │
      ▼
[Scam Journey Reconstruction] (Observed vs Suspected Stage Mapping)
      │
      ▼
[Safe Response & Recovery] (Action State + Traceable Next Steps)
      │
      ▼
[Bharat-First Vernacular Translation] (Instant Trilingual + Simple Mode)
```

---

## 4. Key Features to Highlight to Judges

1. **Deterministic, Explainable Risk Engine (No Black-Box "Scam Scores")**:
   - RakshaScan does **not** emit arbitrary percentage scores (e.g. "92% Scam").
   - Clearly points to concrete, explainable findings: *Guaranteed return promise detected*, *Deposit pressure detected*, *Withdrawal fee friction observed*.
2. **Epistemic Distinction: Observation vs. Verification**:
   - Extracting *"SEBI Approved"* simply records that the phrase was claimed.
   - Verification independently evaluates whether an authoritative record corroborates that claim.
3. **The Financial Trust Chain**:
   - Graph-based resolution establishing whether the claimed advisor, registration number, domain name, and settlement accounts share verified ownership or exhibit identity contradictions.
4. **Scam Journey Reconstruction**:
   - Reconstructs the chronological behavioral stages (*First Contact* → *Financial Claim* → *Deposit Request* → *Withdrawal Friction*), explicitly differentiating between *Observed in text* and *Suspected pattern*.
5. **Contextual Safe Response & Recovery Playbook**:
   - Answers *"What should the user safely do next?"* via actionable defensive recommendations (`PAUSE`, `DO_NOT_SEND_ADDITIONAL_MONEY`, `PRESERVE_EVIDENCE`, `CONTACT_BANK`, `REPORT`).
   - Ephemeral interactive controls (*"Have you already sent money?"*) dynamically reveal the 5-step recovery drawer.
6. **Bharat-First Localization & Plain-Language Mode**:
   - Instant client-side translation into Hindi and Marathi.
   - One-click toggle transforming dense statutory terminology into everyday language without losing nuance.
7. **Production Hardening & Abuse Defenses**:
   - Zero-trust SSRF protection (private IPs, cloud metadata blocked).
   - In-process sliding-window rate limiting (`url`: 30/min, `message`: 30/min, `screenshot`: 15/min).
   - In-memory image processing (no permanent disk or database storage).
   - Defensive HTTP headers and privacy-sanitized operational logs.

---

## 5. Claims Strictly NOT to Make (Boundaries)

To maintain ethical integrity and regulatory compliance, do **NOT** claim:
- ❌ **"RakshaScan is an investment advisor or stock broker"**: RakshaScan does not provide buy/sell/hold stock tips or portfolio management.
- ❌ **"RakshaScan is a judicial fraud authority"**: The platform provides analytical safety guidance, not legal or prosecutorial determinations.
- ❌ **"Live SEBI / MCA registry lookup"**: The current MVP uses synthetic demonstration fixtures. Do not claim real-time live queries to government databases.
- ❌ **"100% Fraud Detection Guarantee"**: Always preserve epistemic uncertainty; negative results do not guarantee absolute safety.

---

## 6. Mandatory Synthetic Verification Disclaimer

Every instance of verification in the demo environment displays:

> **⚠️ DEMO VERIFICATION:** Derived from synthetic test database records for architectural evaluation. Does not represent a live regulator confirmation.

Judges should be informed that in a production deployment, these adapters will connect to authentic government open-data APIs (e.g. MCA21 V3, SEBI intermediary webhooks) using the existing modular `VerificationAdapter` architecture.

---

## 7. Recommended 3–5 Minute Demonstration Sequence

| Timestamp | Screen / Action | Voiceover / Talking Point |
| :--- | :--- | :--- |
| **0:00 - 0:45** | **Landing Page & Positioning** | "Welcome to RakshaScan. Across India, millions of retail investors are lured into predatory investment schemes via WhatsApp, SMS, and fake advisory websites. Existing security tools scan for malware, but miss financial fraud. RakshaScan bridges this gap by verifying financial trust and guiding safe user action." |
| **0:45 - 1:30** | **Message Ingestion & Extraction** | Click **Copied Message** → Click **Load Fictional Example** → Click **Analyze**. "Notice how our engine extracts structured entities, regulatory claims (SEBI registration), and financial promises without executing remote scripts or sending data to cloud vision servers." |
| **1:30 - 2:30** | **Assessment, Trust Chain & Scam Journey** | Scroll through **Assessment** and click into **Trust Chain** & **Scam Journey**. "Rather than an unexplainable scam score, RakshaScan explains *why* the content is risky. The Financial Trust Chain highlights identity disconnects, while the Scam Journey maps the predatory lifecycle from initial contact to withdrawal fee friction." |
| **2:30 - 3:30** | **Safe Response & Recovery** | Scroll to **What should you do now?** and toggle *"Have you already sent money? -> Yes"*. "RakshaScan doesn't just diagnose; it protects. We provide evidence-linked safe actions. When a user indicates they may have already transferred money, RakshaScan immediately activates the 5-step recovery protocol to halt further loss within the golden hour." |
| **3:30 - 4:15** | **Bharat-First Localization** | Switch language to **हिन्दी** or **मराठी** in the Navbar, then toggle **Simple explanation**. "India invests in its own languages. RakshaScan provides zero-latency native translation and a plain-language explanation mode that simplifies legal jargon while preserving critical uncertainty." |
| **4:15 - 5:00** | **Architecture & Wrap-Up** | Show **GET /health** and summary specs. "Built with FastAPI, Next.js, zero-trust SSRF sandboxing, and in-process rate limiting, RakshaScan is ready to safeguard digital Bharat." |

---

## 8. Backup Plan if External / Local Dependencies Fail

1. **Pre-Seeded Mock Dossier**: The frontend includes a fallback demo assessment preview directly on the homepage (`lib/mockData.ts`), ensuring visual continuity even if the backend process is completely offline.
2. **Synthetic Screenshot Generation**: The screenshot demo dynamically draws a test canvas in the browser without requiring external image downloads.
3. **Self-Contained Offline OCR**: Local OCR gracefully falls back to synthetic inspection metadata if Tesseract is not installed on the host operating system.

---

## 9. Local Startup Commands

### Start Backend (Terminal 1):
```bash
cd backend
# Optional virtual environment activation: .venv\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Verify backend health: `http://localhost:8000/health` (returns `{"status": "ok"}`)

### Start Frontend (Terminal 2):
```bash
cd frontend
npm run dev
```
Open: `http://localhost:3000`

### Run Complete Automated Test Suite:
```bash
# Backend pytest suite (125 tests)
cd backend
pytest -v

# Frontend lint & production build
cd frontend
npm run lint
npm run build
```
