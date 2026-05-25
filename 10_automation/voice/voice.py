"""
YouTube China Pipeline - Voice Generator
Tạo voice-over bằng Edge TTS (miễn phí) hoặc ElevenLabs.

Usage:
    python voice.py <script_file> [--engine edge|elevenlabs]
    python voice.py <script_file> --voice "vi-VN-HoaiMyNeural"
    python voice.py --list-voices
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
VOICE_AI_DIR = PROJECT_ROOT / "03_voiceover" / "ai_voice"
SCRIPTS_DIR = PROJECT_ROOT / "02_scripts" / "final"


def list_voices():
    """Liệt kê các voice tiếng Việt có sẵn."""
    print("🎙️ Danh sách voice tiếng Việt (Edge TTS):")
    print("-" * 60)
    try:
        result = subprocess.run(
            ["edge-tts", "--list-voices"],
            capture_output=True, text=True
        )
        for line in result.stdout.split("\n"):
            if "vi-VN" in line or "Vietnamese" in line:
                print(f"  {line.strip()}")
    except FileNotFoundError:
        print("❌ edge-tts chưa được cài đặt!")
        print("   Chạy: pip install edge-tts")


def generate_voice_edge(script_path: str, voice: str = "vi-VN-HoaiMyNeural"):
    """Tạo voice bằng Edge TTS."""
    script = Path(script_path)
    if not script.exists():
        print(f"❌ File không tồn tại: {script_path}")
        return

    VOICE_AI_DIR.mkdir(parents=True, exist_ok=True)

    # Đọc script
    with open(script, "r", encoding="utf-8") as f:
        text = f.read()

    # Xóa markdown formatting
    text = clean_script(text)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = VOICE_AI_DIR / f"{today}_{script.stem}.mp3"

    print(f"🎙️ Generating voice...")
    print(f"📄 Script: {script.name}")
    print(f"🗣️ Voice: {voice}")
    print(f"📁 Output: {output_file}")
    print(f"📝 Text length: {len(text)} chars")
    print("-" * 60)

    cmd = [
        "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", str(output_file),
        "--write-subtitles", str(output_file.with_suffix(".vtt"))
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"\n✅ Voice generated: {output_file}")
            print(f"📄 Subtitles: {output_file.with_suffix('.vtt')}")
        else:
            print(f"\n❌ Voice generation thất bại!")
    except FileNotFoundError:
        print("❌ edge-tts chưa được cài đặt!")
        print("   Chạy: pip install edge-tts")


def clean_script(text: str) -> str:
    """Xóa markdown formatting, giữ lại text thuần."""
    import re
    # Xóa headers markdown
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Xóa bold/italic
    text = re.sub(r'\*+', '', text)
    # Xóa [B-ROLL: ...] markers
    text = re.sub(r'\[B-ROLL:.*?\]', '', text)
    # Xóa dòng trống thừa
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Xóa các chỉ dẫn trong ngoặc vuông
    text = re.sub(r'\[.*?\]', '', text)
    return text.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python voice.py <script_file>")
        print("  python voice.py <script_file> --voice vi-VN-NamMinhNeural")
        print("  python voice.py --list-voices")
        sys.exit(1)

    if sys.argv[1] == "--list-voices":
        list_voices()
        sys.exit(0)

    script_path = sys.argv[1]
    voice = "vi-VN-HoaiMyNeural"
    engine = "edge"

    if "--voice" in sys.argv:
        idx = sys.argv.index("--voice")
        voice = sys.argv[idx + 1]

    if "--engine" in sys.argv:
        idx = sys.argv.index("--engine")
        engine = sys.argv[idx + 1]

    if engine == "edge":
        generate_voice_edge(script_path, voice)
    elif engine == "elevenlabs":
        print("⚠️ ElevenLabs integration: Cấu hình API key trong .env")
        print("   TODO: Implement ElevenLabs API call")
    else:
        print(f"❌ Engine không hỗ trợ: {engine}")
