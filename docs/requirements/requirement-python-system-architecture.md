**file**: docs/requirements/requirement-python-system-architecture.md  
**Status**: Active (Version 1.1.0 – AnimeDlp L2 multi-class PyPI execution — implemented)  
**Area**: python  
**Key**: `requirement-python-system-architecture`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **high-level system architecture** for AnimeDlp as a **PyPI Execution** Python CLI: project-type classification, execution model, module boundaries, privilege, and **OOP level target**.

This file is the architecture SSOT for **shape and boundaries**. Class inventory and SRP map live in **`requirement-python-classes`**. Coding conventions live in **`requirement-python-coding-style`**. Domain and download ops stay on their peers.

---

## 2. Core Rules (Mandatory)

### 2.1 Project type classification

1. **MUST** treat this product as a **PyPI Execution Project** (pip/local package CLI), not a Web API system, not a long-running daemon, and not a shell online Type O install product.  
2. **MUST NOT** require a dedicated non-login system user or a special “Python Project Root” on `sys.path` for normal use.  
3. The tool **MUST** run with the privileges of the **invoking user** (Type 0).

### 2.2 OOP level (ladder)

4. **Architecture level: L2** (multi-class SRP) per product ladder vocabulary (`python-oop-style-levels`) — **achieved on disk** as of product **1.3.0**.  
5. **Current disk shape (stay-honest):** thin `cli.main` + coordinator `Anime1Downloader` + `Anime1MeExtractor` / `Anime1PwExtractor` + `YtDlpDownloadService` + pure helpers (`util`, `errors`).  
6. **MUST** keep extract, download, and CLI concerns on distinct classes/modules (see classes peer).  
7. **L3** (StateLogic+Attr orchestrator + central output/path SSOT) remains **aspirational** — **MUST NOT** claim L3 without Active L3 law and framework on disk.  
8. Further level migrations (e.g. L3) **MUST** be surgical and **MUST NOT** be style-only mass rewrites without user order.

### 2.3 Execution model

9. Primary entry: console script **`anime-dlp`** → `AnimeDlp.cli:main` and module entry `python -m AnimeDlp`.  
10. `main()` **MUST** stay thin: logger init, dependency import gates, argparse, construct coordinator, map errors to exit codes.  
11. **MUST NOT** introduce a long-running server process or Docker management in core scope without updating this REQ.  
12. No Type 1 elevation for core extract/download.

### 2.4 Module boundaries (L2 target)

| Concern | Owner (target) | Must not own |
|---------|----------------|--------------|
| Argv + exit codes | `cli` | Site HTML parse; yt-dlp lifecycle |
| Site extract (me / pw) | extractor classes / modules | Full CLI flags; packaging |
| yt-dlp download + cookie header apply | download service | Host allowlist narrative |
| Coordination (route host → extract → download) | thin coordinator class | Packaging SSOT |
| Pure helpers | `util` | Network I/O |
| Domain errors | `errors` | Process `sys.exit` inside library paths |

13. Domain host catalog narrative remains **`requirement-domain-animedlp`**.  
14. yt-dlp option and cookie safety tables remain **`requirement-download-ytdlp-pipeline`**.

### 2.5 Path and storage

15. Default download writes are **cwd-relative** via yt-dlp `outtmpl` (pipeline peer).  
16. User-specific durable paths (if added later) **MUST** resolve through a named path/logger helper — **MUST NOT** scatter hard-coded `~/.…` paths in extractors.

### 2.6 Privilege model

17. Type 0 only for extract/download/help.  
18. Type 1/2 operations **MUST NOT** appear without new elev law and user order.

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Package** | `AnimeDlp` (`src/AnimeDlp/`) |
| **Product version** | `1.4.1` |
| **Classification** | PyPI Execution CLI |
| **Current OOP level** | **L2** multi-class SRP |
| **Target OOP level** | **L2** (current); L3 optional future |
| **L3** | Not claimed; optional future |
| **Entry** | `cli.main` / `__main__` / console `anime-dlp` |
| **Coordinator** | `Anime1Downloader` in `downloader.py` |
| **L2 modules** | see `requirement-python-classes` class map |
| **Logger** | ChronicleLogger |
| **Privilege** | Type 0 only |
| **Domain peer** | `requirement-domain-animedlp` |
| **Pipeline peer** | `requirement-download-ytdlp-pipeline` |
| **Classes peer** | `requirement-python-classes` |
| **Style peer** | `requirement-python-coding-style` |

### 2.8 Why This Requirement Exists (CIAO)

- **Intentional**: PyPI CLI boundaries named so agents do not import web-service patterns.  
- **SSOT**: One architecture home for level target and execution model.  
- **Caution**: Stay-honest about L1 residual until split lands.  
- **Over-protect**: No unsolicited L3 rewrite.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Assume normal-user invocation and missing deps.  
- **Intentional:** L2 target and thin entry are deliberate.  
- **Anti-fragile:** Module boundaries survive feature growth.  
- **Over-protect:** Explicit non-claims for L3 and elev.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Introduce a dedicated system user or `sys.path` project-root hack for normal runs.  
2. Collapse L2 back so one class owns extract **and** download engine **and** CLI permanently without law update.  
3. Claim **L3** without StateLogic+Attr (or declared equivalent) and central output SSOT on disk.  
4. Apply Web API / daemon architecture without updating this REQ.  
5. Hard-code storage paths in business logic when a resolver exists.  
6. Force style-only rewrite of working L1 residual without user order.  
7. Move full domain host tables or full yt-dlp option tables into this file (peers own them).

**Violating this rule is a critical architecture regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Classified as PyPI Execution CLI |
| AC-2 | Thin entry (`cli.main`) documented |
| AC-3 | Current OOP level **L2** stated honestly with module evidence |
| AC-4 | Type 0 only for core ops |
| AC-5 | Module boundary table present; peers named for domain/pipeline |
| AC-6 | Classes peer L2-done signal met on disk |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-classes` | SRP class map + L2 split jobs |
| `requirement-python-coding-style` | Style conventions |
| `requirement-python-project-structure` | Layout paths |
| `requirement-python-cli-interface` | Argv / entry |
| `requirement-domain-animedlp` | Domain surface |
| `requirement-download-ytdlp-pipeline` | Download ops |
| `requirement-python-error-handling` | Exit/error mapping |
| `requirement-class-software-dev` | Class residual stack |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ARCH-01** | `tests/test_architecture.py` + structure | **have** | L2 modules importable |
| **TP-ARCH-02** | `tests/test_architecture.py` | **have** | download service unit seam without full run |
| **TP-CLI-01** | `tests/test_cli.py` | **have** | thin entry smoke |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-11 | Active 1.0.0 | L2 target architecture law (design+REQ) |
| 2026-08-11 | Active 1.1.0 | L2 implemented; product **1.3.0** |
| 2026-10-05 | Active 1.1.0 | Product version cell aligned to **1.4.0** |
| 2026-10-05 | Active 1.1.0 | Product version cell aligned to **1.4.1** |

---

**Last Updated**: 2026-10-05  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
