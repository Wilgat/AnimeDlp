"""anime1.pw extract path (episode crawl + HTML/iframe/regex sources)."""

import re
from typing import List, Optional, Tuple
from urllib.parse import urljoin

from ..errors import AnimeDlpError

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


class Anime1PwExtractor:
    """Extract (title, source_url) from anime1.pw pages."""

    def __init__(self, session, args, logger):
        self.session = session
        self.args = args
        self.logger = logger

    def fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML with proper error handling."""
        try:
            r = self.session.get(url, timeout=25)
            if r.status_code != 200:
                self.logger.log_message(
                    f"HTTP {r.status_code} → {url}", level="WARN", component="fetch"
                )
                return None
            return r.text
        except Exception as e:
            self.logger.log_message(
                f"Failed to fetch {url}: {e}", level="ERROR", component="fetch"
            )
            return None

    def extract(self, main_url: str) -> List[Tuple[str, str]]:
        """Extract videos from anime1.pw."""
        if BeautifulSoup is None:
            raise AnimeDlpError(
                "'beautifulsoup4' is required for anime1.pw extraction"
            )

        self.logger.log_message(
            "Using anime1.pw extractor", level="INFO", component="extractor"
        )

        html = self.fetch_html(main_url)
        if not html:
            return []

        soup = BeautifulSoup(html, "lxml")
        main = soup.find("main", id="main") or soup
        title_tag = main.find("h1", class_="entry-title")
        series_title = title_tag.get_text().strip() if title_tag else "anime1_pw_video"

        episode_pages = []
        for a in main.find_all("a", href=True):
            href = a["href"]
            text = a.get_text().strip()
            if re.search(r"/\d+$|\?p=\d+", href) or any(
                x in text for x in ["下一集", "上一集", "[", "]"]
            ):
                full_url = urljoin("https://anime1.pw/", href)
                if full_url not in episode_pages and "anime1.pw" in full_url:
                    episode_pages.append(full_url)

        if not episode_pages:
            episode_pages = [main_url]
            self.logger.log_message(
                "Single episode page detected", level="INFO", component="extractor"
            )
        else:

            def get_episode_num(u):
                match = re.search(r"/(\d+)", u)
                return int(match.group(1)) if match else 999999

            episode_pages = sorted(set(episode_pages), key=get_episode_num)
            self.logger.log_message(
                f"Found {len(episode_pages)} episodes",
                level="INFO",
                component="extractor",
            )

        videos = []
        for ep_url in episode_pages:
            page_html = self.fetch_html(ep_url)
            if not page_html:
                continue

            s = BeautifulSoup(page_html, "lxml")
            ep_title_tag = s.find("h1", class_="entry-title")
            ep_title = ep_title_tag.get_text().strip() if ep_title_tag else series_title

            found_url = self._extract_video_url(s, page_html)

            if found_url:
                if found_url.startswith("//"):
                    found_url = "https:" + found_url
                videos.append((ep_title, found_url))
                if self.args.verbose:
                    self.logger.log_message(
                        f"Extracted: {ep_title} → {found_url[:80]}...",
                        level="DEBUG",
                        component="extractor",
                    )
            else:
                self.logger.log_message(
                    f"Failed to extract video from {ep_url}",
                    level="WARN",
                    component="extractor",
                )

        return videos

    def _extract_video_url(self, soup, page_html: str) -> Optional[str]:
        """Try multiple methods to find video URL."""
        source = soup.find("source")
        if source and source.get("src"):
            return source["src"]

        iframe = soup.find("iframe")
        if iframe and iframe.get("src"):
            iframe_url = urljoin("https://anime1.pw/", iframe["src"])
            iframe_html = self.fetch_html(iframe_url)
            if iframe_html:
                for ext in ["m3u8", "mp4"]:
                    match = re.search(
                        rf'https?://[^\s"\'<>()]+?\.{ext}[^\s"\'<>()]*', iframe_html
                    )
                    if match:
                        return match.group(0)

        for ext in ["m3u8", "mp4"]:
            match = re.search(
                rf'https?://[^\s"\'<>()]+?\.{ext}[^\s"\'<>()]*', page_html
            )
            if match:
                return match.group(0)

        return None
