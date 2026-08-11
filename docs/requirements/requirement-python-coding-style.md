**file**: docs/requirements/requirement-python-coding-style.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-coding-style`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define **Python coding style and defensive conventions** for AnimeDlp: how agents and maintainers write Python so logging, HTTP, cookie, and package surfaces stay safe and maintainable, without duplicating domain or yt-dlp pipeline tables.

Pipeline-specific download apply is owned by **`requirement-download-ytdlp-pipeline`**.

---

## 2. Core Rules (Mandatory)

### 2.1 General style (this product)

1. **MUST** keep the installable package under `src/AnimeDlp/` with thin module entry (`__main__` / console script → `cli.main`).  
2. **MUST** cite only live `docs/requirements/requirement-*.md` keys in product-source law comments — never templates or skills as behavioral authority.  
3. **SHOULD** use clear function **General Purpose** docstrings on public helpers.  
4. **MUST** fail closed with user-visible messages on expected errors (unsupported host, missing deps, Cloudflare block, empty extract).  
5. Logging **SHOULD** go through **ChronicleLogger** for durable diagnostics; user-facing extract listings **MAY** use direct `print` for readability.  
6. **OOP level:** **L2** multi-class SRP is **current law and disk shape** (thin `cli` + coordinator + extractors + download service + helpers). Full StateLogic+Attr remains **L3 aspirational** only. **MUST NOT** force a whole-file rewrite solely for style while working behavior holds. **MUST NOT** collapse L2 back to a god-class without architecture/classes peer updates.

### 2.2 HTTP and cookie handling

7. **MUST** use a session object for repeated site requests when the ship unit does so.  
8. **MUST** keep cookie subset logic centralized (pipeline peer) when building download Cookie headers.  
9. **MUST NOT** hard-code live user secrets; Cloudflare values come from CLI flags only.

### 2.3 Temporary files / publish

10. When intermediate files are introduced (future), **MUST** prefer same-mount staging and **`shutil.move`** for cross-mount-safe publish.  
11. Current product primarily writes finals via **yt-dlp** `outtmpl` directly — no intermediate promote path required today.  
12. **MUST NOT** invent fixed predictable temp basenames in cwd for multi-run concurrency without uniqueness.

### 2.4 Package exports

13. **`__init__.py` MUST** export only real public symbols that exist.  
14. **MUST NOT** re-export undefined names (e.g. claiming `ChronicleLogger` from `.cli` when not defined there).

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Package** | `AnimeDlp` |
| **Primary modules** | `cli.py`, `downloader.py`, `download_service.py`, `extractors/{me,pw}.py`, `errors.py`, `util.py`, `__main__.py`, `__init__.py` |
| **Architecture shape** | **L2**: thin `cli.main` + coordinator + extractors + `YtDlpDownloadService` + helpers — not L3 |
| **Architecture / classes peers** | `requirement-python-system-architecture`, `requirement-python-classes` |
| **OOP levels vocabulary** | `python-oop-style-levels` (L0–L3) |
| **Logging** | ChronicleLogger |
| **HTTP** | `requests.Session` |
| **HTML** | BeautifulSoup + lxml |
| **Download engine** | yt-dlp (pipeline peer) |
| **Temp/promote path today** | none (engine writes final name) |
| **Gate checklist (cite ID when audit publish paths)** | **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** if intermediate publish is added later |
| **Version** | package `1.3.0` |
| **Public exports** | `__version__` and `main` only (no phantom `ChronicleLogger` re-export) — fixed in 1.1.0 |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed; no secret hardcodes.  
- **Principle 2 – Intentional**: Class + main shape is declared.  
- **Principle 5 – SSOT**: One coding-style home.  
- **Principle 4 (O)**: Protect working code from unsolicited rewrites.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Cookie and dependency failures are loud.  
- **Intentional:** Logger + session patterns named.  
- **Anti-fragile:** Avoid fragile export re-exports.  
- **Over-protect:** Respect working code; no style-only rewrites.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Force a full StateLogic (L3) rewrite without explicit user order and L3 law.  
2. Collapse L2 collaborators back into a single god-class without peer law update.  
3. Cite templates/skills as product-source behavioral authority.  
4. Store secrets in style docs or code.  
5. Reintroduce multi-name CookieJar collisions as “simpler” cookie apply.  
6. Leave `__init__.py` exporting undefined symbols when claiming package cleanliness.

**Violating this rule is a critical style regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Package under `src/AnimeDlp/` |
| AC-2 | Product comments cite live requirement keys only |
| AC-3 | Fail-closed expected errors |
| AC-4 | No undefined public re-exports in `__init__.py` when fixed |
| AC-5 | Download cookie rules remain on pipeline peer |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-download-ytdlp-pipeline` | Cookie/download apply |
| `requirement-python-error-handling` | Error messaging |
| `requirement-python-project-structure` | Layout |
| `requirement-python-system-architecture` | Level target + boundaries |
| `requirement-python-classes` | SRP class map |
| `requirement-domain-animedlp` | Domain features |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-STYLE-01** | `tests/test_package_exports.py` | **have** | `__init__` exports only real symbols |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Coding style + export honesty for AnimeDlp |
| 2026-08-11 | Active 1.0.0 | L2 target peers; stay-honest L1→L2 transitional |
| 2026-08-11 | Active 1.0.0 | L2 on disk; product **1.3.0** |

---

**Last Updated**: 2026-08-11  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
