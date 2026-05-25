# 📋 SOP: Quy Trình Sản Xuất Video YouTube

> Quy trình chuẩn từ A-Z để sản xuất 1 video YouTube từ nguồn Trung Quốc

---

## Tổng quan Workflow

```
┌─────────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────────┐
│ 1. Tìm nguồn│───→│2. Download│───→│3. Phân tích  │───→│4. Viết script│
│    video     │    │   video   │    │   nội dung   │    │   mới        │
└─────────────┘    └──────────┘    └──────────────┘    └──────────────┘
                                                              │
┌─────────────┐    ┌──────────┐    ┌──────────────┐          │
│ 8. Upload   │←───│7. Render │←───│6. Edit video │←─────────┘
│   YouTube   │    │  & Check │    │   + Subtitle │    ┌──────────────┐
└─────────────┘    └──────────┘    └──────────────┘←───│5. Voice Over │
       │                                                └──────────────┘
       ↓
┌─────────────┐
│ 9. SEO &    │
│   Analytics │
└─────────────┘
```

---

## Bước 1: Tìm nguồn video (15-30 phút)

### Nơi tìm
| Platform      | URL                          | Ưu điểm              |
|---------------|------------------------------|-----------------------|
| Bilibili      | https://bilibili.com         | Video dài, chất lượng |
| Douyin        | https://douyin.com           | Trending, ngắn        |
| Xiaohongshu   | https://xiaohongshu.com      | Lifestyle, review     |
| Weibo         | https://weibo.com            | News, viral           |

### Checklist chọn video
- [ ] Video không có logo đài truyền hình lớn
- [ ] Không có nhạc bản quyền rõ ràng
- [ ] Nội dung có thể voice-over lại
- [ ] Dễ cắt ngắn và ghép lại
- [ ] Có thông tin thú vị, gây tò mò
- [ ] Phù hợp với ngách đã chọn
- [ ] Video có chất lượng tốt (tối thiểu 720p)

### Lưu thông tin
Tạo file trong `01_sources/[platform]/` với format:
```
[NGÀY]_[TÊN_VIDEO].txt
```

Nội dung file:
```
URL: [link gốc]
Tiêu đề gốc: [tiêu đề tiếng Trung]
Nội dung tóm tắt: [mô tả ngắn]
Lý do chọn: [tại sao video này hay]
Ngách: [tech/food/factory/...]
Ngày tìm: [YYYY-MM-DD]
Trạng thái: [tìm thấy/đã download/đã dùng]
```

---

## Bước 2: Download video (5 phút)

### Công cụ chính: yt-dlp

```bash
# Cài đặt
pip install yt-dlp

# Download cơ bản
yt-dlp -o "01_sources/bilibili/%(title)s.%(ext)s" [URL]

# Download chất lượng cao nhất
yt-dlp -f "bestvideo+bestaudio" -o "01_sources/bilibili/%(title)s.%(ext)s" [URL]

# Download với subtitle
yt-dlp --write-subs --sub-langs all -o "01_sources/bilibili/%(title)s.%(ext)s" [URL]
```

### Công cụ backup
- SnapAny: https://snapany.com
- Cobalt: https://cobalt.tools

### Tổ chức file
```
01_sources/
├── bilibili/
│   ├── 2026-05-21_robot_giao_hang.mp4
│   ├── 2026-05-21_robot_giao_hang.txt  (metadata)
│   └── ...
```

---

## Bước 3: Phân tích & trích xuất nội dung (15-20 phút)

### 3a. Tạo transcript bằng Whisper

```bash
# Cài đặt
pip install openai-whisper

# Transcribe tiếng Trung
whisper "01_sources/bilibili/video.mp4" --language zh --output_dir "05_subtitles/raw/"

# Hoặc dùng faster-whisper cho tốc độ nhanh hơn
pip install faster-whisper
```

Output lưu vào: `05_subtitles/raw/`

### 3b. Dịch transcript

```bash
# Dùng API hoặc công cụ dịch
# Output lưu vào: 05_subtitles/translated/
```

Hoặc dùng:
- DeepL Translate (chính xác nhất)
- Google Translate
- ChatGPT (có context tốt hơn)

### 3c. Phân tích nội dung
Trả lời các câu hỏi:
1. **Ý chính là gì?**
2. **Góc nhìn nào mới lạ?**
3. **Đối tượng xem là ai?**
4. **Tiêu đề hấp dẫn nào có thể đặt?**
5. **Video này thuộc dạng nào?** (giải thích/review/reaction/documentary)

---

## Bước 4: Viết script mới (30-45 phút)

### ⚠️ ĐÂY LÀ BƯỚC QUAN TRỌNG NHẤT

### Nguyên tắc vàng
1. **KHÔNG dịch nguyên xi** - Viết lại hoàn toàn
2. **Thêm góc nhìn cá nhân** - Commentary, phân tích
3. **Thay đổi cấu trúc** - Không giữ flow gốc
4. **Thêm thông tin bổ sung** - Research thêm

### Cấu trúc script chuẩn

```markdown
## HOOK (0:00 - 0:05) — 5 giây đầu
[Câu mở gây sốc/tò mò]
Ví dụ: "Bạn sẽ không tin Trung Quốc vừa làm được điều này…"

## CONTEXT (0:05 - 0:30)
[Đặt vấn đề, bối cảnh]

## NỘI DUNG CHÍNH (0:30 - 7:00)
### Điểm 1: [...]
### Điểm 2: [...]
### Điểm 3: [...]
[Commentary cá nhân xen kẽ]

## KẾT LUẬN (7:00 - 7:30)
[Tóm tắt, góc nhìn tổng quan]

## CTA (7:30 - 8:00)
"Nếu bạn thấy video này hay, hãy like và subscribe..."
```

### Prompt AI để viết lại script

Lưu prompt vào `02_scripts/prompts/`:

```
Bạn là một scriptwriter YouTube chuyên nghiệp.
Dựa trên thông tin sau đây từ một video Trung Quốc,
hãy viết lại thành một script YouTube hoàn toàn mới bằng tiếng Việt.

YÊU CẦU:
- KHÔNG dịch nguyên xi, viết lại hoàn toàn
- Thêm commentary và góc nhìn cá nhân
- Dùng ngôn ngữ YouTube cuốn hút
- Cấu trúc: Hook → Context → Nội dung → Kết luận → CTA
- Tone: [vui vẻ / nghiêm túc / tò mò / giải thích]
- Độ dài: [X] phút đọc

THÔNG TIN GỐC:
[Paste transcript đã dịch]

CHỦ ĐỀ:
[Chủ đề video]

NGÁCH:
[Ngách kênh]
```

### Lưu file
```
02_scripts/
├── drafts/
│   └── 2026-05-21_robot_giao_hang_v1.md
├── final/
│   └── 2026-05-21_robot_giao_hang_final.md
```

---

## Bước 5: Tạo Voice Over (10-15 phút)

### Option A: Voice AI (nhanh, dễ scale)

| Tool          | Giá           | Chất lượng | Link                    |
|---------------|---------------|------------|-------------------------|
| ElevenLabs    | Freemium      | ⭐⭐⭐⭐⭐  | https://elevenlabs.io   |
| Fish Audio    | Free          | ⭐⭐⭐⭐    | https://fish.audio      |
| Edge TTS      | Free          | ⭐⭐⭐      | CLI tool                |

```bash
# Edge TTS (miễn phí)
pip install edge-tts
edge-tts --voice "vi-VN-HoaiMyNeural" --text "Script của bạn" --write-media "03_voiceover/ai_voice/output.mp3"
```

### Option B: Voice thật (dễ bật monetization hơn)
- Micro USB tốt: ~500k-1tr VNĐ
- Phần mềm: Audacity (free)
- Phòng yên tĩnh

### Lưu file
```
03_voiceover/
├── ai_voice/
│   └── 2026-05-21_robot_giao_hang.mp3
├── real_voice/
│   └── 2026-05-21_robot_giao_hang.wav
```

---

## Bước 6: Edit Video (30-60 phút)

### Tool chính
| Tool            | Ưu điểm              | Cho ai           |
|-----------------|----------------------|-------------------|
| CapCut Desktop  | Nhanh, dễ, template  | Beginner          |
| DaVinci Resolve | Pro, free, mạnh      | Intermediate+     |

### Checklist edit bắt buộc
- [ ] Zoom in/out các đoạn quan trọng
- [ ] Crop bỏ watermark/logo gốc
- [ ] Thêm subtitle tiếng Việt
- [ ] Thêm B-roll (footage phụ)
- [ ] Thêm transition giữa các đoạn
- [ ] Thêm sound effects tại điểm nhấn
- [ ] Thêm background music (không bản quyền)
- [ ] Overlay text cho các điểm chính
- [ ] Intro/Outro kênh
- [ ] Color grading khác video gốc

### Nguồn nhạc không bản quyền
- YouTube Audio Library (free)
- Pixabay Music (free)
- Epidemic Sound (paid, tốt nhất)
- Artlist (paid)

### Lưu project
```
04_editing/
├── capcut/
│   └── 2026-05-21_robot_giao_hang/
├── assets/
│   ├── music/
│   ├── sfx/
│   └── ...
```

---

## Bước 7: Tạo Thumbnail (10-15 phút)

### Nguyên tắc thumbnail viral
1. **Chữ to, ít chữ** (tối đa 5-6 từ)
2. **Màu tương phản cao** (vàng/đỏ trên nền tối)
3. **Mặt người + biểu cảm** (nếu có)
4. **Hình ảnh rõ ràng** ở kích thước nhỏ
5. **Kích thước**: 1280x720 px

### Tool
- Canva (free, dễ dùng)
- Photoshop
- Figma

### Lưu file
```
06_thumbnails/
├── templates/
│   └── tech_template.psd
├── exported/
│   └── 2026-05-21_robot_giao_hang.png
├── ab_test/
│   ├── 2026-05-21_robot_giao_hang_A.png
│   └── 2026-05-21_robot_giao_hang_B.png
```

---

## Bước 8: Upload YouTube (10 phút)

### Checklist upload
- [ ] Title hấp dẫn, có keyword
- [ ] Description chi tiết (tối thiểu 200 từ)
- [ ] Tags phù hợp (15-20 tags)
- [ ] Thumbnail custom
- [ ] End screen
- [ ] Cards
- [ ] Playlist phù hợp
- [ ] Subtitle file (nếu có)
- [ ] Scheduled time (giờ vàng)

### Giờ upload tốt nhất (Việt Nam)
- **Shorts**: 7h-9h sáng, 12h-13h, 19h-21h
- **Long-form**: 17h-19h (trước giờ prime time)

### Auto upload (CLI)
```bash
# Dùng youtube-upload hoặc API
# Script trong: 10_automation/upload/
```

---

## Bước 9: SEO & Analytics (liên tục)

### Sau khi upload
- [ ] Check 48h đầu: CTR, retention
- [ ] A/B test thumbnail nếu CTR < 5%
- [ ] Đổi title nếu views thấp
- [ ] Reply comment trong 1h đầu
- [ ] Share lên social media

### Tracking
Ghi lại vào `09_data/performance_logs/`:
```
Ngày: 2026-05-21
Video: Robot giao hàng TQ
Views 24h: XXX
CTR: X.X%
Avg Retention: X:XX
Subscribers gained: XX
Revenue: $X.XX
Ghi chú: [...]
```

---

## ⏱️ Tổng thời gian ước tính

| Bước               | Thời gian   |
|---------------------|-------------|
| Tìm nguồn          | 15-30 phút  |
| Download            | 5 phút      |
| Phân tích           | 15-20 phút  |
| Viết script         | 30-45 phút  |
| Voice over          | 10-15 phút  |
| Edit video          | 30-60 phút  |
| Thumbnail           | 10-15 phút  |
| Upload + SEO        | 10 phút     |
| **TỔNG**            | **~2-3 giờ** |

> Với automation, có thể giảm xuống **~1-1.5 giờ/video**

---

## 📌 Naming Convention

Tất cả file trong project nên theo format:
```
[YYYY-MM-DD]_[tên_ngắn_gọn]_[version].[ext]
```

Ví dụ:
```
2026-05-21_robot_giao_hang_v1.md
2026-05-21_robot_giao_hang_final.mp4
2026-05-21_robot_giao_hang_thumb.png
```
