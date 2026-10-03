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
