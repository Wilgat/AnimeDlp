# AnimeDlp

**A clean and robust command-line downloader for specific anime video sites**

AnimeDlp allows you to easily extract direct video URLs or download episodes from supported anime video sites. It handles protection mechanisms and special cookie requirements gracefully, powered by `yt-dlp`.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

- Support for popular anime video sites (including API-based extraction)
- Automatically detects multi-episode series
- Extract video URLs only (`--extract`) or download directly
- Built-in handling for Cloudflare protection (`cf_clearance`)
- Safe cookie extraction to prevent common session conflicts
- Fast downloads using `yt-dlp` with concurrent fragment support
- Clean output with optional verbose debug mode

## Installation

Install via pip:

```bash
pip3 install AnimeDlp
```

### Required Dependencies
If you install by git clone, you need to add the following dependencies.
```bash
pip3 install requests beautifulsoup4 lxml yt-dlp ChronicleLogger
```

## Usage

### Basic Command

```bash
anime-dlp "https://your-anime-video-site-url-here"
```

### Options

```bash
Usage: anime-dlp [OPTIONS] URL

A clean downloader for supported anime video sites

Positional Arguments:
  url                   URL from a supported anime video site

Optional Arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable debug output
  -x, --extract         Extract URLs only (no download)
  -cf, --cloudflare CF  cf_clearance cookie value (for Cloudflare protection)
  -ua, --user-agent UA  Custom User-Agent string
```

### Examples

**1. Download episodes:**

```bash
anime-dlp "https://example-anime-site.com/your-series-url"
```

**2. Extract direct video URLs only:**

```bash
anime-dlp "https://example-anime-site.com/..." --extract
```

**3. Bypass Cloudflare protection:**

```bash
anime-dlp "https://example-anime-site.com/..." --cloudflare "your_cf_clearance_value_here" --verbose
```

**4. Custom User-Agent:**

```bash
anime-dlp "https://example-anime-site.com/..." --user-agent "Mozilla/5.0 ..."
```

## How It Works

- Parses episode information from the page
- Calls internal APIs when needed and safely handles required playback cookies
- Automatically finds and sorts episodes in series pages
- Uses **yt-dlp** for reliable, high-speed downloading

## Troubleshooting

- **Cloudflare block (403)**: Get a fresh `cf_clearance` cookie from your browser and use the `--cloudflare` flag.
- **Cookie-related errors**: The tool includes a robust fix for duplicate cookie name issues.
- **No video found**: Run with `--verbose` to see detailed logs.

## Requirements

- Python 3.8 or higher
- `requests`, `beautifulsoup4`, `lxml`, `yt-dlp`, and `ChronicleLogger`

## Project Links

- **Homepage**: https://github.com/Wilgat/AnimeDlp
- **Repository**: https://github.com/Wilgat/AnimeDlp
- **Issues**: https://github.com/Wilgat/AnimeDlp/issues

## Changelog

**v1.0.0** (Current)
- Initial public release
- Robust cookie handling implemented
- Support for major anime video sites
- CLI command `anime-dlp` added

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is intended for personal, educational use only. Please respect the terms of service of the websites you use it with. Downloading copyrighted material may be illegal in your jurisdiction.

---

Made for anime fans who want a simple downloading experience.
