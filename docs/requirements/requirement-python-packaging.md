**file**: docs/requirements/requirement-python-packaging.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-packaging`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define packaging SSOT for the AnimeDlp Python distribution: **`pyproject.toml`**, metadata, dependencies, console entry points, and version consistency.

---

## 2. Core Rules (Mandatory)

### 2.1 Manifest SSOT

1. **`pyproject.toml` MUST** be the primary packaging manifest (PEP 517 / PEP 621).  
2. **MUST** declare: name, version, description, authors, license text, requires-python, dependencies, build-system, and console scripts.  
3. **MUST NOT** treat an ad-hoc `requirements.txt` as the primary product dependency SSOT.  
4. Legacy `setup.py` under build trees **MUST NOT** become a second source of runtime identity without deprecation plan.

### 2.2 Version SSOT

5. Package version in **`pyproject.toml`** and **`src/AnimeDlp/__init__.__version__`** **MUST** match when a release is claimed.  
6. Bumping either **MUST** update both in the same change (or automated single writer documented later).  
7. **MUST NOT** invent a third silent version constant without declaring the new SSOT.  
8. CLI-internal `MAJOR_VERSION` / `MINOR_VERSION` / `PATCH_VERSION` in `cli.py` **SHOULD** match package version when displayed; if they diverge, agents **MUST** treat package SSOT as authoritative for release claims until reconciled.

### 2.3 Dependencies

9. **MUST** declare runtime Python dependencies required for the shipped CLI.  
10. System tools **MUST NOT** be faked as pip packages when they are not — document under runtime prerequisites.  
11. **MUST NOT** commit real secrets or private index passwords into packaging files.

### 2.4 Entry points

12. **MUST** declare console script **`anime-dlp`** → `AnimeDlp.cli:main`.  
13. Entry function **MUST** remain a thin launch into product logic.

### 2.5 Metadata honesty

14. **`description` and keywords MUST** describe this product (anime site CLI downloader), not an unrelated video-editing product.  
15. **MUST** keep project URLs consistent with the public GitHub project when claimed.  
16. README Version badge **MUST** match packaging version when README claims complete.

### 2.6 Build / release helpers

17. Optional `build.sh` / Cython tooling **MAY** exist for maintainer packaging.  
18. **MUST** keep helper scripts consistent with `pyproject.toml` identity (project name AnimeDlp).  
19. Generated `build/` and `dist/` **MUST NOT** be treated as source SSOT.

### 2.7 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Manifest** | `pyproject.toml` |
| **Project name** | `AnimeDlp` |
| **Version** | `1.5.2` |
| **requires-python** | as declared in `pyproject.toml` (broad string today — README advertises **Python 3.8+**; agents re-verify before marketing) |
| **Dependencies** | `ChronicleLogger>=1.2.3`, `requests`, `beautifulsoup4`, `yt-dlp`, `lxml` |
| **Build backend** | `setuptools.build_meta` |
| **Console script** | `anime-dlp = AnimeDlp.cli:main` |
| **Homepage / repo** | `https://github.com/Wilgat/AnimeDlp` |
| **Maintainer build helper** | `build.sh` |
| **Optional Cython config** | `cy-master.ini` (maintainer tooling; not runtime package SSOT) |
| **License** | MIT (packaging claims MIT; ensure root LICENSE file present when publishing) |
| **Public package exports** | `__version__` (+ optional `main`); **MUST NOT** re-export undefined `ChronicleLogger` from `.cli` |
| **Metadata honesty** | Description/keywords must describe anime site downloader (not unrelated video editing) — aligned in 1.1.0 |
| **User docs** | Root `README.md` Installation must document `pip install AnimeDlp` / local install and console script `anime-dlp` |
| **README version badge** | Must match packaging version when README claims complete (**1.5.2**) |

### 2.8 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest for identity and entry.  
- **Principle 2 – Intentional**: Version dual-write is explicit.  
- **Principle 1 – Caution**: Metadata must not lie about product purpose.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Validate version dual SSOT on release.  
- **Intentional:** PEP 621 over ad-hoc manifests.  
- **Anti-fragile:** Console script + module entry.  
- **Over-protect:** No secrets in packaging files.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Remove or rename `anime-dlp` entry without CLI + README update.  
2. Let `__version__` and `pyproject.toml` diverge while claiming a release.  
3. Add private credentials to `pyproject.toml`.  
4. Replace packaging SSOT with only `requirements.txt`.  
5. Change product name silently across packaging and source package directory.  
6. Leave video-editing description as official packaging identity for this downloader product.

**Violating this rule is a critical packaging regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `pyproject.toml` present with name AnimeDlp |
| AC-2 | Console script `anime-dlp` declared |
| AC-3 | Dependencies include requests, beautifulsoup4, lxml, yt-dlp, ChronicleLogger |
| AC-4 | Version dual SSOT documented |
| AC-5 | Description matches anime downloader purpose (when debt fixed) |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-cli-interface` | Entry target |
| `requirement-python-project-structure` | Package path |
| `requirement-runtime-prerequisites` | Dep runtime meaning |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PKG-01** | packaging inspection | **have** | console script name |
| **TP-PKG-02** | packaging inspection | **have** | version equality |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Packaging SSOT + honesty debt notes for AnimeDlp |
| 2026-10-05 | Active 1.0.0 | Version cell and README badge cell aligned to **1.4.0** |
| 2026-10-05 | Active 1.0.0 | Version cell and README badge cell aligned to **1.5.0** |
| 2026-10-06 | Active 1.0.0 | Version cell and README badge cell aligned to **1.5.1** |
| 2026-10-07 | Active 1.0.0 | Version cell and README badge cell aligned to **1.5.2** |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
