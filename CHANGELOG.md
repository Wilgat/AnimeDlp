# Changelog

All notable changes to **AnimeDlp** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

Version SSOT: `pyproject.toml` + `src/AnimeDlp/__init__.__version__` (CLI reads package version only).

## [1.4.0] - 2026-10-05

### Changed

- On a terminal, a download no longer leaves the screen on yt-dlp's own bar. A flashing bullet shows the file being saved, the file total, the percent finished, and the time until finish. Each flash redraws that time. The line is erased when the downloads return.
- `--extract` and a non-terminal do not show that line. Off a terminal, yt-dlp keeps its own progress.

### Added

- Sample frames in `screenshots/` and a sample-operation section in the README.
- Checklist `docs/checklists/2026-10-05-checklist-download-progress.md` and review `docs/reviews/2026-10-05-download-progress-review.md`.
- `TP-ANIMEDLP-05` asserts the file count, the percent, and a time that changes before the line is erased.

---

## [1.3.1] - 2026-08-19

### Added

- Optional live-network extract suite **TP-ANIMEDLP-04** (`ANIMEDLP_LIVE_NET=1` + `ANIMEDLP_LIVE_URL`)
- Loopback HTTP integration download **TP-YTDLP-04** (no public network)

### Fixed

- **ADLP-NET-01:** live/integration proof now exists (optional extract; offline download fixture)
- **ADLP-DOC-02:** live SSOT surfaces say **1.3.1**; historical 1.1.0/1.2.0 reviews marked superseded

---

## [1.3.0] - 2026-08-11

### Changed (L2 OOP revision)

- **L2 multi-class SRP** on disk: `Anime1MeExtractor`, `Anime1PwExtractor`, `YtDlpDownloadService`, slim `Anime1Downloader` coordinator, thin `cli.main`
- Product law: `requirement-python-system-architecture` / `requirement-python-classes` updated to **L2 achieved**
- Portable molds added earlier in harness for domain URL-CLI, yt-dlp pipeline, python runtime prerequisites

### Added

- Tests: TP-ARCH-01/02, TP-CLASS-01/02 (`tests/test_architecture.py`); Core suite **29** cases
- Updated RTM / test-plan for architecture and classes peers

---

## [1.2.0] - 2026-08-11

### Fixed (product review revision)

- **ADLP-EXIT-01:** empty extract and download failures return non-zero exit; no false “All downloads completed!”
- **ADLP-ERR-02:** extractors raise `AnimeDlpError` instead of deep `sys.exit`; `main` maps to exit codes
- **ADLP-SEC-01:** verbose logs redact cookie values; extract prints redacted cookies unless `--show-cookies`
- **ADLP-VER-02:** single version SSOT via `__version__` (removed CLI MAJOR/MINOR/PATCH triples)
- **ADLP-IO-01:** episode titles sanitized for filesystem; optional `-o` / `--output-dir`
- **ADLP-ARCH-01:** split package into `cli.py`, `downloader.py`, `errors.py`, `util.py`

### Added

- Tests: TP-ERR-03/04, TP-SEC-01, TP-YTDLP-05 (Core suite now 25 cases)

### Security

- Cookie values redacted by default in logs and extract output; use `--show-cookies` only when needed.

---

## [1.1.0] - 2026-08-09

### Added

- Full product requirements set under `docs/requirements/` (class, domain, yt-dlp pipeline, CLI, packaging, structure, coding style, errors, runtime).
- Automated Core test suite under `tests/` (20 cases; mocked; no public network).
- Product reviews and TP maps under `docs/reviews/` (test plan, RTM, product + requirements reviews).
- Root `LICENSE.md`, `SECURITY.md`, and this changelog for specialized product hygiene.

### Changed

- Version aligned to **1.1.0** across packaging, package `__version__`, CLI constants, and README badge.
- Packaging metadata description/keywords corrected to anime site downloader (not unrelated video editing).
- Package public exports: `__version__` and `main` only (removed phantom `ChronicleLogger` re-export).
- `requires-python` tightened to **>=3.8** to match README and typing usage.
- Product README rewritten for install honesty (PyPI + local), supported hosts, and disclaimer.

### Fixed

- `__init__.py` import surface honesty.
- Version surface drift across CLI / package / README.

### Security

- Still user-level only; no Type 1 elevation. Session cookies may appear only under explicit verbose diagnostics — do not commit cookies.

---

## [1.0.1] - prior (PyPI)

### Added

- Initial PyPI-published package with `anime-dlp` console script.
- Extractors for anime1.me and anime1.pw with yt-dlp download path.

---

## [1.0.0] - prior

### Added

- Initial public baseline.
