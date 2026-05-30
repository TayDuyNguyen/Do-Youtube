"""
YouTube China Pipeline - Transcribe & Translate
Tự động transcribe video bằng Whisper và dịch sang tiếng Việt.

Usage:
    python transcribe.py <video_path>
    python transcribe.py <video_path> --translate
    python transcribe.py <video_path> --model small --language zh
    python transcribe.py <video_path> --backend openai --model medium --language zh
"""

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).parent.parent.parent
SUBTITLE_RAW = PROJECT_ROOT / "noi_dung_video" / "transcript_goc"
SUBTITLE_TRANSLATED = PROJECT_ROOT / "noi_dung_video" / "ban_dich"
WHISPER_CPP_DIR = PROJECT_ROOT / "cong_cu" / "whisper.cpp"
WHISPER_CPP_BIN = WHISPER_CPP_DIR / "Release" / "whisper-cli.exe"
WHISPER_CPP_MODELS = WHISPER_CPP_DIR / "models"
WHISPER_CPP_TEMP = Path("C:/tmp/whispercpp")


def resolve_whisper_cpp_model(model: str) -> Path:
    """Resolve a whisper.cpp model name or path to a local ggml model file."""
    model_path = Path(model)
    if model_path.exists():
        return model_path

    filename = model if model.startswith("ggml-") else f"ggml-{model}"
    if not filename.endswith(".bin"):
        filename = f"{filename}.bin"

    resolved = WHISPER_CPP_MODELS / filename
    if not resolved.exists():
        available = ", ".join(sorted(p.name for p in WHISPER_CPP_MODELS.glob("*.bin"))) or "none"
        raise FileNotFoundError(
            f"Không tìm thấy model whisper.cpp: {resolved}\n"
            f"Model hiện có: {available}\n"
            "Tải thêm model từ https://huggingface.co/ggerganov/whisper.cpp/tree/main"
        )
    return resolved


def safe_temp_prefix(video: Path) -> str:
    """Create a stable ASCII-safe prefix for whisper.cpp temp files on Windows."""
    digest = hashlib.sha1(str(video).encode("utf-8")).hexdigest()[:12]
    return f"whisper_{digest}"


def extract_audio(video: Path, keep_wav: bool = False) -> tuple[Path, bool]:
    """Convert video/audio input to the 16 kHz mono WAV format whisper.cpp expects."""
    SUBTITLE_RAW.mkdir(parents=True, exist_ok=True)
    WHISPER_CPP_TEMP.mkdir(parents=True, exist_ok=True)
    if video.suffix.lower() == ".wav":
        return video, False

    wav_path = WHISPER_CPP_TEMP / f"{safe_temp_prefix(video)}.wav"
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(wav_path),
    ]
    print("🎧 Extracting audio with FFmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg thất bại:\n{result.stderr}")

    return wav_path, not keep_wav


def move_whisper_output(temp_prefix: Path, final_prefix: Path, suffix: str) -> Path | None:
    """Move whisper.cpp output from the ASCII temp location back to the project tree."""
    temp_file = temp_prefix.with_suffix(suffix)
    if not temp_file.exists():
        return None
    final_file = final_prefix.with_suffix(suffix)
    final_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(temp_file), str(final_file))
    return final_file


def transcribe_with_whisper_cpp(
    video: Path,
    model: str = "small",
    language: str = "zh",
    threads: int | None = None,
    keep_wav: bool = False,
):
    """Transcribe video bằng whisper.cpp."""
    if not WHISPER_CPP_BIN.exists():
        print("❌ Chưa thấy whisper.cpp binary.")
        print(f"   Cần file: {WHISPER_CPP_BIN}")
        return None

    try:
        model_path = resolve_whisper_cpp_model(model)
        wav_path, delete_wav = extract_audio(video, keep_wav=keep_wav)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"❌ {exc}")
        return None

    output_prefix = SUBTITLE_RAW / video.stem
    temp_output_prefix = WHISPER_CPP_TEMP / safe_temp_prefix(video)
    cmd = [
        str(WHISPER_CPP_BIN),
        "-m", str(model_path),
        "-f", str(wav_path),
        "-l", language,
        "-otxt",
        "-osrt",
        "-of", str(temp_output_prefix),
    ]
    if threads:
        cmd.extend(["-t", str(threads)])

    print(f"🎙️ Transcribing with whisper.cpp: {video.name}")
    print(f"📊 Model: {model_path.name}")
    print(f"🌐 Language: {language}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
    finally:
        if delete_wav and wav_path.exists():
            wav_path.unlink()

    if result.returncode != 0:
        print("\n❌ Transcribe thất bại!")
        return None

    txt_file = move_whisper_output(temp_output_prefix, output_prefix, ".txt")
    srt_file = move_whisper_output(temp_output_prefix, output_prefix, ".srt")
    print("\n✅ Transcribe thành công!")
    if txt_file.exists():
        print(f"📄 Text: {txt_file}")
    if srt_file.exists():
        print(f"📄 SRT: {srt_file}")
    return txt_file if txt_file.exists() else None


def transcribe_with_openai_whisper(video: Path, model: str = "medium", language: str = "zh"):
    """Transcribe video bằng Python openai-whisper CLI."""
    SUBTITLE_RAW.mkdir(parents=True, exist_ok=True)

    print(f"🎙️ Transcribing with openai-whisper: {video.name}")
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
        "--verbose", "True",
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
    except FileNotFoundError:
        print("❌ Whisper chưa được cài đặt!")
        print("   Chạy: pip install openai-whisper")
        return None

    if result.returncode != 0:
        print("\n❌ Transcribe thất bại!")
        return None

    stem = video.stem
    txt_file = SUBTITLE_RAW / f"{stem}.txt"
    srt_file = SUBTITLE_RAW / f"{stem}.srt"
    print("\n✅ Transcribe thành công!")
    if txt_file.exists():
        print(f"📄 Text: {txt_file}")
    if srt_file.exists():
        print(f"📄 SRT: {srt_file}")
    return txt_file if txt_file.exists() else None


def transcribe(
    video_path: str,
    model: str = "small",
    language: str = "zh",
    backend: str = "whispercpp",
    threads: int | None = None,
    keep_wav: bool = False,
):
    """Transcribe video bằng whisper.cpp hoặc openai-whisper."""
    video = Path(video_path)
    if not video.exists():
        print(f"❌ File không tồn tại: {video_path}")
        return None

    if backend == "openai":
        return transcribe_with_openai_whisper(video, model=model, language=language)
    return transcribe_with_whisper_cpp(
        video,
        model=model,
        language=language,
        threads=threads,
        keep_wav=keep_wav,
    )


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
    parser = argparse.ArgumentParser(description="Transcribe video/audio to TXT and SRT.")
    parser.add_argument("video_path", help="Path to video/audio file")
    parser.add_argument("--translate", action="store_true", help="Save a Vietnamese translation placeholder")
    parser.add_argument("--model", default="small", help="whisper.cpp model name/path, e.g. small, medium, large-v3-turbo")
    parser.add_argument("--language", default="zh", help="Spoken language code, or auto")
    parser.add_argument("--backend", choices=["whispercpp", "openai"], default="whispercpp")
    parser.add_argument("--threads", type=int, default=None, help="CPU threads for whisper.cpp")
    parser.add_argument("--keep-wav", action="store_true", help="Keep extracted 16 kHz WAV file")
    args = parser.parse_args()

    txt_file = transcribe(
        args.video_path,
        model=args.model,
        language=args.language,
        backend=args.backend,
        threads=args.threads,
        keep_wav=args.keep_wav,
    )

    if args.translate and txt_file and txt_file.exists():
        print(f"\n🌐 Translating...")
        with open(txt_file, "r", encoding="utf-8") as f:
            original_text = f.read()
        translated = translate_with_edge(original_text)
        save_translation(txt_file, translated)
