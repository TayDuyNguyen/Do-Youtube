# 🔧 Hướng Dẫn Cài Đặt Tools

---

## 1. Tools bắt buộc

### yt-dlp — Download video

```bash
# Cài đặt
pip install yt-dlp

# Hoặc dùng binary
# Download từ: https://github.com/yt-dlp/yt-dlp/releases

# Test
yt-dlp --version
```

**Cấu hình mặc định** - Tạo file `config/yt-dlp.conf`:
```
-o "01_sources/%(extractor)s/%(upload_date)s_%(title)s.%(ext)s"
-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
--write-subs
--sub-langs all
--embed-metadata
--no-overwrites
```

---

### Whisper — Transcribe audio

```bash
# OpenAI Whisper
pip install openai-whisper

# Hoặc faster-whisper (nhanh hơn 4x)
pip install faster-whisper

# Test
whisper --help
```

**Yêu cầu**: NVIDIA GPU khuyến nghị (CUDA)

---

### Edge TTS — Voice AI miễn phí

```bash
pip install edge-tts

# Xem danh sách voice tiếng Việt
edge-tts --list-voices | findstr "vi-VN"

# Voice hay nhất:
# vi-VN-HoaiMyNeural (nữ)
# vi-VN-NamMinhNeural (nam)

# Test
edge-tts --voice "vi-VN-HoaiMyNeural" --text "Xin chào" --write-media test.mp3
```

---

### FFmpeg — Xử lý video/audio

```bash
# Download từ: https://ffmpeg.org/download.html
# Hoặc dùng winget:
winget install FFmpeg

# Test
ffmpeg -version
```

---

## 2. Tools khuyến nghị

### ElevenLabs — Voice AI chất lượng cao
- Website: https://elevenlabs.io
- Free tier: 10,000 ký tự/tháng
- API key lưu trong `.env`

### Fish Audio — Voice AI alternative
- Website: https://fish.audio
- Free, chất lượng tốt

### CapCut Desktop — Edit video
- Download: https://www.capcut.com/
- Free, nhiều template
- Hỗ trợ auto-caption

### DaVinci Resolve — Edit video pro
- Download: https://www.blackmagicdesign.com/products/davinciresolve
- Free (bản đầy đủ)
- Color grading mạnh

### Canva — Thiết kế thumbnail
- Website: https://canva.com
- Free tier đủ dùng

---

## 3. Tools automation (cho developer)

### Python packages

```bash
pip install yt-dlp openai-whisper edge-tts requests python-dotenv
```

### Node.js packages (nếu dùng)

```bash
npm install googleapis dotenv axios
```

### VS Code Extensions khuyến nghị
- Python
- Markdown Preview Enhanced
- CSV to Table

---

## 4. API Keys cần thiết

Tạo file `config/.env` từ template:

```bash
cp config/.env.example config/.env
```

Điền các API key:

```env
# OpenAI (cho ChatGPT rewrite)
OPENAI_API_KEY=sk-...

# ElevenLabs (cho voice AI)
ELEVENLABS_API_KEY=...

# YouTube Data API (cho upload & analytics)
YOUTUBE_API_KEY=...
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...

# DeepL (cho dịch thuật)
DEEPL_API_KEY=...

# Google Cloud (cho Speech-to-Text backup)
GOOGLE_CLOUD_KEY=...
```

---

## 5. Kiểm tra cài đặt

Chạy checklist sau để verify:

```bash
# 1. yt-dlp
yt-dlp --version

# 2. Whisper
whisper --help

# 3. Edge TTS
edge-tts --list-voices | head -5

# 4. FFmpeg
ffmpeg -version

# 5. Python
python --version

# 6. pip packages
pip list | findstr "yt-dlp whisper edge-tts"
```

Nếu tất cả OK → sẵn sàng sản xuất! 🚀

---

## 6. Cấu trúc file cấu hình

```
config/
├── .env.example      # Template API keys
├── .env              # API keys thật (KHÔNG commit git)
├── settings.json     # Cài đặt pipeline
└── yt-dlp.conf       # Cài đặt yt-dlp
```
