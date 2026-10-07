**file**: docs/requirements/requirement-runtime-prerequisites.md  
**Status**: Active (Version 1.0.1)  
**Area**: runtime  
**Key**: `requirement-runtime-prerequisites`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare **host and Python runtime prerequisites** required to run AnimeDlp successfully. This product does **not** implement a privileged system `prerequisites` installer command; this file is the **documentation and validation SSOT** for what must already be present.

---

## 2. Core Rules (Mandatory)

### 2.1 Scope (honest product mode)

1. **MUST** document all external tools and libraries required at runtime.  
2. **MUST NOT** claim the product auto-installs system packages via root/sudo unless a future Active elev + install requirement is added.  
3. **MUST** separate **pip-installable** Python deps from any true **system binaries**. Download and extract need no system binary beyond CPython. `mpv` is optional. The `mpv` verb and menu row 2 need `mpv` on PATH whose `mpv --version` contains `mplayer2`. The product **MUST NOT** install that binary.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython | interpreter | package import + CLI | OS / pyenv / system Python |
| `requests` | pip package | HTTP session / fetch | `pyproject.toml` / pip |
| `beautifulsoup4` | pip package | HTML parse | `pyproject.toml` / pip |
| `lxml` | pip package | BS4 parser backend | `pyproject.toml` / pip |
| `yt-dlp` | pip package | media download | `pyproject.toml` / pip |
| `ChronicleLogger` | pip package | logging | `pyproject.toml` / pip |
| Network egress | host capability | reach supported sites + media CDNs | operator environment |

### 2.3 Validation expectations

4. **MUST** fail with an actionable message when required Python modules are missing (import gates in `main()`).  
5. **MUST** document that site pages may require a browser-obtained `cf_clearance` value (not auto-fetched by a privileged agent).  
6. **MUST** document supported hosts as domain peer (anime1.me / anime1.pw).

### 2.4 Privilege

7. **MUST NOT** require root to satisfy runtime prerequisites for normal use.  
8. Type 1 elevation for package install is **out of scope** for this product.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `pip install AnimeDlp` (when published); local `pip install -e .` / `pip install .` for checkout |
| **Declared pip deps** | ChronicleLogger≥1.2.3, requests, beautifulsoup4, yt-dlp, lxml |
| **System binary** | **none required** beyond CPython for download and extract. `mpv` is optional and is not installed by this product. The `mpv` verb and menu row 2 need an mplayer2 build on PATH (yt-dlp may use ffmpeg for some formats as its own optional tool — not claimed as AnimeDlp product auto-install) |
| **Auto install command** | **none** for OS packages |
| **Platform notes** | Linux primary; macOS/Windows OK when CPython + network available |
| **Product version** | 1.5.3 |
| **Startup checks** | Import gates in `cli.main()` for requests, BeautifulSoup, yt_dlp, lxml |
| **User docs** | Root `README.md` Required Dependencies / Requirements sections |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Assume deps may be missing.  
- **Principle 10 – Least privilege**: No root prerequisites command forced.  
- **Principle 2 – Intentional**: Pip vs system deps separated.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document before fail.  
- **Intentional:** No fake root install claim.  
- **Anti-fragile:** Works wherever Python + network exist.  
- **Over-protect:** No silent elev install.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Claim OS packages are installed by `pip install AnimeDlp` alone when not true.  
2. Add root package-manager elev without elev allowlist law and user order.  
3. Drop declared pip deps from tables while code still imports them.  
4. Store secrets in this file.  
5. Invent FFmpeg as a hard product gate unless code paths actually require a product-level `ffmpeg` check.

**Violating this rule is a critical honesty regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | All pip deps listed |
| AC-2 | Network egress noted |
| AC-3 | No false auto root-install claim |
| AC-4 | Import gates documented |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | Declared deps SSOT |
| `requirement-python-cli-interface` | Import gates |
| `requirement-download-ytdlp-pipeline` | yt-dlp usage |
| `requirement-domain-animedlp` | Host scope |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-RT-01** | `tests/test_prereqs.py` | **have** | missing module message path |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Runtime prerequisites for AnimeDlp |
| 2026-08-11 | Active 1.0.0 | Version 1.3.0; entry gate path honesty |
| 2026-10-05 | Active 1.0.0 | Product version cell aligned to **1.4.0** |
| 2026-10-05 | Active 1.0.0 | Product version cell aligned to **1.5.0** |
| 2026-10-06 | Active 1.0.0 | Product version cell aligned to **1.5.1** |
| 2026-10-07 | Active 1.0.0 | Product version cell aligned to **1.5.2** |
| 2026-10-07 | Active 1.0.1 | `mpv` is optional and is not installed by this product. Package **1.5.3** |

---

**Last Updated**: 2026-10-07  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
