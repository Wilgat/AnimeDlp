**file**: docs/requirements/requirement-python-classes.md  
**Status**: Active (Version 1.1.0 – AnimeDlp L2 multi-class SRP — implemented on disk)  
**Area**: python  
**Key**: `requirement-python-classes`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **class and module responsibility map** for AnimeDlp at **OOP level L2** (multi-class SRP): who owns extract, download, coordination, errors, and pure helpers.

This is **not** an L3 StateLogic+Attr mandate. Framework-grade orchestrator rules remain aspirational until L3 is ordered and architecture peer is updated.

Architecture boundaries and project type live in **`requirement-python-system-architecture`**.

---

## 2. Core Rules (Mandatory)

### 2.1 OOP rule for this product (L2)

1. **MUST** move toward **several classes with clear single jobs** (extract vs download vs entry).  
2. **MUST NOT** grow a single god-class that permanently owns HTML extract **and** yt-dlp lifecycle **and** CLI argv as the end state.  
3. **MUST** keep library paths free of `sys.exit` for domain failures — raise **`AnimeDlpError`** (or subclass); **`cli.main`** maps exit codes.  
4. **SHOULD** prefer composition (coordinator uses extractors + download service) over inheritance trees.  
5. StateLogic+Attr **MUST NOT** be claimed as required for L2; that is **L3**.

### 2.2 Current disk inventory (stay-honest — L2 complete)

| Symbol / module | Job | L2 status |
|-----------------|-----|-----------|
| `cli.main` | Argparse, dep gates, exit map | **OK** thin entry |
| `Anime1Downloader` (`downloader.py`) | Thin coordinator: session, route host, `run()`, facade delegates | **OK** |
| `Anime1MeExtractor` (`extractors/me.py`) | anime1.me extract | **OK** |
| `Anime1PwExtractor` (`extractors/pw.py`) | anime1.pw extract | **OK** |
| `YtDlpDownloadService` (`download_service.py`) | yt-dlp download + cookie header | **OK** |
| `AnimeDlpError` (`errors.py`) | Domain error + optional exit_code | **OK** |
| `util` helpers | filename sanitize, cookie redaction | **OK** |

### 2.3 L2 class / module map (normative)

| Class / module | Job (one sentence) | Depends on | Tests how |
|----------------|--------------------|------------|-----------|
| `cli` (`cli.py`) | Parse argv; dependency gates; map `AnimeDlpError` → process exit | coordinator | CLI smoke |
| `Anime1Downloader` (coordinator) | Route host; run extract then download or extract-only | extractors, download svc, logger, args | integration |
| `Anime1MeExtractor` | Extract `(title, url, cookie_dict)` from anime1.me | session, HTTP | TP-CLASS-02 |
| `Anime1PwExtractor` | Extract `(title, url)` from anime1.pw | session, HTML parse | domain / unit |
| `YtDlpDownloadService` | Apply headers/cookies; run `YoutubeDL` per item | yt_dlp, util | TP-ARCH-02, TP-YTDLP-* |
| `AnimeDlpError` | User-facing operational failure | — | error tests |
| `util` | Pure sanitize / redaction helpers | — | pure unit |

Coordinator **MAY** expose thin facade methods (`extract_anime1_me`, `download_video`) that **only** delegate — logic **MUST** live in collaborator classes.

### 2.4 Protection zones (class placement)

| Zone | Rule |
|------|------|
| Cookie header apply (`e`/`h`/`p`) | Download service / pipeline peer — not scattered prints of full jar |
| Host allowlist reject | Coordinator or extractors — fail closed |
| Exit codes | `cli.main` only |
| Filename sanitize | `util` or single shared helper |

### 2.5 Adding features (L2 discipline)

6. **New site family** → new extractor class/module + domain peer update — **MUST NOT** only paste a third path into an already overloaded method without map update.  
7. **New download option** → download service + pipeline peer — **MUST NOT** invent a second YoutubeDL call site without law.  
8. **New CLI flag** → CLI peer + thin wiring into config/args object — **MUST NOT** parse argv inside extractors.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Package** | `src/AnimeDlp/` |
| **Version** | `1.3.0` |
| **Target level** | **L2** (achieved) |
| **Current level** | **L2** multi-class SRP |
| **Coordinator** | `Anime1Downloader` in `downloader.py` (delegates only) |
| **Modules** | `extractors/me.py`, `extractors/pw.py`, `download_service.py`, `downloader.py`, `cli.py`, `errors.py`, `util.py` |
| **Entry** | `cli.py` |
| **Error type** | `AnimeDlpError` |
| **Helpers** | `util.sanitize_filename`, `util.redact_cookie_map` |
| **Architecture peer** | `requirement-python-system-architecture` |
| **Domain peer** | `requirement-domain-animedlp` |
| **Pipeline peer** | `requirement-download-ytdlp-pipeline` |
| **Product version** | `1.4.0` |

### 2.7 Why This Requirement Exists (CIAO)

- **Intentional**: Named jobs prevent god-class growth.  
- **SSOT**: One class map for L2.  
- **Caution**: Stay-honest about residual methods.  
- **Anti-fragile**: Test seams for extractors without full CLI.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not claim L2/L3 falsely.  
- **Intentional:** One job per class.  
- **Anti-fragile:** Unit seams for extract and download.  
- **Over-protect:** Cookie and exit-code placement locked.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Re-merge extract + download engine logic into one god-class as permanent design without law update.  
2. Claim **L3** / mandatory StateLogic+Attr from this REQ alone.  
3. Put `sys.exit` inside extractors/download service for domain failures.  
4. Scatter cookie-header construction outside the download path without pipeline peer update.  
5. Flatten the L2 map back to a single procedural `main` without architecture peer update and user order.  
6. Add features only by lengthening god methods when a new class is the map’s answer.

**Violating this rule is a critical OOP / SRP regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Target L2 class/module map present |
| AC-2 | Current inventory stay-honest |
| AC-3 | Exit mapping remains in `cli.main` |
| AC-4 | Cookie apply zone named |
| AC-5 | **L2 done:** distinct extractors + download service + thin coordinator on disk |
| AC-6 | Architecture peer Active and consistent |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-system-architecture` | Project type + level target |
| `requirement-python-coding-style` | Style conventions |
| `requirement-python-project-structure` | Layout |
| `requirement-python-error-handling` | Error categories |
| `requirement-domain-animedlp` | Host extract narrative |
| `requirement-download-ytdlp-pipeline` | Download ops |
| `requirement-python-cli-interface` | Entry / flags |
| `docs/requirements/index.md` | Registry |

## Design-time verification

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLASS-01** | `tests/test_architecture.py` | **have** | coordinator composes collaborators |
| **TP-CLASS-02** | `tests/test_architecture.py` | **have** | Me extractor unit seam without CLI |
| **TP-YTDLP-01..03** | `tests/test_download_pipeline.py` | **have** | download service behavior |
| **TP-ANIMEDLP-01..02** | domain tests | **have** | host / extract-only |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-11 | Active 1.0.0 | L2 class map law (design+REQ; migration phased) |
| 2026-08-11 | Active 1.1.0 | L2 implemented on disk; product **1.3.0** |
| 2026-10-05 | Active 1.1.0 | Product version cell aligned to **1.4.0** |

---

**Last Updated**: 2026-10-05  
**Owner**: Wilgat Wong  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
