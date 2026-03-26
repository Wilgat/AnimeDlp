#!/usr/bin/env python3
"""
Anime1 Downloader - Clean Class-based Implementation
Supports: anime1.me and anime1.pw

Fixed: Multiple cookies with same name ('e') conflict in requests CookieJar
"""

from ChronicleLogger import ChronicleLogger
import argparse
import sys
from urllib.parse import urlparse, urljoin
import json
import re
from typing import List, Tuple, Optional, Dict

# Try to import required dependencies with clear error messages
try:
    import requests
except ImportError:
    requests = None

try:
    import lxml
except ImportError:
    lxml = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class Anime1Downloader:
    CLASSNAME = "Anime1Downloader"
    MAJOR_VERSION = 1
    MINOR_VERSION = 0
    PATCH_VERSION = 0

    def __init__(self, args: argparse.Namespace, logger: ChronicleLogger):
        self.args = args
        self.session = requests.Session()

        # Setup headers and cookies
        self.headers = {
            'User-Agent': args.user_agent or (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
            )
        }

        self.cookies = {}
        if args.cloudflare:
            self.cookies['cf_clearance'] = args.cloudflare

        self.session.headers.update(self.headers)
        if self.cookies:
            self.session.cookies.update(self.cookies)

    def fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML with proper error handling"""
        try:
            r = self.session.get(url, timeout=25)
            if r.status_code != 200:
                if self.args.verbose:
                    print(f" [warn] HTTP {r.status_code} → {url}")
                return None
            return r.text
        except Exception as e:
            print(f" [error] Failed to fetch {url}: {e}")
            return None

    # ====================== anime1.me ======================
    def extract_anime1_me(self, main_url: str) -> List[Tuple[str, str, Dict]]:
        """Extract videos from anime1.me"""
        print(" [info] Using anime1.me extractor")

        videos = self._extract_api_paths(main_url)
        if not videos:
            return []

        result = []
        for title, apireq in videos:
            src, cookie = self._get_anime1_me_source(apireq)
            if src:
                full_src = 'https:' + src if src.startswith('//') else src
                result.append((title, full_src, cookie))
                if self.args.verbose:
                    print(f" [debug] Extracted: {title} → {full_src[:80]}...")
        
        return result

    def _extract_api_paths(self, url: str) -> List[Tuple[str, str]]:
        """Extract titles and data-apireq from anime1.me page"""
        try:
            if self.args.user_agent and self.args.cloudflare:
                resp = self.session.get(url)
            elif self.args.user_agent or self.args.cloudflare:
                print("[ERROR] Provide both --user-agent and --cloudflare or neither")
                sys.exit(1)
            else:
                print(" [warn] Missing user-agent/cf_clearance, Cloudflare may block")
                resp = self.session.get(url)

            if resp.status_code == 403:
                print("[ERROR] Blocked by Cloudflare")
                sys.exit(1)

            soup = BeautifulSoup(resp.text, 'lxml')
            
            titles = [t.get_text().strip() for t in soup.find_all(class_='entry-title')]
            videos = [v.get('data-apireq') for v in soup.find_all(class_='video-js')]

            if not videos or not videos[0]:
                print("[ERROR] Could not find data-apireq")
                sys.exit(1)
            if not titles or not titles[0]:
                print("[ERROR] Could not find titles")
                sys.exit(1)
            if len(titles) != len(videos):
                print(f"[ERROR] Title/video count mismatch: {len(titles)} titles vs {len(videos)} videos")
                sys.exit(1)

            return list(zip(titles, videos))

        except Exception as e:
            print(f" [error] Failed to extract API paths: {e}")
            return []

    def _get_anime1_me_source(self, apireq: str) -> Tuple[Optional[str], Optional[Dict]]:
        """Call anime1.me API to get video source and relevant cookies"""
        try:
            data = f'd={apireq}'
            response = self.session.post(
                'https://v.anime1.me/api',
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            result = json.loads(response.content.decode("utf-8"))
            src = result['s'][0]['src']

            # === BETTER LONG-TERM FIX ===
            # Extract only needed cookies safely (avoids CookieConflictError)
            # We only care about 'e', 'h', 'p' for anime1.me playback
            cookie_dict = {}
            for cookie in self.session.cookies:
                if cookie.name in ('e', 'h', 'p'):
                    cookie_dict[cookie.name] = cookie.value

            if self.args.verbose:
                print(f" [debug] API Response src: https:{src}")
                print(f" [debug] Relevant cookies: {cookie_dict}")
            
            return src, cookie_dict

        except Exception as e:
            print(f" [error] anime1.me API call failed: {e}")
            return None, None

    # ====================== anime1.pw ======================
    def extract_anime1_pw(self, main_url: str) -> List[Tuple[str, str]]:
        """Extract videos from anime1.pw"""
        print(" [info] Using anime1.pw extractor")
        html = self.fetch_html(main_url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        main = soup.find('main', id='main') or soup
        title_tag = main.find('h1', class_='entry-title')
        series_title = title_tag.get_text().strip() if title_tag else "anime1_pw_video"

        # Find episode pages
        episode_pages = []
        for a in main.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()
            if re.search(r'/\d+$|\?p=\d+', href) or any(x in text for x in ['下一集', '上一集', '[', ']']):
                full_url = urljoin('https://anime1.pw/', href)
                if full_url not in episode_pages and 'anime1.pw' in full_url:
                    episode_pages.append(full_url)

        if not episode_pages:
            episode_pages = [main_url]
            print(" [info] Single episode page detected")
        else:
            def get_episode_num(u):
                match = re.search(r'/(\d+)', u)
                return int(match.group(1)) if match else 999999
            episode_pages = sorted(set(episode_pages), key=get_episode_num)
            print(f" [info] Found {len(episode_pages)} episodes")

        videos = []
        for ep_url in episode_pages:
            page_html = self.fetch_html(ep_url)
            if not page_html:
                continue

            s = BeautifulSoup(page_html, 'lxml')
            ep_title_tag = s.find('h1', class_='entry-title')
            ep_title = ep_title_tag.get_text().strip() if ep_title_tag else series_title

            found_url = self._extract_video_url(s, page_html)

            if found_url:
                if found_url.startswith('//'):
                    found_url = 'https:' + found_url
                videos.append((ep_title, found_url))
                if self.args.verbose:
                    print(f" [debug] Extracted: {ep_title} → {found_url[:80]}...")
            else:
                print(f" [warn] Failed to extract video from {ep_url}")

        return videos

    def _extract_video_url(self, soup: BeautifulSoup, page_html: str) -> Optional[str]:
        """Try multiple methods to find video URL"""
        # 1. Direct <source> tag
        source = soup.find('source')
        if source and source.get('src'):
            return source['src']

        # 2. iframe player
        iframe = soup.find('iframe')
        if iframe and iframe.get('src'):
            iframe_url = urljoin('https://anime1.pw/', iframe['src'])
            iframe_html = self.fetch_html(iframe_url)
            if iframe_html:
                for ext in ['m3u8', 'mp4']:
                    match = re.search(rf'https?://[^\s"\'<>()]+?\.{ext}[^\s"\'<>()]*', iframe_html)
                    if match:
                        return match.group(0)

        # 3. Universal regex fallback
        for ext in ['m3u8', 'mp4']:
            match = re.search(rf'https?://[^\s"\'<>()]+?\.{ext}[^\s"\'<>()]*', page_html)
            if match:
                return match.group(0)

        return None

    # ====================== Download ======================
    def download_video(self, title: str, video_url: str, special_cookie: Optional[Dict] = None):
        """Download using yt-dlp"""
        print(f" [info] Downloading → {title}")

        cookie_str = ''
        if special_cookie and isinstance(special_cookie, dict):
            # anime1.me special cookies
            parts = []
            for key in ['e', 'h', 'p']:
                if key in special_cookie:
                    parts.append(f"{key}={special_cookie[key]}")
            cookie_str = '; '.join(parts)

        ydl_opts = {
            'outtmpl': f"{title}.%(ext)s",
            'concurrent_fragment_downloads': 16,
            'retries': 10,
            'verbose': self.args.verbose,
            'http_headers': {
                'Referer': "https://anime1.me/" if "anime1.me" in video_url else "https://anime1.pw/",
                'User-Agent': self.headers['User-Agent'],
            }
        }

        if cookie_str:
            ydl_opts['http_headers']['Cookie'] = cookie_str

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            print(f" [error] Download failed for {title}: {e}")

    # ====================== Main Logic ======================
    def run(self):
        url = self.args.url.strip().rstrip('/')
        print(f" [info] Processing: {url}")

        domain = urlparse(url).netloc.lower()
        is_anime1_me = 'anime1.me' in domain
        is_anime1_pw = 'anime1.pw' in domain

        if not (is_anime1_me or is_anime1_pw):
            print(" [error] URL must be from anime1.me or anime1.pw")
            sys.exit(1)

        print(f" [info] Detected site: {'anime1.me' if is_anime1_me else 'anime1.pw'}")

        all_videos = []

        if is_anime1_me:
            items = self.extract_anime1_me(url)
            for title, src, cookie in items:
                all_videos.append((title, src, cookie))
        else:
            items = self.extract_anime1_pw(url)
            for title, src in items:
                all_videos.append((title, src, None))

        print(f"\n [info] Total videos found: {len(all_videos)}\n")

        if self.args.extract:
            for title, src, cookie in all_videos:
                print(f"Title : {title}")
                print(f"URL   : {src}")
                if cookie:
                    print(f"Cookie: {cookie}")
                print("-" * 70)
            return

        # Download all videos
        for title, video_url, special_cookie in all_videos:
            self.download_video(title, video_url, special_cookie)

        print(" [info] All downloads completed!")


def main():
    appname = 'AnimeDlp'
    MAJOR_VERSION = 1
    MINOR_VERSION = 1
    PATCH_VERSION = 0

    # Create logger instance
    logger = ChronicleLogger(logname=appname)
    appname=logger.logName()    
    basedir=logger.baseDir()
    if logger.isDebug():
        logger.log_message(f"{appname} v{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION} ({__file__}) with the following:", component="main")
        logger.log_message(f">> {ChronicleLogger.class_version()}", component="main")

    # ====================== Dependency Checks ======================
    if requests is None:
        logger.log_message("[ERROR] 'requests' module is not installed.\n    Please install it using: pip install requests", level="FATAL", component="main")
        sys.exit(1)

    if BeautifulSoup is None:
        print(" [ERROR] 'beautifulsoup4' module is not installed.")
        print("         Please install it using: pip install beautifulsoup4 lxml")
        sys.exit(1)

    if yt_dlp is None:
        logger.log_message("[ERROR] 'yt_dlp' module is not installed.\n    Please install it using: pip install requests", level="FATAL", component="main")
        sys.exit(1)

    if lxml is None:
        logger.log_message("[ERROR] 'lxml' module is not installed.\n    Please install it using: pip install requests", level="FATAL", component="main")
        sys.exit(1)

    # ====================== Argument Parsing ======================
    parser = argparse.ArgumentParser(
        appname,
        formatter_class=argparse.RawTextHelpFormatter,
        description='Clean downloader for anime1.me and anime1.pw'
    )
    parser.add_argument("url", help="URL from anime1.me or anime1.pw")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable debug output")
    parser.add_argument('-x', '--extract', action='store_true', help="Extract URLs only (no download)")
    parser.add_argument('-cf', '--cloudflare', help="cf_clearance cookie value")
    parser.add_argument('-ua', '--user-agent', help="Custom User-Agent string")

    args = parser.parse_args()

    # ====================== Run Downloader ======================
    downloader = Anime1Downloader(args, logger)
    downloader.run()


if __name__ == "__main__":
    main()