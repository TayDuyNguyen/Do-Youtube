"""
YouTube China Pipeline - Music Downloader
Tai nhac/background music tu SoundCloud va cac nguon duoc yt-dlp ho tro.

Usage:
    python music_download.py <url>
    python music_download.py <url> --format mp3
    python music_download.py <url> --source soundcloud
    python music_download.py --batch music_urls.txt

Notes:
    Chi tai nhac ban co quyen su dung hoac nhac duoc cap phep cho video cua ban.
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).parent.parent.parent
MUSIC_DIR = PROJECT_ROOT / "04_editing" / "assets" / "music"
METADATA_DIR = PROJECT_ROOT / "09_data" / "music_downloads"

SUPPORTED_FORMATS = {"best", "mp3", "m4a", "wav", "opus"}


def get_source(url: str) -> str:
    """Nhan dien nguon nhac tu URL."""
    host = urlparse(url).netloc.lower().replace("www.", "")
    sources = {
        "soundcloud.com": "soundcloud",
        "youtube.com": "youtube",
        "youtu.be": "youtube",
        "bandcamp.com": "bandcamp",
        "archive.org": "archive",
        "pixabay.com": "pixabay",
    }

    for domain, source in sources.items():
        if host == domain or host.endswith("." + domain):
            return source
    return "other"


def build_command(url: str, output_dir: Path, audio_format: str) -> list[str]:
    """Tao lenh yt-dlp de tai audio."""
    today = datetime.now().strftime("%Y-%m-%d")
    output_template = str(output_dir / f"{today}_%(title).180B [%(id)s].%(ext)s")
    ytdlp_cmd = ["yt-dlp"] if shutil.which("yt-dlp") else [sys.executable, "-m", "yt_dlp"]

    cmd = ytdlp_cmd + [
        "--ignore-errors",
        "--no-overwrites",
        "--embed-metadata",
        "--write-info-json",
        "--extract-audio",
        "--audio-quality",
        "0",
        "-o",
        output_template,
        url,
    ]

    if audio_format != "best":
        cmd[6:6] = ["--audio-format", audio_format]

    return cmd


def write_metadata(url: str, source: str, output_dir: Path, audio_format: str) -> None:
    """Luu log download de sau nay biet track nao da dung."""
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    meta_file = METADATA_DIR / f"{datetime.now().strftime('%Y-%m-%d')}_music_downloads.json"

    record = {
        "url": url,
        "source": source,
        "audio_format": audio_format,
        "output_dir": str(output_dir),
        "downloaded_at": datetime.now().isoformat(timespec="seconds"),
        "usage_status": "downloaded",
        "license_notes": "",
    }

    existing = []
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
            if not isinstance(existing, list):
                existing = [existing]

    existing.append(record)
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"Metadata saved: {meta_file}")


def download_music(url: str, source: str | None = None, audio_format: str = "mp3") -> bool:
    """Tai mot track/playlist audio."""
    if audio_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {audio_format}. Use: {', '.join(sorted(SUPPORTED_FORMATS))}")

    source = source or get_source(url)
    output_dir = MUSIC_DIR / source
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = build_command(url, output_dir, audio_format)

    print(f"Downloading music from {source}: {url}")
    print(f"Output: {output_dir}")
    print(f"Format: {audio_format}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
    except FileNotFoundError:
        print("yt-dlp chua duoc cai dat trong Python hien tai.")
        print("Chay: pip install yt-dlp")
        return False

    if result.returncode != 0:
        print(f"Download that bai. Return code: {result.returncode}")
        return False

    write_metadata(url, source, output_dir, audio_format)
    print("Download thanh cong.")
    return True


def batch_download(file_path: str, audio_format: str = "mp3") -> None:
    """Tai nhieu URL tu file text, moi dong 1 URL."""
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]

    print(f"Found {len(urls)} music URLs")
    for index, url in enumerate(urls, 1):
        print("\n" + "=" * 60)
        print(f"[{index}/{len(urls)}] Processing")
        download_music(url, audio_format=audio_format)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download music/audio for video editing assets.")
    parser.add_argument("url", nargs="?", help="Music URL, for example a SoundCloud track or playlist")
    parser.add_argument("--batch", help="Text file containing one music URL per line")
    parser.add_argument("--source", help="Override source folder name, e.g. soundcloud, pixabay")
    parser.add_argument(
        "--format",
        default="mp3",
        choices=sorted(SUPPORTED_FORMATS),
        help="Audio output format. Default: mp3",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.batch:
        batch_download(args.batch, args.format)
    elif args.url:
        download_music(args.url, args.source, args.format)
    else:
        print("Usage:")
        print("  python music_download.py <url>")
        print("  python music_download.py <url> --format mp3")
        print("  python music_download.py --batch music_urls.txt")
