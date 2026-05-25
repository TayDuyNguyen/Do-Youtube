"""
YouTube China Pipeline - Transcribe & Translate
Tự động transcribe video bằng Whisper và dịch sang tiếng Việt.

Usage:
    python transcribe.py <video_path>
    python transcribe.py <video_path> --translate
    python transcribe.py <video_path> --model medium --language zh
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
SUBTITLE_RAW = PROJECT_ROOT / "05_subtitles" / "raw"
SUBTITLE_TRANSLATED = PROJECT_ROOT / "05_subtitles" / "translated"


def transcribe(video_path: str, model: str = "medium", language: str = "zh"):
    """Transcribe video bằng Whisper."""
    video = Path(video_path)
    if not video.exists():
        print(f"❌ File không tồn tại: {video_path}")
        return None

    SUBTITLE_RAW.mkdir(parents=True, exist_ok=True)

    print(f"🎙️ Transcribing: {video.name}")
    print(f"📊 Model: {model}")
    print(f"🌐 Language: {language}")
    print("-" * 60)

    cmd = [
        "whisper",
        str(video),
        "--model", model,
        "--language", language,
        "--output_dir", str(SUBTITLE_RAW),
        "--output_format", "all",
        "--verbose", "True"
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"\n✅ Transcribe thành công!")
            # Tìm file output
            stem = video.stem
            srt_file = SUBTITLE_RAW / f"{stem}.srt"
            txt_file = SUBTITLE_RAW / f"{stem}.txt"
            if txt_file.exists():
                print(f"📄 Text: {txt_file}")
            if srt_file.exists():
                print(f"📄 SRT: {srt_file}")
            return txt_file if txt_file.exists() else None
        else:
            print(f"\n❌ Transcribe thất bại!")
            return None
    except FileNotFoundError:
        print("❌ Whisper chưa được cài đặt!")
        print("   Chạy: pip install openai-whisper")
        return None


def translate_with_edge(text: str) -> str:
    """Dịch text sử dụng phương pháp đơn giản (placeholder cho API dịch)."""
    # TODO: Integrate DeepL or Google Translate API
    print("⚠️ Auto-translate chưa được cấu hình.")
    print("   Vui lòng dịch thủ công hoặc cấu hình API trong .env")
    print("   Gợi ý: DeepL, Google Translate, hoặc ChatGPT")
    return text


def save_translation(original_path: Path, translated_text: str):
    """Lưu bản dịch."""
    SUBTITLE_TRANSLATED.mkdir(parents=True, exist_ok=True)
    output = SUBTITLE_TRANSLATED / f"{original_path.stem}_vi.txt"
    with open(output, "w", encoding="utf-8") as f:
        f.write(translated_text)
    print(f"📝 Translation saved: {output}")
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python transcribe.py <video_path>")
        print("  python transcribe.py <video_path> --translate")
        print("  python transcribe.py <video_path> --model large --language zh")
        sys.exit(1)

    video_path = sys.argv[1]
    model = "medium"
    language = "zh"
    do_translate = "--translate" in sys.argv

    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        model = sys.argv[idx + 1]

    if "--language" in sys.argv:
        idx = sys.argv.index("--language")
        language = sys.argv[idx + 1]

    txt_file = transcribe(video_path, model, language)

    if do_translate and txt_file and txt_file.exists():
        print(f"\n🌐 Translating...")
        with open(txt_file, "r", encoding="utf-8") as f:
            original_text = f.read()
        translated = translate_with_edge(original_text)
        save_translation(txt_file, translated)
