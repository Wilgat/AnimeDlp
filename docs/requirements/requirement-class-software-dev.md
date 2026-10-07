**file**: docs/requirements/requirement-class-software-dev.md  
**Status**: Active (Version 1.0.0 – AnimeDlp software-development class law + residual stack)  
**Area**: class  
**Key**: `requirement-class-software-dev`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare this workspace as a **software-development** project class and hold the **residual collection** of software-engineering stack facts **not already owned** by more specific Active peer requirements: primary language, toolchain policy, package/build tooling, and runtime OS family.

This file is **class law + residual SSOT**, not a second copy of domain download features, yt-dlp ops, CLI surface, packaging tables, or error-handling tables (those stay on peer requirements).

---

## 2. Core Rules (Mandatory)

### 2.0 Project class membership

1. **MUST** treat this workspace as **software-development** (shippable software), not genesis-template and not server-maintenance.  
2. **MUST** use basename **`requirement-class-software-dev.md`** as the sole Active class-law file for this class.  
3. **MUST NOT** register an Active `requirement-class-server-maintenance.md` while class is software-development.  
4. **MUST** retain portable harness knowledge when present; specialized product knowledge lives in this and peer `requirement-*.md` files.  
5. **MUST** apply software-development SSOT/gate posture when claimed (identity, package ship surface, precommit when git is used — as applicable).  
6. **MUST NOT** invent hollow product docs solely to look specialized; collect real values or defer explicitly.

### 2.1 Residual collection principle (SSOT hygiene)

7. **MUST** treat this file as the **default home** for software-stack facts **not owned** by another Active requirement.  
8. **MUST NOT** duplicate full normative tables that already live in a more specific Active requirement. Prefer a **one-line pointer** to the peer requirement key.  
9. When a new specialized requirement **takes ownership** of a topic previously only listed here, **MUST** update this file in the **same change**: remove or shrink the residual entry and point to the new owner.  
10. **MUST NOT** leave contradictory stack facts across this file and peer requirements.

### 2.2 Programming language(s)

11. **MUST** declare at least one **primary programming language** for the ship unit.  
12. **SHOULD** list secondary languages only when they are real product law.  
13. **MUST** state whether the product is primarily: interpreted, compiled, polyglot, or package-multi-language.  
14. **MUST NOT** freeze a marketing product name as if it were the language name.

### 2.3 Compilers, interpreters, and toolchains

15. **MUST** declare the **target toolchain class** used to build or run the product.  
16. **MUST** state version policy as one of: unconstrained · minimum version · range · pinned.  
17. **SHOULD** record whether cross-compilation is in scope.  
18. **MUST** fail closed in CI/docs claims: do not claim “supports all interpreters” without tests or explicit unconstrained policy.

### 2.4 Project / package / build tools

19. **MUST** declare the **primary project or package tool** used for dependencies and builds.  
20. **MUST** declare how dependencies are resolved when the ecosystem supports lockfiles.  
21. **SHOULD** name the test runner and linter/formatter **classes** when they are project law.  
22. **MUST NOT** require a secret token or private registry password in this file.

### 2.5 Runtime and platform (residual)

23. **MUST** declare the intended **primary runtime/OS family** when not fully owned by another architecture requirement.  
24. **SHOULD** declare minimum CPU/arch support only when it is real product law.  
25. **MUST** separate **developer machine** toolchain requirements from **end-user runtime** requirements when they differ.

### 2.6 No-hardcode / dual policy (class file)

26. **MUST NOT** hard-code a single product/app brand, one org’s production hostname, or personal owner identity as universal core law.  
27. **MUST** put live product name, repo slug, and concrete stack choices in **Implementation Notes** after collection — complete when Status is Active.  
28. **MUST NOT** store secrets, PATs, or toy credentials in this file.

### 2.7 Implementation Notes (this project)

| Field | Value (AnimeDlp) |
|-------|------------------|
| **Project display name** | AnimeDlp |
| **Project class** | software-development |
| **Class requirement basename** | `requirement-class-software-dev.md` |
| **Primary language(s)** | Python |
| **Language role** | primary only for runtime package under `src/AnimeDlp/` |
| **Execution model** | **interpreted** package (PyPI-style); optional Cython/`build.sh` tooling for packaging experiments, not required for interactive CLI runtime |
| **Toolchain / interpreter** | CPython |
| **Toolchain version policy** | **range** declared in `pyproject.toml` (`requires-python`); live ship unit uses typing/`argparse` patterns consistent with **Python 3.8+** advertised in root README — agents **MUST** re-verify before advertising untested minor versions |
| **Cross-compile in scope?** | no (unless Cython extension build is deliberately re-enabled and tested) |
| **Primary project/package tool** | setuptools via PEP 517/621 **`pyproject.toml`** |
| **Lockfile policy** | **not used** as product law (no committed lockfile requirement) |
| **Test runner** | none as project law today (honest gap — `build.sh test` may invoke pytest when suites exist) |
| **Linter/formatter** | none as project law |
| **Primary runtime / OS family** | multi-OS where Python + network + yt-dlp run (documented focus: Linux; macOS/Windows when deps exist) |
| **Architectures supported** | any arch with CPython available |
| **Git surface** | used — remote `https://github.com/Wilgat/AnimeDlp` |
| **Ship surface** | installable Python package `AnimeDlp`; console script `anime-dlp`; module form `python -m AnimeDlp` |
| **Product version SSOT** | `src/AnimeDlp/__init__.py` → `__version__` and `pyproject.toml` `[project].version` **MUST** stay equal when either is bumped (current package: **1.5.3**). CLI-internal version constants in `cli.py` **MUST** not contradict without documentation |
| **Install mode** | **pip / local package** — not a shell online-install Type 0 product |
| **Type 1 elevation** | **intentionally absent** — no root/sudo product surface |
| **Author contact (non-secret)** | Wilgat Wong · `wilgat.wong@gmail.com` (also in `pyproject.toml`) |

**Residual ownership table:**

| Topic | Owner | Notes |
|-------|-------|--------|
| Project class membership | **this file** | Fixed |
| Primary language + toolchain policy | **this file** | Python / CPython |
| Package/build tool + lockfile | **this file** + `requirement-python-packaging` | packaging owns PEP 621 tables |
| Project layout (`src/` package) | `requirement-python-project-structure` | Do not duplicate |
| CLI entry / argparse surface | `requirement-python-cli-interface` | Do not duplicate |
| Domain surface (sites, extract/download workflow) | `requirement-domain-animedlp` | Four pillars |
| yt-dlp download / cookie ops | `requirement-download-ytdlp-pipeline` | Ops SSOT |
| Python coding style / temps | `requirement-python-coding-style` | Style + I/O |
| Error / fail-closed user messaging | `requirement-python-error-handling` | Do not duplicate |
| Host runtime deps (network tools via pip) | `requirement-runtime-prerequisites` | External deps |
| Online install / self-update / Type O | **intentionally absent** | Not a shell channel product |
| Type 1 sudoers / root elev | **intentionally absent** | No elevation law |

---

## 3. Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional**: Class and stack choices are explicit, not assumed from folder names.  
- **CIAO Principle 5 – SSOT**: Residual stack facts have one home until specialized requirements take ownership.  
- **CIAO Principle 1 – Caution**: Toolchain policies are declared; agents do not invent compilers or online install.  
- **CIAO Principle 21 – Dual Policies**: Portable core; filled Implementation Notes.  
- **CIAO Principle 4 (O) + Principle 20**: Protection Rule against dual stack SSOTs and wrong-class pollution.

---

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Assume network and site protection may fail until checked.  
- **Intentional**: Residual collection is deliberate — not a dump of every possible tool.  
- **Anti-fragile**: Packaging SSOT in `pyproject.toml` survives multi-env installs when versions stay consistent.  
- **Over-protect**: Protection rule prevents dual stack SSOTs and genesis/class confusion.

---

## 5. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Delete this file while the workspace remains **software-development** with other Active product requirements.  
2. Rename the specialized basename away from `requirement-class-software-dev.md` without an explicit class-model change.  
3. Hard-code secrets, personal tokens, or production host FQDNs into core rules as universal law.  
4. Duplicate full peer requirement bodies into this residual section.  
5. Leave Implementation Notes as hollow stubs when Status claims Active.  
6. Introduce Active **online-install** / remote **self-update** / shell **Type O** install-ensure law without explicit user order.  
7. Introduce Active **Type 1** sudoers / root elevation law without explicit user order and elev allowlist tables.  
8. Treat this file as server-maintenance allowlist law, or register an Active server-maintenance class file in parallel.  
9. Invent a second primary language SSOT that contradicts peer Python requirements.

**Violating any of these is considered a critical regression.**

---

## 6. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Workspace declared software-development with sole Active class file |
| AC-2 | Implementation Notes filled for AnimeDlp (Python, setuptools, pip package) |
| AC-3 | Residual ownership table points to peer REQs without full duplication |
| AC-4 | Online-install and Type 1 elev intentionally absent |
| AC-5 | Registered in `docs/requirements/index.md` Area `class` |

---

## 7. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-domain-animedlp` | Domain four pillars |
| `requirement-download-ytdlp-pipeline` | Download ops |
| `requirement-python-cli-interface` | CLI entry |
| `requirement-python-packaging` | PEP 621 / version |
| `requirement-python-project-structure` | Layout |
| `requirement-python-coding-style` | Style |
| `requirement-python-error-handling` | Errors |
| `requirement-runtime-prerequisites` | Runtime deps |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **n/a** | — | n/a | Class residual law; verified by registry + peer REQs present |

---

## 8. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial class law for AnimeDlp leaving genesis |
| 2026-10-05 | Active 1.0.0 | Product version cell aligned to **1.4.0** |
| 2026-10-05 | Active 1.0.0 | Product version cell aligned to **1.5.0** |
| 2026-10-06 | Active 1.0.0 | Product version cell aligned to **1.5.1** |
| 2026-10-07 | Active 1.0.0 | Product version cell aligned to **1.5.2** |
| 2026-10-07 | Active 1.0.0 | Product version cell aligned to **1.5.3** |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
