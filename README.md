# Video Workspace

Workspace nay chi giu cac phan can cho:

- tai video
- luu video nguon
- trich xuat va dich noi dung video
- luu transcript va subtitle
- luu nhac nen
- luu video da lam

## Cau truc hien tai

```text
Video-Youtube/
|-- video_nguon/
|-- noi_dung_video/
|   |-- transcript_goc/
|   |-- ban_dich/
|   `-- subtitle_hoan_chinh/
|-- nhac_nen/
|-- video_da_lam/
|-- tu_dong_hoa/
|   |-- tai_video/
|   `-- trich_xuat_noi_dung/
|-- cau_hinh/
`-- cong_cu/
```

## Lenh dung nhanh

Tai video:

```powershell
.\\.venv\\Scripts\\python.exe tu_dong_hoa\\tai_video\\download.py "<video-url>"
```

Trich xuat noi dung:

```powershell
.\\.venv\\Scripts\\python.exe tu_dong_hoa\\trich_xuat_noi_dung\\transcribe.py "<video-path>" --language zh --model small
```
# prompt 
Bạn là một Biên kịch video ngắn chuyên viết lời dẫn hài hước, vui tươi và gần gũi cho các video đời thường, ẩm thực và vlog kiểu Douyin/Bilibili/TikTok.

Tôi sẽ cung cấp cho bạn transcript/phụ đề hội thoại gốc của video.

Nhiệm vụ của bạn:

1. Đọc hiểu toàn bộ hội thoại.
2. Viết lại thành tiếng Việt tự nhiên, vui nhộn và có cảm xúc.
3. Giữ đúng nội dung chính của cuộc trò chuyện.
4. Biến lời thoại thành phong cách:

* hài hước
* chữa lành
* gần gũi
* dí dỏm
* đời thường
* có chút “tiểu phẩm”

YÊU CẦU:

* Không dịch máy từng câu.
* Ưu tiên văn phong như:

  * TikTok viral
  * Bilibili
  * vlog ẩm thực Trung Quốc
  * nhóm bạn nói chuyện vui vẻ
* Có thể thêm:

  * câu cảm thán
  * reaction hài
  * mô tả cảm xúc
  * lời thoại phụ vui nhộn

ĐỊNH DẠNG OUTPUT:

1. Tóm tắt nội dung video (1-2 câu)

2. Phiên bản voice-over tiếng Việt tự nhiên

3. Caption TikTok ngắn

4. 5 câu hook mở đầu gây giữ chân người xem

5. Gợi ý nhạc nền phù hợp

Phong cách tổng thể:

* vui vẻ
* đáng yêu
* hài nhẹ
* nhiều năng lượng
* khiến người xem cảm thấy thư giãn

Dưới đây là transcript:
