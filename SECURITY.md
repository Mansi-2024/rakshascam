# RakshaScan — Security Architecture & Guidelines

> **SANGYAN 2026 Production-Oriented Prototype**  
> *Defensive Engineering, SSRF Mitigation, Isolation, and Privacy by Design*

---

## 1. Security Philosophy

Because RakshaScan is designed to evaluate potentially malicious websites, predatory schemes, and deceptive communications, the platform itself is exposed to adversarial inputs. The core security mandate is:

> **Never trust user input, never execute remote client code unsafely, and never allow the server to become an SSRF proxy.**

---

## 2. Privacy Principles & PII Handling

1. **Privacy by Design**:
   - RakshaScan evaluates financial risk, not individual user behavior.
   - Minimal data collection: no mandatory account creation or phone number verification required for running scans.
2. **PII Sanitization & Redaction**:
   - Ingested screenshots, message transcripts, or text payloads are passed through a PII scrubber prior to long-term database storage.
   - User identity, personal bank account details (belonging to the victim), Aadhaar/PAN, or personal contact info are masked (e.g., `user@****.com`, `XXXX-XXXX-1234`).
3. **Data Retention & Anonymization**:
   - Scan records are retained for threat intelligence and pattern analysis with all submitter identifiers detached.

---

## 3. Server-Side Request Forgery (SSRF) Protection

When users submit URLs for domain or metadata inspection, the backend must never execute indiscriminate HTTP requests:

### Technical Requirements for URL Resolution:
1. **Pre-Flight DNS Resolution & IP Filtering**:
   - Resolve DNS records before dispatching any HTTP socket.
   - Reject any target resolving to:
     - Loopback addresses (`127.0.0.0/8`, `::1`)
     - Private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)
     - Link-local and cloud metadata addresses (`169.254.169.254`, `fe80::/10`)
     - Broadcast or multicast spaces (`0.0.0.0`, `224.0.0.0/4`)
2. **Scheme Allowlist**:
   - Only `http://` and `https://` protocols are permitted. Schemes like `file://`, `gopher://`, `dict://`, `ftp://`, or `data://` are dropped immediately.
3. **Strict Redirect Enforcement**:
   - HTTP redirects are manually inspected. Every redirect hop must undergo re-resolution and IP filtering. Maximum allowed redirect hops: **3**.
4. **Network Sandboxing**:
   - Future background worker tasks performing external queries must operate in an isolated egress network where internal VPC endpoints are physically unreachable.

### Phase 2 Implementation Verification:
All pre-flight DNS and SSRF checks are operational in `backend/app/core/security.py` and covered by automated test suites in `backend/tests/test_url_validation.py`. The module rejects loopback, RFC 1918 private IPs, link-local, carrier NAT (100.64.0.0/10), 0.0.0.0/8, cloud metadata IPs (`169.254.169.254`, `100.100.100.200`), non-HTTP schemes, non-whitelisted ports, and IPv4-mapped IPv6 targets before any socket is initiated.

---

## 4. URL Analysis & Remote Resource Constraints

To protect backend workers from Denial of Service (DoS) and resource exhaustion when interacting with third-party web endpoints:

- **Strict Socket Timeouts**: Connect timeout: **3 seconds**; Read timeout: **7 seconds**. Total transaction cap: **10 seconds**.
- **Response Size Limits**: Stream truncation at **5 MB**. Any remote response exceeding 5 MB is halted and closed immediately.
- **Header & Content-Type Guards**: Binary blobs, heavy media streams, and executable formats (`.exe`, `.apk`, `.iso`) are aborted without buffering into server memory.

---

## 5. Malicious Webpage & Content Isolation

Future visual verification and DOM scraping (e.g., via Playwright / Chromium headless):

1. **No Code Execution on Host**:
   - Headless browser sessions must run in ephemeral, unprivileged container instances with `seccomp` profiles active.
2. **Script Execution Restrictions**:
   - JavaScript execution is constrained; web workers, service workers, WebRTC, and local storage access are disabled where possible.
3. **Sandbox Storage Isolation**:
   - Sandboxes operate on ephemeral RAM disks (`tmpfs`). All cookies, cache, and state are wiped immediately after the snapshot/scrape completes.
4. **Air-Gapped Rendering**:
   - Snapshots and OCR processing are performed offline on pre-rendered raster buffers rather than live browser frames.

---

## 6. File Upload Security (Screenshots & Evidence)

Users can submit screenshots of suspicious chats, ads, or certificates:

1. **MIME-Type & Magic Byte Validation**:
   - Enforce strict magic-number inspection (not relying on file extensions). Only `image/jpeg`, `image/png`, and `image/webp` are permitted.
2. **Payload Size Caps**:
   - Maximum upload size restricted to **10 MB** per artifact.
3. **Image Re-encoding & Stripping**:
   - All uploaded images are re-encoded using PIL / Pillow or Sharp to strip malicious EXIF metadata, embedded scripts, polyglot payloads, and malformed markers before downstream storage.
4. **Non-Executable Storage**:
   - Uploaded files are stored in object storage or isolated paths with execution permissions strictly disabled (`noexec`, non-public read).

---

## 7. Secrets Management

- **Zero Hardcoded Secrets**: Absolute ban on committing API tokens, database passwords, or cryptographic keys into version control.
- **Environment Separation**: Distinct `.env` configurations for development, testing, and production.
- **Runtime Secret Injection**: In production deployments, secrets are loaded via environment variables or secret vaults (e.g., HashiCorp Vault, AWS Secrets Manager, GitHub Secrets).
- **Leak Detection**: Pre-commit hooks and CI scans (e.g., `gitleaks` or `trufflehog`) will be configured to block accidental commits of credentials.

---

## 8. Logging, Auditability & Rate Limiting

- **Safe Logging (No Sensitive Data Leakage)**:
  - Application logs must never write raw auth headers, user credentials, or unredacted PII.
  - Log entries are structured (JSON format) with traceable request correlation IDs.
- **Rate Limiting**:
  - API endpoints are governed by rate-limiting rules (e.g., maximum 20 requests per minute per IP for public scan endpoints) to prevent automated abuse and scraper spamming.
- **Audit Logging**:
  - Verification decisions, regulatory queries, and evidence outputs maintain immutable audit timestamps for forensic integrity.

---

## 9. Phase 3 Extraction & Analysis Boundaries

Phase 3 introduces structured entity, claim, and relationship extraction with explicit security boundaries:

1. **No External Crawling or Link Following**:
   - Extraction operates strictly on the single in-memory HTML document retrieved during safe ingestion. RakshaScan does not crawl child links, follow external domains, or initiate recursive network activity.
2. **No Interactive Outreach**:
   - Extracted phone numbers, email addresses, WhatsApp handles, or Telegram contacts are treated strictly as static textual evidence. The backend never attempts to email, call, SMS, or ping extracted contacts.
3. **No Premature Registry Lookups**:
   - In Phase 3, regulatory references and registration numbers are extracted and organized with status `UNKNOWN`. No external lookups are dispatched to SEBI, MCA, RBI, or third-party APIs during this phase.
4. **Deterministic Regular Expressions**:
   - Entity and pattern extraction use bounded, non-backtracking regular expressions with length constraints to prevent ReDoS (Regular Expression Denial of Service).
5. **Separation of Observation and Adjudication**:
   - The extraction layer never issues a final fraud or safety declaration (`SCAM`, `SAFE`, `TRUST SCORE`). All findings are classified as observed signals awaiting authoritative Phase 4 verification.

---

## 10. Phase 4 Verification Security & Trust Mandates

The Authoritative Verification Architecture introduces strict security and anti-abuse safeguards:

1. **No Unauthenticated Web Scraping of Government / Regulatory Portals**:
   - RakshaScan strictly prohibits blind automated scraping of official statutory portals (e.g. `sebi.gov.in`, `mca.gov.in`, `rbi.org.in`).
   - The system **never** attempts to bypass visual or audio CAPTCHA, solve challenge tokens, or bypass session authentication.
   - When official machine-readable APIs are unavailable without authenticated enterprise credentials, adapters strictly report `UNAVAILABLE` rather than executing brittle, abusive scrapers.
2. **No Unofficial Third-Party Databases as Authority**:
   - Regulatory status may only be verified against confirmed, official statutory sources or designated enterprise API conduits (e.g. API Setu). Unofficial third-party aggregators or web scrapers are prohibited from granting `VERIFIED` status.
3. **No Interactive Contacting or Social Pinging**:
   - The system never contacts claimed phone numbers, emails, UPI handles, or messaging groups during verification.
4. **SSRF Guardrails on Verification Endpoints**:
   - Verification adapters use strictly pre-configured, immutable registry endpoints or internal mock URIs. Arbitrary user-controlled URLs can never be supplied as verification targets.
5. **Fault Isolation & Error Sanitization**:
   - Verification exceptions (timeouts, socket errors, connection resets) are caught at the engine boundary and translated to status `UNAVAILABLE`. Internal stack traces or database connection details are never leaked to the client.

---

## 11. Phase 5 Risk & Assessment Security Controls

1. **Non-Prejudicial Concern Assessments (No Libelous Verdicts)**:
   - RakshaScan produces evidence-backed concern assessments (`LOW_CONCERN`, `MODERATE_CONCERN`, `HIGH_CONCERN`, `INSUFFICIENT_EVIDENCE`), not legal fraud determinations.
   - The platform **never** outputs statements such as *"This is a scam"*, *"This company is fake"*, or arbitrary numerical "scam scores". All outputs describe observable evidence signals and verification states.
2. **Strict Evidence Provenance & Immutability**:
   - Every risk signal is strictly bound to one or more `EvidenceRecord` objects containing exact verbatim text excerpts observed directly on the target webpage or official registry.
   - AI-generated summaries cannot substitute for raw evidence. A signal without verifiable evidence provenance is structurally rejected.
3. **Deterministic & Auditable Evaluation**:
   - Risk signals are generated using transparent, deterministic rules (Rules 1–10). There are no black-box or non-deterministic statistical models influencing concern classification.
4. **Preservation of Uncertainty**:
   - The engine strictly enforces epistemic boundaries:
     - `NOT_FOUND ≠ FRAUD`: Inability to locate an entity in a registry query does not establish criminal intent.
     - `UNKNOWN ≠ SAFE`: Absence of negative records does not validate legitimacy.
     - `UNAVAILABLE ≠ NOT_FOUND`: Technical service disruption or lack of registry access is never equated to a missing registration.
5. **No Unauthorized or Intrusive Surveillance**:
   - RakshaScan does not collect or access banking credentials, OTPs, or payment account data.
   - It does not initiate phone calls, send messages, or scrape private chat platforms (WhatsApp, Telegram).
   - SSRF protections, response limits, and domain sanitization established in Phase 2 remain strictly active.

---

## 12. Phase 6 & 7 Security Safeguards & Trust Boundaries

### 12.1 Closed Data Boundary (No Out-of-Band Queries)
- **Operates Exclusively on Pipeline Artifacts**: The Trust Chain (`app.trust_chain`) and Scam Journey (`app.journey`) modules operate **strictly on data already obtained through the existing safe ingestion pipeline**.
- **No External Crawling**: The builders do not trigger secondary web crawls or spidering.
- **No Social Media Scraping**: External social handles (e.g. `t.me`, `wa.me`) are parsed as static textual URLs; no API queries, member counts, or private group logs are extracted.
- **No Payment Account Inquiries**: The engine does not ping UPI VPAs, perform penny-drop bank account lookups, query crypto balances, or inspect transaction histories.
- **No PII or Credential Harvesting**: The system never asks for, accepts, or stores OTPs, passwords, ATM PINs, netbanking credentials, or private keys.

### 12.2 Strict Truth & Evidence Mandates
1. *"Trust Chain relationships are established only when supported by available evidence."*
   - Fabricated links between entities and unobserved payment methods are strictly prevented. If no evidence connects a node, `NOT_OBSERVED` or `UNKNOWN` is mandatory.
2. *"Scam Journey Reconstruction represents a possible/reconstructed interaction pattern and is not a determination of fraud."*
   - The behavioral reconstruction model is strictly educational and advisory. The prominent mandatory disclaimer must accompany all journey renders.

---

## 13. Phase 8 Multi-Input Security, Privacy & Ingestion Controls

Phase 8 introduces user message submission and screenshot OCR while maintaining zero-trust architecture:

### 13.1 Privacy-by-Design & Temporary Artifact Lifecycle
1. **Zero Permanent Image Storage**:
   - Uploaded screenshot files are processed strictly in RAM (`io.BytesIO`).
   - Images are **never** written to local disk, temp directories, or permanent databases.
   - Image buffers are discarded immediately once text extraction concludes.
2. **Log Privacy & Redaction**:
   - Application loggers are strictly forbidden from logging raw message bodies, OCR text buffers, or base64 image strings.
   - Backend logging is restricted to operational metadata (e.g., input type, character count, image dimensions, execution duration).
3. **No Credential Harvesting**:
   - Prominently warns users never to upload OTPs, passwords, ATM PINs, CVVs, or card details.
   - Any sensitive authentication tokens accidentally submitted are treated as untrusted text and discarded after session analysis.

### 13.2 100% Local & Offline OCR (No Cloud Vision APIs)
- All optical character extraction operates exclusively on local compute via `PIL` and local offline libraries (`pytesseract`).
- The backend **never transmits user screenshots to cloud vision APIs, external OCR microservices, or third-party web endpoints**.

### 13.3 Non-Crawling URL Discovery
- URLs embedded in user messages or detected via OCR are parsed and structured as `LinkItemModel` objects for display and evidence provenance.
- **The system does NOT automatically crawl or fetch discovered URLs**.
- This eliminates uncontrolled recursive crawling, Denial of Service amplification, and inadvertent SSRF vector traversal.

### 13.4 Epistemic Integrity of OCR Evidence
- Text extracted from screenshots is classified as `source_type: "SCREENSHOT_OCR"`.
- OCR output is explicitly treated as **unverified user-observed text**, not statutory truth.
- Every screenshot analysis exposes the mandatory OCR notice:
  > *"Text extracted from the screenshot may contain OCR errors or omissions. Verify important identifiers against authoritative statutory sources."*

---

## 14. Phase 9 Safe Response & Recovery Security Guidelines

### 14.1 Zero Automated Assumptions of Victimhood
- The Safe Response Engine never assumes money was lost or credentials were leaked solely based on the presence of predatory text.
- Phrasing is conditional (*"If you have already transferred money..."*).
- Payment events (`PAYMENT_MADE`) on the incident timeline are restricted to explicit, affirmative user declarations.

### 14.2 Ephemeral Incident State
- User responses to *"Have you already sent money?"* or *"Have you shared sensitive credentials?"* are strictly ephemeral in the browser session.
- Responses are **never stored in persistent databases** or correlated with IP addresses.

### 14.3 Sensitive Authentication Credential Exclusion
- Recovery guidance explicitly instructs users to **never** upload or save passwords, OTPs, ATM PINs, UPI PINs, or CVV codes into RakshaScan.
- When credential compromise is declared, the system directs users to change passwords from an independent clean device through the provider's official portal.

---

## 15. Phase 10 Regional Safety & Epistemic Boundaries

### 15.1 Regional Language Safety
- Trilingual translation strictly maintains epistemic uncertainty:
  - English *"Authoritative corroboration was unavailable"* translates to Hindi *"यह दावा स्वतंत्र रूप से सत्यापित नहीं किया जा सका"* and Marathi *"अधिकृत नोंदीमध्ये या दाव्याची पडताळणी होऊ शकलेली नाही"*.
  - Strict prohibition against translating unverified claims into definitive fraud declarations (e.g. never *"यह फर्जी है"* or *"यह फ्रॉड है"*).
- Fictional demonstration badges remain clearly and unambiguously translated (*"काल्पनिक प्रदर्शन इनपुट"* / *"काल्पनिक प्रात्यक्षिक माहिती"*).

### 15.2 Identifier Invariance
- Regulatory license codes, CINs, URLs, phone numbers, payment handles, and evidence IDs remain invariant across all language views to prevent spoofing or misinterpretation.

---

## 16. Phase 11 Production Hardening, Abuse Prevention & Egress Boundaries

### 16.1 In-Process Rate Limiting & Resource Caps
- **Protection from Floods**: Endpoints are throttled via an in-memory sliding window rate limiter (`backend/app/core/rate_limit.py`).
  - URL scanning: 30 requests / minute
  - Message analysis: 30 requests / minute
  - Screenshot OCR: 15 requests / minute
- **Resource Exhaustion Defense**:
  - URLs > 2,048 chars rejected with `413 Content Too Large`.
  - Messages > 15,000 chars rejected with `413 Content Too Large`.
  - Images > 10 MB or > 8000x8000 pixels rejected with `413 Content Too Large`.

### 16.2 Image Format & Polyglot Prevention
- **Cryptographic Header Checks**: Inspects initial magic bytes (`PNG`, `JPEG`, `WEBP`) before passing data to Pillow to neutralize malicious polyglot or disguised executable uploads.
- **Decompression Bomb Defense**: Enforces maximum dimension checks (`8000 x 8000`) before decoding full pixel matrices into memory.

### 16.3 Defensive HTTP Headers
- Every FastAPI response attaches defensive HTTP headers:
  - `X-Content-Type-Options: nosniff`: Prevents MIME-type sniffing.
  - `X-Frame-Options: DENY`: Prevents clickjacking and framing.
  - `Referrer-Policy: strict-origin-when-cross-origin`: Restricts referrer information leakage.
  - `X-XSS-Protection: 1; mode=block`: Activates browser XSS filters.
  - `Permissions-Policy: geolocation=(), camera=(), microphone=()`: Blocks unwanted client hardware access.

### 16.4 Privacy Redaction in Operational Logs
- Query parameters containing credentials or tokens (`token`, `auth`, `password`, `key`, `otp`, `pin`, `cvv`) are dynamically redacted to `[REDACTED]` prior to logging.
- Raw message bodies, image buffers, and OCR strings are excluded from all logging streams.

### 16.5 Statutory Verification Boundaries (Demo vs Production)
- RakshaScan strictly prohibits unauthorized scraping or automated bypassing of government verification portals.
- In demonstration environments, the system queries seeded, synthetic fixtures explicitly identified as non-authoritative (`is_demo: true`).






