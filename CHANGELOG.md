# Changelog

All notable changes to **AnimeDlp** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

Version SSOT: `pyproject.toml` + `src/AnimeDlp/__init__.__version__`.

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
