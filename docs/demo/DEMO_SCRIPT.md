# Demo Script — AI Home Search Companion

## Trạng thái

- Bản nháp lời thoại; chưa rehearsal
- Dùng cùng `docs/demo/DEMO_STORYBOARD.md`
- Placeholder `[Căn ...]`, `[Nguồn]` phải được thay bằng dữ liệu đã xác minh trước demo

## Mở đầu — 30 giây

**Presenter:**

> Người tìm nhà thường không thiếu tin đăng. Vấn đề là họ phải xử lý quá nhiều thông tin rời rạc, khó nhớ đã xem gì, vì sao đã loại một căn và thường phải bắt đầu lại khi quay lại sau vài ngày. Sản phẩm của chúng tôi là AI Home Search Companion, tập trung vào việc giúp người dùng tiếp tục hành trình và thu hẹp lựa chọn.

Không giới thiệu sản phẩm là BookingBot hoặc hệ thống tự động hóa sale.

## Session 1 — Lần đầu tìm nhà

### 1. Yêu cầu tự nhiên

**Demo user:**

> Tôi muốn thuê nhà khoảng 18 triệu, gia đình 3 người, tôi làm ở Cầu Giấy.

**Presenter:**

> AI không yêu cầu người dùng bắt đầu bằng một form dài. Nó trích xuất ngay những gì đã biết và hiển thị minh bạch trong profile.

Điểm cần chỉ: loại giao dịch, ngân sách, household size, workplace và các trường còn thiếu.

### 2. Clarification

Cho AI hỏi các thông tin còn thiếu theo ngữ cảnh, ưu tiên:

- cần tối thiểu bao nhiêu phòng ngủ;
- commute tối đa có thể chấp nhận;
- trường học có phải tiêu chí quan trọng hay không.

**Presenter:**

> AI chỉ hỏi điều còn thiếu và giúp người dùng phân biệt must-have với tiêu chí linh hoạt.

Không nói “AI đạt 90%” nếu chưa có test report.

### 3. Profile confirmation

**Demo user:** Xác nhận profile hoặc sửa một chi tiết nếu luồng demo đã chuẩn bị tình huống này.

**Presenter:**

> Người dùng có thể xem, sửa hoặc xóa điều AI ghi nhớ; memory không phải một hộp đen.

### 4. Recommendation

Hiển thị tối đa 3 căn có nguồn đã xác minh.

**Presenter:**

> Mỗi recommendation giải thích điều gì phù hợp, điều gì chưa phù hợp và dữ liệu nào còn thiếu. AI diễn giải dữ kiện nguồn thay vì tự tạo thông tin căn hộ.

Không đọc toàn bộ card; chỉ chỉ ra một matched criterion, một trade-off và source.

### 5. Feedback

**Demo user:**

- Save `[Căn A]`.
- Reject `[Căn B]` với lý do “bếp nhỏ”.
- Reject `[Căn C]` với lý do “đi làm xa”.

**Presenter:**

> Sản phẩm không chỉ ghi nhận nút bấm. Lý do feedback trở thành context để cải thiện đề xuất ở lần quay lại.

Kết thúc Session 1 và chỉ rõ journey đã dừng tại đâu. Không nói dữ liệu đã persist nếu demo chưa chứng minh được điều đó.

## Session 2 — Quay lại và resume

### 1. Mở Journey History/Resume

Recap mục tiêu cần thể hiện:

> Lần trước bạn đang tìm căn 2PN dưới 18 triệu, ưu tiên đi Cầu Giấy dưới 35 phút. Bạn đã loại hai căn vì bếp nhỏ và thời gian di chuyển. Tôi sẽ ưu tiên lựa chọn có bếp phù hợp hơn và commute ngắn hơn.

Chỉ dùng câu trên nếu các giá trị thực sự tồn tại trong trạng thái demo. Nếu không, dùng recap đúng với dữ liệu đã lưu.

**Presenter:**

> Đây là điểm khác biệt cốt lõi: người dùng không phải nhập lại từ đầu và có thể kiểm soát recap trước khi tiếp tục.

### 2. Recommendation cá nhân hóa

Hiển thị `[Căn D/E]` từ dữ liệu đã xác minh.

**Presenter:**

> Các đề xuất mới được giải thích dựa trên feedback trước: tránh bếp nhỏ và giảm thời gian đi làm. Đây là personalization có thể nhìn thấy, không chỉ là một nhãn “AI”.

### 3. Compare

So sánh `[Căn A]` với một recommendation mới.

**Presenter:**

> AI tóm tắt trade-off theo ưu tiên của chính người dùng, đồng thời nêu rõ dữ liệu nào chưa đủ để kết luận.

## Kết thúc — 20 giây

**Presenter:**

> Giá trị của sản phẩm không nằm ở việc tạo thêm tin đăng hay tự động hóa sale. Giá trị là giúp người dùng được hiểu, được ghi nhớ và tiến gần hơn đến quyết định sau mỗi lần quay lại.

## Câu trả lời an toàn khi được hỏi

| Câu hỏi | Cách trả lời |
|---|---|
| Hệ thống đã đạt các metric chưa? | Đây là mục tiêu MVP; chỉ báo cáo kết quả khi có test report và sample size. |
| AI lấy dữ liệu căn ở đâu? | Chỉ chỉ nguồn đang dùng trong demo; không suy đoán nguồn chưa tích hợp. |
| Có tự động booking không? | MVP chỉ ghi nhận yêu cầu xem nhà ở trạng thái Pending. |
| Có dashboard cho sale không? | Đây không phải trọng tâm MVP hiện tại. |
| Có Multi-Agent không? | Demo tập trung vào giá trị người dùng; không claim kiến trúc chưa được xác nhận. |
| AI có đảm bảo recommendation đúng không? | AI giải thích theo dữ kiện có nguồn và nêu dữ liệu thiếu; người dùng vẫn kiểm soát quyết định. |

## Script readiness

- [ ] Lời thoại khớp phiên bản UI/demo thực tế.
- [ ] Mọi dữ kiện căn hộ đã thay placeholder và có nguồn.
- [ ] Các claim metric có bằng chứng hoặc được gọi đúng là target.
- [ ] Presenter và operator đã rehearsal.
- [ ] Thời lượng nằm trong giới hạn được thống nhất.

Hiện chưa có bằng chứng để đánh dấu các mục trên hoàn tất.
