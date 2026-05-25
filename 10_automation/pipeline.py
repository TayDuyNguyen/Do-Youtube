"""
YouTube China Pipeline - Full Pipeline Runner
Chạy toàn bộ pipeline từ download đến voice generation.

Usage:
    python pipeline.py <url>                     # Chạy full pipeline
    python pipeline.py <url> --steps download     # Chỉ download
    python pipeline.py <url> --steps download,transcribe  # Download + transcribe
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Thêm path để import các module khác
sys.path.insert(0, str(Path(__file__).parent.parent))

from download.download import download_video, get_platform
from transcribe.transcribe import transcribe
from voice.voice import generate_voice_edge


def run_pipeline(url: str, steps: list = None):
    """Chạy pipeline đầy đủ hoặc từng bước."""
    all_steps = ["download", "transcribe", "voice"]
    if steps is None:
        steps = all_steps

    print("=" * 60)
    print("🚀 YouTube China Pipeline")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"🔗 URL: {url}")
    print(f"📋 Steps: {', '.join(steps)}")
    print("=" * 60)

    results = {}

    # Step 1: Download
    if "download" in steps:
        print("\n" + "=" * 60)
        print("📥 STEP 1: DOWNLOAD")
        print("=" * 60)
        platform = get_platform(url)
        download_video(url, platform)
        results["download"] = True
        print("\n⏭️ Sau bước này:")
        print("   → Kiểm tra video trong 01_sources/")
        print("   → Tiếp tục với transcribe")

    # Step 2: Transcribe
    if "transcribe" in steps:
        print("\n" + "=" * 60)
        print("🎙️ STEP 2: TRANSCRIBE")
        print("=" * 60)
        print("⚠️ Cần chỉ định path video đã download")
        print("   Chạy riêng: python transcribe/transcribe.py <video_path>")
        results["transcribe"] = "manual"

    # Step 3: Rewrite (manual)
    if "rewrite" in steps or steps == all_steps:
        print("\n" + "=" * 60)
        print("✍️ STEP 3: REWRITE SCRIPT")
        print("=" * 60)
        print("📋 Bước này cần làm thủ công:")
        print("   1. Mở transcript từ 05_subtitles/translated/")
        print("   2. Dùng prompt từ 02_scripts/prompts/rewrite_prompts.md")
        print("   3. Paste vào ChatGPT/Claude")
        print("   4. Lưu script vào 02_scripts/final/")
        results["rewrite"] = "manual"

    # Step 4: Voice
    if "voice" in steps:
        print("\n" + "=" * 60)
        print("🗣️ STEP 4: VOICE GENERATION")
        print("=" * 60)
        print("⚠️ Cần chỉ định path script đã viết")
        print("   Chạy riêng: python voice/voice.py <script_path>")
        results["voice"] = "manual"

    # Summary
    print("\n" + "=" * 60)
    print("📊 PIPELINE SUMMARY")
    print("=" * 60)
    for step, status in results.items():
        icon = "✅" if status is True else "⚠️"
        print(f"  {icon} {step}: {status}")

    print("\n📋 Các bước tiếp theo (thủ công):")
    print("  5. Edit video trong CapCut/DaVinci")
    print("  6. Tạo thumbnail")
    print("  7. Upload lên YouTube")
    print("  8. Tối ưu SEO")
    print("  9. Theo dõi analytics")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pipeline.py <url>")
        print("  python pipeline.py <url> --steps download,transcribe,voice")
        print("\nSteps available: download, transcribe, rewrite, voice")
        sys.exit(1)

    url = sys.argv[1]
    steps = None

    if "--steps" in sys.argv:
        idx = sys.argv.index("--steps")
        steps = sys.argv[idx + 1].split(",")

    run_pipeline(url, steps)
