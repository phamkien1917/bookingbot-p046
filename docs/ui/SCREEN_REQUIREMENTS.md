# Screen Requirements — 5 màn hình MVP

## Nguyên tắc chung

- AI là trung tâm trải nghiệm và phải tạo giá trị nhìn thấy được.
- Mọi dữ kiện căn hộ cần có nguồn; dữ liệu thiếu phải được ghi rõ.
- Người dùng có quyền xác nhận, sửa hoặc xóa memory.
- Mọi recommendation phải có giải thích.
- Không mở rộng thành booking automation, Sale Dashboard hoặc Admin Dashboard.
- Các acceptance criteria dưới đây là yêu cầu thiết kế/sản phẩm, không phải tuyên bố rằng frontend đã hoàn thành.

---

## 1. AI Conversation

### User goal

Mô tả nhu cầu tìm nhà tự nhiên, được AI hiểu đúng và biết bước tiếp theo cần cung cấp gì.

### Primary action

Gửi tin nhắn và trả lời câu hỏi làm rõ của AI.

### Required information

- nội dung hội thoại hiện tại;
- tóm tắt điều AI đã hiểu;
- profile progress;
- trường còn thiếu hoặc cần xác nhận;
- quick actions phù hợp với ngữ cảnh;
- property cards khi đã có recommendation;
- chỉ báo dữ liệu nào đến từ người dùng và dữ kiện căn hộ nào có nguồn.

### AI role

- hiểu yêu cầu tự nhiên;
- trích xuất profile;
- hỏi làm rõ có chọn lọc;
- phát hiện trade-off;
- xác nhận thay đổi memory;
- diễn giải recommendation và phản hồi theo ngữ cảnh.

### UI components

- conversation thread;
- message composer;
- profile progress;
- panel “AI đang hiểu gì về bạn”;
- clarification chips/quick actions;
- inline property card;
- trạng thái AI đang xử lý;
- liên kết sang Profile/Memory, Recommendations và Resume.

### States

- chưa có hội thoại;
- đang nhập hoặc đang xử lý;
- đã trích xuất một phần profile;
- cần làm rõ;
- phát hiện trade-off;
- đủ điều kiện recommendation;
- không đủ dữ liệu hoặc không có kết quả;
- lỗi có thể thử lại;
- resumed session với recap.

### Acceptance criteria

- Người dùng có thể bắt đầu bằng một câu tự nhiên, không phải điền form bắt buộc trước.
- Thông tin được AI trích xuất xuất hiện trong khu vực “AI đang hiểu gì về bạn”.
- Trường còn thiếu được phân biệt với trường đã biết.
- AI không hỏi lại dữ liệu đã biết nếu không có lý do thay đổi/xác nhận.
- Khi phát hiện tiêu chí mâu thuẫn, AI hỏi người dùng chọn ưu tiên.
- Property card trong chat có lý do phù hợp và nguồn dữ kiện.
- Khi quay lại, màn hình hiển thị recap và điểm tiếp tục thay vì bắt đầu trắng.

### Có thể tái sử dụng từ mock UI

- Bố cục chat ba cột, conversation thread, composer và contextual panel từ `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai_chat_booking_bot_ai/code.html`.
- Chat bubble, button, chip, màu sắc và spacing từ `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai/DESIGN.md`.
- Không tái sử dụng countdown giữ căn, tìm sale hoặc booking summary.

---

## 2. Profile / AI Memory

### User goal

Hiểu và kiểm soát những gì AI đang ghi nhớ về nhu cầu tìm nhà.

### Primary action

Xác nhận, sửa hoặc xóa một thông tin trong profile/memory.

### Required information

- loại giao dịch;
- khoảng ngân sách;
- quy mô hộ gia đình;
- khu vực ưu tiên;
- địa điểm làm việc/trường học;
- số phòng tối thiểu;
- thời điểm chuyển nhà;
- commute tối đa;
- must-have;
- ưu tiên;
- tiêu chí linh hoạt;
- trường chưa biết;
- lịch sử thay đổi có liên quan.

### AI role

- tóm tắt profile bằng ngôn ngữ dễ hiểu;
- chỉ ra trường còn thiếu hoặc chưa chắc chắn;
- giải thích thay đổi nào đến từ feedback;
- yêu cầu xác nhận trước khi coi thay đổi quan trọng là đúng.

### UI components

- profile summary;
- progress indicator;
- nhóm field theo chủ đề;
- must-have/priority/flexible chips;
- unknown-field indicator;
- edit/delete/confirm controls;
- change-history list;
- CTA quay lại hội thoại hoặc cập nhật recommendation.

### States

- profile trống;
- profile chưa hoàn chỉnh;
- chờ xác nhận;
- đã xác nhận;
- đang chỉnh sửa;
- thay đổi chưa lưu;
- đã cập nhật từ feedback;
- lỗi cập nhật.

### Acceptance criteria

- Người dùng phân biệt được dữ liệu đã xác nhận, suy ra và còn thiếu.
- Người dùng có thể sửa hoặc xóa từng memory item.
- Thay đổi được phản ánh nhất quán trong phần tóm tắt profile.
- UI giải thích khi một ưu tiên được cập nhật từ feedback.
- Không hiển thị memory như một “hộp đen” không thể kiểm soát.
- Có đường quay lại conversation và recommendation sau khi cập nhật.

### Có thể tái sử dụng từ mock UI

- Card, form control, chip, badge, typography và spacing từ `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai/DESIGN.md`.
- Sidebar/profile entry từ `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai_chat_booking_bot_ai/code.html`.
- Chưa có màn hình Profile/Memory hiện hữu để tái sử dụng nguyên trạng.

---

## 3. AI Recommendations

### User goal

Xem một tập lựa chọn ngắn, hiểu vì sao từng căn được đề xuất và phản hồi nhanh.

### Primary action

Đánh giá một recommendation bằng LIKE, DISLIKE, SAVE hoặc REJECT và cung cấp lý do khi phù hợp.

### Required information

- tối đa 3 căn;
- hình ảnh, tên, vị trí, giá, diện tích và số phòng;
- nguồn và thời điểm xác minh nếu có;
- tiêu chí phù hợp;
- tiêu chí chưa phù hợp;
- trade-off;
- dữ liệu còn thiếu;
- lý do recommendation;
- feedback state;
- liên kết tới shortlist/compare.

### AI role

- diễn giải kết quả theo profile cá nhân;
- không thay dữ kiện nguồn bằng suy đoán;
- nêu rõ điểm đạt, chưa đạt và chưa có dữ liệu;
- giải thích sự thay đổi so với recommendation hoặc feedback trước.

### UI components

- recommendation summary;
- tối đa 3 explainable property cards;
- matched/unmet/unknown indicators;
- trade-off block;
- source badge;
- LIKE/DISLIKE/SAVE/REJECT controls;
- reason capture;
- CTA compare.

### States

- chưa đủ profile;
- đang tạo recommendation;
- có 1–3 kết quả;
- không có kết quả phù hợp;
- dữ liệu căn thiếu;
- đã like/dislike/save/reject;
- đang nhập lý do;
- recommendation đã thay đổi sau feedback;
- lỗi có thể thử lại.

### Acceptance criteria

- Không hiển thị quá 3 recommendation trong một tập chính.
- Mỗi recommendation có ít nhất một lý do phù hợp và phần trade-off/dữ liệu thiếu khi có.
- Mọi dữ kiện căn hộ hiển thị nguồn hoặc trạng thái chưa xác minh rõ ràng.
- Người dùng có thể SAVE hoặc REJECT trực tiếp.
- REJECT/DISLIKE cho phép ghi lý do và hiển thị xác nhận đã ghi nhận.
- Recommendation ở Session 2 chỉ rõ cách feedback trước đã ảnh hưởng đến kết quả.
- Không tự động xác nhận booking từ màn hình này.

### Có thể tái sử dụng từ mock UI

- Property card, filter chip và metadata từ `MOCKUI/stitch_booking_bot_ai_agent/danh_s_ch_c_n_h_booking_bot_ai/code.html`.
- Gallery và property facts từ `MOCKUI/stitch_booking_bot_ai_agent/chi_ti_t_c_n_h_booking_bot_ai/code.html`.
- Cần bổ sung explainability, trade-off, source và feedback; không tái sử dụng CTA đặt lịch làm hành động chính.

---

## 4. Shortlist & Compare

### User goal

So sánh các căn đang cân nhắc và hiểu lựa chọn nào phù hợp nhất với ưu tiên cá nhân.

### Primary action

Chọn các căn trong shortlist để so sánh side-by-side.

### Required information

- danh sách căn đã SAVE;
- các tiêu chí chính từ profile;
- dữ kiện của từng căn;
- nguồn và dữ liệu thiếu;
- điểm giống/khác;
- tiêu chí đạt/chưa đạt;
- feedback và lý do trước đó;
- AI trade-off summary.

### AI role

- so sánh theo profile cá nhân thay vì tiêu chí chung;
- tóm tắt trade-off quan trọng;
- không tự quyết định thay người dùng;
- chỉ ra dữ liệu chưa đủ để kết luận.

### UI components

- shortlist cards/list;
- selection controls;
- comparison table;
- pinned criteria;
- matched/unmet/unknown markers;
- AI summary;
- remove/reject controls;
- CTA quay lại recommendation hoặc hội thoại.

### States

- shortlist trống;
- shortlist có một căn;
- đủ căn để compare;
- đang chọn căn;
- đang hiển thị compare;
- dữ liệu so sánh thiếu;
- căn đã bị remove/reject;
- lỗi tải dữ liệu.

### Acceptance criteria

- Empty state hướng người dùng quay lại Recommendations.
- Người dùng có thể thêm/bỏ căn khỏi shortlist mà không mất feedback history.
- Compare hiển thị cùng một bộ tiêu chí cho các căn được chọn.
- Dữ liệu thiếu không được diễn giải thành điểm yếu hoặc điểm mạnh giả.
- AI summary nêu được ít nhất trade-off chính giữa các căn khi có đủ dữ liệu.
- Người dùng có thể tiếp tục hội thoại để điều chỉnh ưu tiên sau khi so sánh.

### Có thể tái sử dụng từ mock UI

- Property card và metadata từ `MOCKUI/stitch_booking_bot_ai_agent/danh_s_ch_c_n_h_booking_bot_ai/code.html`.
- Tab, card list và status chip từ `MOCKUI/stitch_booking_bot_ai_agent/l_ch_xem_c_a_t_i_booking_bot_ai/code.html`.
- Chưa có comparison table hoặc AI trade-off summary trong mock UI hiện tại.

---

## 5. Journey History / Resume

### User goal

Nhớ mình đã làm gì và tiếp tục hành trình mà không phải nhập lại nhu cầu.

### Primary action

Chọn “Tiếp tục từ đây”.

### Required information

- recap phiên gần nhất;
- profile/ưu tiên đang áp dụng;
- căn đã xem;
- căn đã lưu;
- căn đã loại và lý do;
- thay đổi tiêu chí;
- shortlist hiện tại;
- điểm đang dừng;
- recommendation mới nếu đã có.

### AI role

- tóm tắt lịch sử chính xác, ngắn gọn;
- nhấn mạnh điều đã học từ feedback;
- đề xuất điểm tiếp tục phù hợp;
- cho phép người dùng sửa recap nếu nhu cầu đã thay đổi.

### UI components

- session recap card;
- journey timeline;
- viewed/saved/rejected groups;
- feedback reason labels;
- profile-change markers;
- “Tiếp tục từ đây” CTA;
- liên kết tới conversation, recommendation và compare.

### States

- người dùng chưa có journey;
- có Session 1 chưa hoàn tất;
- có journey sẵn sàng resume;
- recap cần xác nhận;
- profile đã thay đổi từ phiên trước;
- không còn căn hợp lệ trong shortlist;
- lỗi tải journey.

### Acceptance criteria

- Người dùng quay lại thấy recap trước khi bị yêu cầu nhập lại dữ liệu.
- Recap gồm nhu cầu chính, feedback và điểm đang dừng.
- Căn đã loại hiển thị kèm lý do nếu lý do đã được ghi nhận.
- Người dùng có thể sửa thông tin không còn đúng.
- “Tiếp tục từ đây” đưa người dùng đến đúng context tiếp theo.
- Recommendation mới giải thích được ảnh hưởng của memory và feedback trước.
- UI không tuyên bố nhớ dữ liệu nếu dữ liệu journey không tồn tại hoặc tải lỗi.

### Có thể tái sử dụng từ mock UI

- List/card, tab và status pattern từ `MOCKUI/stitch_booking_bot_ai_agent/l_ch_xem_c_a_t_i_booking_bot_ai/code.html`.
- Sidebar/history pattern từ `MOCKUI/stitch_booking_bot_ai_agent/booking_bot_ai_chat_booking_bot_ai/code.html`.
- Không tái sử dụng trạng thái lịch hẹn, sale contact hoặc booking confirmation.
