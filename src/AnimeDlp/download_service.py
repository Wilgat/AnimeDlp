"""yt-dlp download service (L2 SRP) — cookie subset, referer, outtmpl."""

from typing import Dict, Optional

from .util import sanitize_filename

try:
    import yt_dlp
except ImportError:  # pragma: no cover
    yt_dlp = None


class YtDlpDownloadService:
    """Apply headers/cookies and download one media item via yt-dlp."""

    def __init__(self, user_agent: str, verbose: bool, output_dir: Optional[str], logger):
        self.user_agent = user_agent
        self.verbose = verbose
        self.output_dir = output_dir
        self.logger = logger

    def download(
        self, title: str, video_url: str, special_cookie: Optional[Dict] = None
    ) -> bool:
        """Download using yt-dlp. Returns True on success, False on failure."""
        self.logger.log_message(
            f"Downloading → {title}", level="INFO", component="downloader"
        )

        cookie_str = ""
        if special_cookie and isinstance(special_cookie, dict):
            parts = []
            for key in ["e", "h", "p"]:
                if key in special_cookie:
                    parts.append(f"{key}={special_cookie[key]}")
            cookie_str = "; ".join(parts)

        safe_title = sanitize_filename(title)
        if self.output_dir:
            outtmpl = f"{self.output_dir.rstrip('/')}/{safe_title}.%(ext)s"
        else:
            outtmpl = f"{safe_title}.%(ext)s"

        ydl_opts = {
            "outtmpl": outtmpl,
            "concurrent_fragment_downloads": 16,
            "retries": 10,
            "verbose": self.verbose,
            "http_headers": {
                "Referer": (
                    "https://anime1.me/"
                    if "anime1.me" in video_url
                    else "https://anime1.pw/"
                ),
                "User-Agent": self.user_agent,
            },
        }

        if cookie_str:
            ydl_opts["http_headers"]["Cookie"] = cookie_str

        if yt_dlp is None:
            self.logger.log_message(
                "yt_dlp is not available", level="ERROR", component="downloader"
            )
            return False

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return True
        except Exception as e:
            self.logger.log_message(
                f"Download failed for {title}: {e}",
                level="ERROR",
                component="downloader",
            )
            return False
