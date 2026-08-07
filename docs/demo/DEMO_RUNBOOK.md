# Demo Runbook

## Trạng thái

- Trạng thái: Bản nháp vận hành demo
- Demo kỹ thuật: Chưa được repository xác nhận chạy end-to-end
- Deadline và người phụ trách: TBD

## Vai trò

| Vai trò | Trách nhiệm | Người phụ trách |
|---|---|---|
| Demo Lead | Quyết định go/no-go, giữ thời lượng | TBD |
| Presenter | Kể narrative và xử lý Q&A | TBD |
| Demo Operator | Thực hiện click/input đúng kịch bản | TBD |
| Product/PM | Kiểm tra claim, scope và outcome | TBD |
| UI/UX | Kiểm tra màn hình và trạng thái hiển thị | TBD |
| Technical Support | Xác nhận môi trường và xử lý lỗi kỹ thuật | TBD |
| Timekeeper/Note taker | Theo dõi thời gian và ghi câu hỏi | TBD |

Một người có thể giữ nhiều vai trò sau khi team xác nhận.

## Tài sản cần có

| Tài sản | Trạng thái hiện tại |
|---|---|
| Storyboard hai phiên | Bản nháp: `docs/demo/DEMO_STORYBOARD.md` |
| Presenter script | Bản nháp: `docs/demo/DEMO_SCRIPT.md` |
| Pitch deck | Chưa có file deck được xác nhận |
| Demo environment | Chưa xác nhận |
| User/session demo account | Chưa xác nhận |
| Property dataset có source | Chưa xác nhận |
| Session 1 saved state | Chưa xác nhận |
| Session 2 resume state | Chưa xác nhận |
| Fallback screenshots/video | Chưa có bằng chứng |

## Pre-demo checklist

### Trước 1–2 ngày

- [ ] Chốt thời lượng và audience.
- [ ] Gán owner cho từng vai trò.
- [ ] Chốt đúng build/môi trường demo.
- [ ] Xác minh dữ liệu `[Căn A–E]`, source và trạng thái.
- [ ] Kiểm tra account/session không chứa dữ liệu cá nhân thật.
- [ ] Rehearsal toàn bộ Session 1 và Session 2.
- [ ] Ghi lại thời lượng từng cảnh và điểm chuyển người nói.
- [ ] Chuẩn bị fallback cho từng evidence checkpoint.

### Trước 60 phút

- [ ] Kiểm tra kết nối, màn hình, font và độ phân giải.
- [ ] Kiểm tra đúng account và trạng thái bắt đầu Session 1.
- [ ] Kiểm tra cách chuyển sang Session 2.
- [ ] Xóa notification hoặc dữ liệu không liên quan khỏi màn hình.
- [ ] Mở sẵn deck, demo và fallback theo thứ tự.
- [ ] Không thay đổi dữ liệu demo sau lần kiểm tra cuối nếu chưa rehearsal lại.

### Trước 10 phút

- [ ] Chạy smoke path ngắn.
- [ ] Xác nhận presenter/operator communication.
- [ ] Bật timekeeper.
- [ ] Đóng ứng dụng hoặc tab không liên quan.
- [ ] Xác nhận phương án dừng an toàn nếu demo lỗi.

## Run of show

| Mốc | Nội dung | Thời lượng mục tiêu | Owner |
|---|---|---:|---|
| 00:00 | Problem và product positioning | 0:30 | TBD |
| 00:30 | Session 1: conversation + extraction | 0:45 | TBD |
| 01:15 | Clarification + profile | 0:45 | TBD |
| 02:00 | Top-3 recommendations | 1:00 | TBD |
| 03:00 | Feedback + shortlist | 0:45 | TBD |
| 03:45 | Chuyển Session 2 + recap | 0:45 | TBD |
| 04:30 | Personalized recommendation | 0:45 | TBD |
| 05:15 | Compare + outcome | 0:45 | TBD |
| 06:00 | Kết luận | 0:20 | TBD |

Thời lượng cuối cùng cần điều chỉnh theo giới hạn của chương trình.

## Fallback matrix

| Lỗi | Cách phản hồi | Fallback được phép | Claim không được nói |
|---|---|---|---|
| AI không trả lời | Nói ngắn rằng live response gặp lỗi và chuyển sang bằng chứng dự phòng | Ảnh/video từ đúng build đã được xác minh | Không nói live flow đã thành công |
| Profile không cập nhật | Chuyển sang state đã chuẩn bị và nói rõ đây là state dự phòng | Screenshot có timestamp/version | Không claim extraction vừa chạy đúng |
| Recommendation không tải | Hiển thị dữ liệu dự phòng có source | Property cards đã xác minh | Không bịa kết quả hoặc nguồn |
| Feedback không lưu | Không tiếp tục giả vờ Session 2 học từ feedback live | Dùng pre-seeded journey và nói rõ | Không claim feedback vừa được persist |
| Resume sai | Dừng claim memory live; chuyển sang expected-state capture | Video/screenshot đã kiểm chứng | Không diễn giải recap sai là đúng |
| Mất mạng | Chuyển deck/storyboard | Offline deck và captures | Không che giấu nguyên nhân nếu được hỏi |

## Go / No-Go

### Go khi

- happy path đã rehearsal trên đúng môi trường;
- property facts có source;
- Session 2 có bằng chứng resume đáng tin cậy;
- fallback đã mở được;
- presenter biết rõ claim nào là target và claim nào có kết quả.

### No-Go hoặc chuyển sang recorded demo khi

- resume/memory không ổn định;
- dữ kiện căn hộ chưa xác minh;
- live flow có nguy cơ lộ dữ liệu cá nhân;
- các failure checkpoint chưa có fallback trung thực;
- team chưa thống nhất narrative.

## Rehearsal log

| Lần | Ngày | Build/Môi trường | Thời lượng | Kết quả | Lỗi chính | Action | Owner |
|---|---|---|---:|---|---|---|---|
| R-TBD | TBD | TBD | TBD | Chưa chạy | TBD | TBD | TBD |

Không đánh dấu demo ready nếu chưa có rehearsal log và người quyết định go/no-go.
