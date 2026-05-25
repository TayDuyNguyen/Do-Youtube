# 🎬 YouTube China Content Pipeline

> Quy trình bán tự động sản xuất nội dung YouTube từ nguồn video Trung Quốc

## 📁 Cấu trúc dự án

```
youtube-china-pipeline/
│
├── 01_sources/              # Nguồn video gốc từ Trung Quốc
│   ├── bilibili/            # Video từ Bilibili
│   ├── douyin/              # Video từ Douyin/TikTok TQ
│   ├── xiaohongshu/         # Video từ Xiaohongshu
│   ├── weibo/               # Video từ Weibo
│   └── other/               # Nguồn khác
│
├── 02_scripts/              # Kịch bản viết lại
│   ├── drafts/              # Bản nháp script
│   ├── final/               # Bản script hoàn chỉnh
│   └── prompts/             # Prompt templates cho AI rewrite
│
├── 03_voiceover/            # File voice AI hoặc voice thật
│   ├── ai_voice/            # Voice từ ElevenLabs/Fish Audio
│   └── real_voice/          # Voice tự đọc
│
├── 04_editing/              # Project edit video
│   ├── capcut/              # Project CapCut
│   ├── davinci/             # Project DaVinci Resolve
│   ├── assets/              # Assets dùng chung
│   │   ├── music/           # Nhạc nền không bản quyền
│   │   ├── sfx/             # Sound effects
│   │   ├── overlays/        # Overlay text/graphics
│   │   ├── transitions/     # Transition presets
│   │   └── fonts/           # Font chữ
│   └── templates/           # Template edit tái sử dụng
│
├── 05_subtitles/            # Phụ đề
│   ├── raw/                 # Subtitle gốc (Whisper output)
│   ├── translated/          # Subtitle đã dịch
│   └── final/               # Subtitle đã chỉnh sửa
│
├── 06_thumbnails/           # Thumbnail
│   ├── templates/           # Template thumbnail (PSD/Figma)
│   ├── exported/            # Thumbnail đã export
│   └── ab_test/             # Các phiên bản A/B test
│
├── 07_output/               # Video hoàn chỉnh sẵn upload
│   ├── shorts/              # YouTube Shorts
│   └── longform/            # Video dài
│
├── 08_published/            # Video đã upload
│   ├── analytics/           # Dữ liệu phân tích
│   └── archive/             # Lưu trữ video cũ
│
├── 09_data/                 # Dữ liệu thu thập & tracking
│   ├── niche_research/      # Nghiên cứu ngách
│   ├── keyword_research/    # Nghiên cứu keyword SEO
│   ├── competitor_analysis/ # Phân tích đối thủ
│   ├── performance_logs/    # Log hiệu suất kênh
│   └── content_calendar/    # Lịch đăng nội dung
│
├── 10_automation/           # Scripts tự động hóa
│   ├── download/            # Script download video
│   ├── transcribe/          # Script Whisper
│   ├── rewrite/             # Script AI rewrite
│   ├── voice/               # Script tạo voice
│   ├── upload/              # Script auto upload
│   └── utils/               # Tiện ích chung
│
├── docs/                    # Tài liệu & SOP
│   ├── SOP_WORKFLOW.md      # Quy trình làm việc chi tiết
│   ├── NICHE_GUIDE.md       # Hướng dẫn chọn ngách
│   ├── COPYRIGHT_GUIDE.md   # Hướng dẫn tránh bản quyền
│   ├── SEO_GUIDE.md         # Hướng dẫn SEO YouTube
│   ├── TOOLS_SETUP.md       # Hướng dẫn cài đặt tools
│   └── TEAM_SOP.md          # SOP cho team/studio
│
└── config/                  # Cấu hình
    ├── .env.example          # Template biến môi trường
    └── settings.json         # Cài đặt pipeline
```

## 🚀 Bắt đầu nhanh

1. Đọc [SOP Workflow](docs/SOP_WORKFLOW.md)
2. Cài đặt tools theo [Tools Setup](docs/TOOLS_SETUP.md)
3. Chọn ngách theo [Niche Guide](docs/NICHE_GUIDE.md)
4. Bắt đầu sản xuất!

## 📊 Workflow tổng quan

```
Bilibili/Douyin → Download → Extract idea → Rewrite script
    → Voice AI → CapCut edit → Subtitle → Thumbnail → Upload → Analyze
```

## 🎯 Mục tiêu

- **Shorts**: 2-5 video/ngày
- **Long-form**: 2-3 video/tuần
- **Thời gian mỗi video**: ~30-60 phút (với automation)

## ⚠️ Lưu ý quan trọng

- **KHÔNG reup nguyên video** - luôn transform nội dung
- **KHÔNG dùng audio gốc** - thay bằng voice AI hoặc voice thật
- **KHÔNG dịch nguyên xi** - viết lại theo style riêng
- Đọc kỹ [Copyright Guide](docs/COPYRIGHT_GUIDE.md) trước khi bắt đầu
