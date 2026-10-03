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

#### Node Relationship Statuses:
Every link in the chain is evaluated and tagged with one of four explicit states:
- **`VERIFIED`**: Independently substantiated by authoritative institutional records or cryptographic proof (e.g., domain matches official SEBI-registered broker directory).
- **`UNVERIFIED`**: Claimed by the entity or promotion, but no independent public or regulatory record could confirm it.
- **`CONTRADICTORY`**: Explicit mismatch detected between the claim and reality (e.g., claimed incorporation in 2012, but domain registered last week; or company registered to manufacture textiles while offering guaranteed crypto-forex returns).
- **`UNKNOWN`**: Insufficient data available to evaluate the node without further user-supplied artifacts.

---

### 5.2. Feature B: Scam Journey Reconstruction

Scams typically adhere to predictable social-engineering progressions. RakshaScan reconstructs the user's encounter as a **probable lifecycle pattern**:

```
[ 1. Initial Contact ]
      │ (Unsolicited SMS / WhatsApp invite / Sponsored ad)
      ▼
[ 2. Social Media / Channel Redirection ]
      │ (Redirected to curated VIP group / Instagram handle)
      ▼
[ 3. Landing Website ]
      │ (High-yield presentation / Fabricated testimonials)
      ▼
[ 4. Communication Channel ]
      │ (Private Telegram coordinator / "Mentor" contact)
      ▼
[ 5. Supposed Financial Expert ]
      │ (Fake analyst certificate / Impersonated SEBI research analyst)
      ▼
[ 6. Custom App / Platform ]
      │ (Off-market APK or rigged web dashboard showing simulated balances)
      ▼
[ 7. Initial Deposit Request ]
      │ (Personal UPI ID or individual savings bank account)
      ▼
[ 8. Apparent Profit Generation ]
      │ (Simulated astronomical gains displayed on UI)
      ▼
[ 9. Additional Payment Demands ]
      │ ("Tax clearance fee", "liquidity deposit", or "VIP unlocking fee")
      ▼
[ 10. Withdrawal Block / Cessation ]
        (Account frozen or handlers vanish)
```

> **Design Guardrail**: This pipeline is explicitly presented as a **reconstructed / possible pattern based on matching indicators**, NEVER asserted as an absolute or legally adjudicated fact.

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

## 6. Safe Next-Step Guidance Matrix

When risks or unverified links are identified, RakshaScan provides context-specific defensive playbooks:

- **Verification Protocol**: Direct links to official regulatory lookup tools (e.g., SEBI Recognized Intermediaries Portal, RBI Kehta Hai directory, MCA Company Master Data).
- **Asset Protection Measures**: Explicit instructions *never* to transfer funds to personal UPI handles or download third-party `.apk` packages.
- **Reporting Channels**: Pre-formatted incident summaries ready to copy-paste into the National Cyber Crime Reporting Portal (`cybercrime.gov.in`) or report via helpline `1930`.
- **Communication Containment**: Instructions on securing compromised messaging accounts and preserving chat logs as evidence.
