# AnimeDlp

**A clean and robust command-line downloader for specific anime video sites**

AnimeDlp extracts direct video URLs or downloads episodes from supported anime video sites. It handles common protection cookies and session needs gracefully, and uses **yt-dlp** for reliable media download.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.3.1-green)
![License](https://img.shields.io/badge/license-MIT-blue)
[![PyPI](https://img.shields.io/pypi/v/AnimeDlp.svg)](https://pypi.org/project/AnimeDlp/)
[![GitHub stars](https://img.shields.io/github/stars/Wilgat/AnimeDlp?style=social)](https://github.com/Wilgat/AnimeDlp)

**Philosophy:** [CIAO](https://github.com/cloudgen/ciao) / [CIAO-Lite](https://github.com/cloudgen/ciao-lite) defensive design.

## Features

- Support for **anime1.me** and **anime1.pw** (API and HTML extract paths)
- Multi-episode series discovery where pages expose episode links
- Extract URLs only (`--extract`) or download directly
- Optional Cloudflare assist (`cf_clearance` + User-Agent)
- Safe playback-cookie subset for anime1.me API cookies
- Fast downloads via **yt-dlp** with concurrent fragment support
- Clean logging with optional verbose debug mode

## Installation

### From PyPI

```bash
pip3 install AnimeDlp
```

### From a local checkout

```bash
pip3 install -e .
# or
pip3 install .
```

### Required dependencies

Declared in `pyproject.toml` and installed with the package:

- `requests`, `beautifulsoup4`, `lxml`, `yt-dlp`, `ChronicleLogger`

Python **3.8+** is required (`requires-python` in packaging).

## Usage

### Basic command

```bash
anime-dlp "https://anime1.me/your-series-or-episode-url"
# or
python -m AnimeDlp "https://anime1.pw/your-page-url"
```

### Options

```text
Usage: anime-dlp [OPTIONS] URL

A clean downloader for anime1.me and anime1.pw

Positional Arguments:
  url                   URL from anime1.me or anime1.pw

Optional Arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable debug output (cookie values redacted in logs)
  -x, --extract         Extract URLs only (no download)
  -o, --output-dir DIR  Directory for downloads (default: current directory)
  -cf, --cloudflare CF  cf_clearance cookie value (for Cloudflare protection)
  -ua, --user-agent UA  Custom User-Agent string
  --show-cookies        Print full playback cookies with --extract (default: redacted)
```

### Examples

**1. Download episodes:**

```bash
anime-dlp "https://anime1.me/..."
```

**2. Extract direct video URLs only:**

```bash
anime-dlp "https://anime1.me/..." --extract
```

**3. Bypass Cloudflare protection:**

```bash
anime-dlp "https://anime1.me/..." --cloudflare "your_cf_clearance_value" --user-agent "Mozilla/5.0 ..." --verbose
```

## How it works

1. Validates the host (`anime1.me` or `anime1.pw` only).  
2. Parses episode information / API tokens from the page.  
3. For anime1.me, calls the site API and applies needed playback cookies safely.  
4. Either prints sources (`--extract`) or downloads with **yt-dlp**.

## Troubleshooting

- **Cloudflare block (403):** Get a fresh `cf_clearance` from your browser and pass `--cloudflare` with a matching `--user-agent` when required.  
- **Cookie-related errors:** The tool uses a fixed cookie-name subset for me API downloads.  
- **No video found:** Run with `--verbose` for detailed logs.  
- **Unsupported host:** Only anime1.me / anime1.pw are accepted.

## Development / tests

```bash
pip3 install -e . pytest
python3 -m pytest -q tests/
```

Product law: `docs/requirements/`. TP map: `docs/reviews/test-plan.md`.

## Project links

- **Homepage / Repository:** https://github.com/Wilgat/AnimeDlp  
- **Issues:** https://github.com/Wilgat/AnimeDlp/issues  
- **PyPI:** https://pypi.org/project/AnimeDlp/

## Version

**1.3.0** — SSOT: `pyproject.toml` and `src/AnimeDlp/__init__.py` (`__version__`).

## License

MIT — see [`LICENSE.md`](./LICENSE.md).

## Security

See [`SECURITY.md`](./SECURITY.md) for reporting contact and design posture.

## Disclaimer

This tool is intended for **personal, educational use** only. Respect the terms of service of the websites you use it with. Downloading copyrighted material may be illegal in your jurisdiction.

---

Made for anime fans who want a simple downloading experience.
