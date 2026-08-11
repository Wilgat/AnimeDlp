"""Small pure helpers (filename safety, cookie redaction)."""

import re
from typing import Dict, Mapping, Optional


def sanitize_filename(title: str, max_len: int = 180) -> str:
    """Make an episode title safe for use in yt-dlp outtmpl basenames."""
    if not title or not str(title).strip():
        return "anime_video"
    name = str(title).strip()
    # Path separators and traversal
    name = name.replace("\\", "_").replace("/", "_")
    name = name.replace("\x00", "")
    name = re.sub(r"\.\.+", ".", name)
    # Windows-forbidden / control-ish
    name = re.sub(r'[<>:"|?*]', "_", name)
    name = re.sub(r"[\x00-\x1f]", "", name)
    name = name.strip(" .")
    if not name or name in {".", ".."}:
        return "anime_video"
    if len(name) > max_len:
        name = name[:max_len].rstrip(" .")
    return name or "anime_video"


def redact_cookie_map(cookies: Optional[Mapping[str, str]]) -> Dict[str, str]:
    """Return cookie keys with values redacted for logs/stdout."""
    if not cookies:
        return {}
    out = {}
    for k, v in cookies.items():
        s = "" if v is None else str(v)
        if len(s) <= 4:
            out[str(k)] = "****"
        else:
            out[str(k)] = s[:2] + "…" + s[-2:] + f"(len={len(s)})"
    return out


def redact_secret(value: Optional[str]) -> str:
    """Redact a single secret string (e.g. cf_clearance)."""
    if not value:
        return ""
    s = str(value)
    if len(s) <= 4:
        return "****"
    return s[:2] + "…" + s[-2:] + f"(len={len(s)})"
