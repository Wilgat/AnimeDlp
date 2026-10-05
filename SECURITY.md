# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.4.0 (current) | Yes |
| 1.3.1 | Yes |
| 1.3.0 | Best-effort; prefer upgrading to current |
| 1.2.x | Best-effort; prefer upgrading to current |
| 1.1.x | Best-effort; prefer upgrading to current |
| 1.0.x | Best-effort; prefer upgrading to current |

## Reporting a Vulnerability

Please **do not** open a public issue for security-sensitive reports when a private channel is available.

**Maintainer contact (email):** `wilgat.wong@gmail.com`

- Source of contact: product **author-email** SSOT in [`LICENSE.md`](./LICENSE.md) (Copyright line).
- Prefer email for vulnerability details, reproduction steps, and impact.
- You should receive an acknowledgment when the report is received and actionable.
- Do not include exploit weaponization guides in public channels.

## Security Design Principles (CIAO)

This project follows **[CIAO](https://github.com/cloudgen/ciao)** / **CIAO-Lite** defensive design. Security-relevant intent:

| Letter | Principle | Security application |
|--------|-----------|----------------------|
| **C** | **Caution** | Fail closed on unsupported hosts, missing Python deps, and Cloudflare 403. Do not claim success when extract/download fails. |
| **I** | **Intentional** | Host allowlist is explicit. Playback cookies limited to needed names. yt-dlp is the named download engine. |
| **A** | **Anti-fragile** | Retries and concurrent fragment options on downloads; session-based HTTP. |
| **O** | **Over-protect** | User-level CLI only (no product root elevation). No shell online-install channel. |

Full principles: [CIAO Defensive Programming](https://github.com/cloudgen/ciao) · agent contract: [CIAO-Lite](https://github.com/cloudgen/ciao-lite).

This section describes **design posture**. It is **not** a claim of third-party certification.

## Scope notes

- AnimeDlp is a **network-using** CLI that contacts supported anime video sites and media CDNs. Use only where you have the right to access content.
- Optional Cloudflare `cf_clearance` values are **session cookies** supplied by the operator — do not commit them to git.
- Verbose mode logs **redacted** cookie maps by default. `--extract` also redacts cookies unless `--show-cookies`. Still treat logs as sensitive; do not commit cookies.
- This product does **not** implement online shell install channels or companion `.sha256` download integrity for itself.
- Related product docs: [`README.md`](./README.md), [`LICENSE.md`](./LICENSE.md).
