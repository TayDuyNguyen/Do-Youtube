"""
YouTube China Pipeline - Video Downloader
Tự động download video từ Bilibili, Douyin, và các nguồn TQ khác.

Usage:
    python download.py <url> [--platform bilibili|douyin|xiaohongshu|weibo]
    python download.py --batch urls.txt
"""

import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Đường dẫn project
PROJECT_ROOT = Path(__file__).parent.parent.parent
SOURCES_DIR = PROJECT_ROOT / "video_nguon"
CONFIG_DIR = PROJECT_ROOT / "cau_hinh"


def get_platform(url: str) -> str:
    """Tự động nhận diện platform từ URL."""
    platforms = {
        "bilibili.com": "bilibili",
        "b23.tv": "bilibili",
        "douyin.com": "douyin",
        "xiaohongshu.com": "xiaohongshu",
        "xhslink.com": "xiaohongshu",
        "weibo.com": "weibo",
    }
    for domain, platform in platforms.items():
        if domain in url:
            return platform
    return "other"


def download_video(url: str, platform: str = None):
    """Download video từ URL."""
    if not platform:
        platform = get_platform(url)

    output_dir = SOURCES_DIR / platform
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_template = str(output_dir / f"{today}_%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "--write-subs",
        "--sub-langs", "all",
        "--embed-metadata",
        "--no-overwrites",
        "-o", output_template,
        url
    ]

    print(f"📥 Downloading from {platform}: {url}")
    print(f"📁 Output: {output_dir}")
    print(f"🔧 Command: {' '.join(cmd)}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"\n✅ Download thành công!")
            # Tạo metadata file
            create_metadata(url, platform, output_dir, today)
        else:
            print(f"\n❌ Download thất bại! Return code: {result.returncode}")
    except FileNotFoundError:
        print("❌ yt-dlp chưa được cài đặt!")
        print("   Chạy: pip install yt-dlp")


def create_metadata(url: str, platform: str, output_dir: Path, date: str):
    """Tạo file metadata cho video đã download."""
    metadata = {
        "url": url,
        "platform": platform,
        "download_date": date,
        "status": "downloaded",
        "notes": ""
    }

    meta_file = output_dir / f"{date}_metadata.json"

    # Append nếu file đã tồn tại
    existing = []
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
            if not isinstance(existing, list):
                existing = [existing]

    existing.append(metadata)

    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"📝 Metadata saved: {meta_file}")


def batch_download(file_path: str):
    """Download nhiều video từ file text (mỗi dòng 1 URL)."""
    with open(file_path, "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"📋 Found {len(urls)} URLs to download")
    for i, url in enumerate(urls, 1):
        print(f"\n{'='*60}")
        print(f"📥 [{i}/{len(urls)}] Processing...")
        download_video(url)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python download.py <url>")
        print("  python download.py --batch urls.txt")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("❌ Cần chỉ định file chứa URLs")
            sys.exit(1)
        batch_download(sys.argv[2])
    else:
        platform = None
        if "--platform" in sys.argv:
            idx = sys.argv.index("--platform")
            platform = sys.argv[idx + 1]
        download_video(sys.argv[1], platform)
