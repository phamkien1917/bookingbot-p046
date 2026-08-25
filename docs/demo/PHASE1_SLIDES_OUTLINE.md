# Dàn ý Slides — Nera (Demo Day Phase 1)

Ngắn gọn, đủ dùng để dựng nhanh trong Google Slides/Canva. Mỗi mục dưới đây là 1 slide.

## 1. Trang bìa
- Tên: **Nera**
- Dòng phụ: Trợ lý AI tìm và đặt lịch xem nhà qua hội thoại tự nhiên
- Team: 046 LTD — Lê Tiến Đạt, Vũ Thế Lực, Phạm Trung Kiên, Nguyễn Thế Anh

## 2. Vấn đề
- Người tìm nhà phải tự lọc qua hàng loạt tin đăng rời rạc.
- Mỗi lần tìm lại phải nhập lại tiêu chí từ đầu.
- Đặt lịch xem nhà không có kênh nhanh gọn, phải liên hệ thủ công.

## 3. Giải pháp
- Một trợ lý AI duy nhất: nói chuyện tự nhiên để tìm nhà, không cần điền form.
- Nhớ ngữ cảnh trong suốt cuộc trò chuyện — không phải lặp lại tiêu chí.
- Đặt lịch xem nhà ngay trong hội thoại, nối thẳng vào lịch làm việc thật của sale.

## 4. Demo — ảnh chụp màn hình thật (không dàn dựng)
- Ảnh 1: tìm nhà bằng câu tự nhiên, ra đúng kết quả thật từ DB.
- Ảnh 2: hỏi tiếp không nhắc lại tiêu chí cũ, vẫn giữ đúng ngữ cảnh.
- Ảnh 3: đặt lịch, ra khung giờ trống thật kèm tên nhân viên sale thật.

## 5. Kiến trúc kỹ thuật (ngắn gọn)
- Next.js (frontend) → FastAPI (backend) → LangGraph multi-agent (điều phối hội thoại) → LLM thật (gpt-4o-mini).
- Dữ liệu bất động sản: crawl thật từ batdongsan.com.vn, chotot.com — lưu PostgreSQL.
- Đặt lịch: đọc/ghi trực tiếp lịch làm việc thật của nhân viên sale trong hệ thống.

## 6. Đã kiểm chứng, không chỉ là mockup
- Toàn bộ luồng trên đã test trực tiếp trên bản deploy thật (nerahome.space), có log xác nhận gọi LLM thật.
- Không bịa dữ liệu: khi thiếu thông tin hoặc hỏi ngoài phạm vi, agent từ chối thay vì đoán bừa.

## 7. Hướng phát triển tiếp theo
- Định vị tiện ích xung quanh nhà (khoảng cách thật tới trường học, bệnh viện).
- Cố vấn tài chính: tính khoản vay, trả góp dựa trên thu nhập thực tế của khách.

## 8. Cảm ơn / Link
- MVP: nerahome.space
- Repo: github.com/AI20K-Build-Phase-Cohort-3/P-046

---

**Ghi chú khi làm slide:** ưu tiên chụp ảnh thật từ đúng 4 câu trong kịch bản demo (`PROD_DEMO_SCRIPT_2026-08-22.md`) cho slide 4, đừng vẽ mockup giả — giám khảo có thể vào thẳng link MVP để đối chiếu.
