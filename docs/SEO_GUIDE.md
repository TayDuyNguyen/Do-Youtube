# 🔍 Hướng Dẫn SEO YouTube

---

## 1. Tiêu đề (Title)

### Công thức tiêu đề viral

```
[Số] + [Chủ thể] + [Hành động gây sốc] + [Kết quả/Hệ quả]
```

### Ví dụ theo ngách

#### Công nghệ AI
- "AI Trung Quốc vừa làm điều KHÔNG TƯỞNG này..."
- "Tại sao AI TQ khiến cả Mỹ phải sợ?"
- "5 AI tools TQ MIỄN PHÍ đánh bại ChatGPT"

#### Factory/Machine
- "Xem cách TQ sản xuất 1 triệu sản phẩm MỖI NGÀY"
- "Nhà máy TQ tự động 100% — không cần con người"

#### Xe điện
- "Xe điện TQ giá 100 triệu đánh bại Tesla?"
- "BYD vừa tung xe mới khiến thế giới CHOÁNG"

### Quy tắc
- Dưới 60 ký tự (không bị cắt)
- Có keyword chính ở đầu
- Dùng CAPS cho 1-2 từ nhấn mạnh
- Gợi tò mò nhưng không clickbait quá

---

## 2. Mô tả (Description)

### Template

```
[Hook 1-2 câu] 

Trong video này, [tóm tắt nội dung 2-3 câu].

📌 Nội dung chính:
00:00 - Intro
01:30 - [Phần 1]
04:00 - [Phần 2]
07:00 - [Phần 3]
09:30 - Kết luận

🔗 Link hữu ích:
- [Link 1]
- [Link 2]

📱 Follow:
- Facebook: [link]
- TikTok: [link]

#keyword1 #keyword2 #keyword3

© Disclaimer: [Nếu cần]
```

### Quy tắc
- Tối thiểu 200 từ
- 3-5 hashtag cuối description
- Timestamps (YouTube yêu thích)
- Keyword chính xuất hiện 2-3 lần tự nhiên

---

## 3. Tags

### Chiến lược tags
1. **Tag chính** (1-2): Keyword chính, broad
2. **Tag phụ** (5-8): Keyword liên quan, cụ thể hơn
3. **Tag dài** (5-8): Long-tail keyword
4. **Tag brand** (2-3): Tên kênh, tên series

### Ví dụ cho video "AI Trung Quốc"
```
AI Trung Quốc, trí tuệ nhân tạo, công nghệ Trung Quốc,
AI TQ vs ChatGPT, deepseek, AI tools miễn phí,
trung quốc phát triển AI, so sánh AI, công nghệ mới 2026,
review AI, AI hay nhất 2026, tên_kênh, AI series
```

---

## 4. Thumbnail SEO

### Checklist
- [ ] Text rõ ràng khi nhỏ (mobile)
- [ ] Tối đa 5-6 từ
- [ ] Font to, bold, có outline
- [ ] Màu tương phản (vàng/trắng trên nền tối)
- [ ] Có mặt người + biểu cảm (nếu phù hợp)
- [ ] Hình ảnh chính rõ ràng
- [ ] Kích thước: 1280x720

### Màu hiệu quả
| Nền      | Chữ     | Hiệu quả |
|----------|---------|-----------|
| Đen/tối  | Vàng    | ⭐⭐⭐⭐⭐  |
| Đỏ       | Trắng   | ⭐⭐⭐⭐   |
| Xanh đậm | Trắng  | ⭐⭐⭐⭐   |
| Gradient  | Trắng  | ⭐⭐⭐⭐   |

---

## 5. Keyword Research

### Công cụ free
- YouTube Search Suggest (gõ keyword → xem gợi ý)
- Google Trends (https://trends.google.com)
- VidIQ (extension Chrome - bản free)
- TubeBuddy (extension Chrome - bản free)

### Quy trình
1. Brainstorm 10-20 keyword
2. Check search volume trên VidIQ
3. Check competition
4. Chọn keyword có: volume trung bình + competition thấp
5. Lưu vào `09_data/keyword_research/`

### Format file keyword
```csv
keyword,search_volume,competition,score,notes
"AI Trung Quốc",12000,medium,85,trending up
"robot TQ",8000,low,92,good opportunity
```

---

## 6. Tối ưu Retention

### Cấu trúc giữ người xem
```
0:00-0:05  → HOOK mạnh (preview kết quả)
0:05-0:30  → Setup/Context
0:30-3:00  → Nội dung 1 (peak interest)
3:00-3:05  → Mini hook ("Nhưng đó chưa phải tất cả...")
3:05-6:00  → Nội dung 2
6:00-6:05  → Transition hook
6:05-8:00  → Nội dung 3 + Kết luận
8:00-8:30  → CTA
```

### Mẹo giữ retention
- Pattern interrupt mỗi 30-60 giây
- Zoom in/out tại điểm nhấn
- Sound effect tại transition
- Text overlay cho key points
- Đặt câu hỏi cho người xem
- Preview nội dung phía sau

---

## 7. Tracking & Analytics

Lưu vào `09_data/performance_logs/monthly_YYYY_MM.csv`:

```csv
date,title,type,views_24h,views_7d,ctr,avg_retention,subs_gained,revenue,notes
2026-05-21,Robot TQ,long,1500,8000,6.2%,45%,120,$12.50,good hook
2026-05-21,AI demo,short,5000,25000,8.1%,72%,80,$3.20,viral potential
```
