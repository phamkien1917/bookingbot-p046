# BOOKINGBOT / AI HOME SEARCH COMPANION — PROJECT SOURCE OF TRUTH

## 0. Mục đích
Đây là tài liệu context chính cho Codex/AI coding assistant khi làm việc trong VS Code.
Nếu tài liệu cũ mâu thuẫn với file này, ưu tiên file này.
Không tự mở rộng scope nếu chưa được yêu cầu.

## 1. Định vị sản phẩm
Tên đang dùng: BookingBot AI Agent
Định vị hiện tại: AI Home Search Companion

Tuyên bố sản phẩm:
BookingBot là trợ lý AI đồng hành cùng người dùng trong hành trình tìm nhà. AI giúp người dùng mô tả nhu cầu bằng ngôn ngữ tự nhiên, làm rõ nhu cầu còn mơ hồ, ghi nhớ lịch sử tìm kiếm qua nhiều phiên, học từ phản hồi thích/không thích, cá nhân hóa gợi ý, so sánh lựa chọn và tiếp tục hành trình ở đúng điểm đã dừng.

Trọng tâm:
AI phải nằm ở trung tâm trải nghiệm.
Không xây một website bất động sản nhiều chức năng rồi gắn chatbot vào.

## 2. Problem First
Người dùng không thiếu tin bất động sản. Họ gặp:
- quá tải thông tin;
- khó nhớ đã xem căn nào;
- không nhớ vì sao đã loại một căn;
- khó so sánh nhiều căn;
- chưa hiểu rõ tiêu chí nào thực sự quan trọng;
- mỗi lần quay lại gần như phải tìm từ đầu;
- dễ bỏ cuộc hoặc ra quyết định cảm tính.

Problem statement:
Người tìm nhà phải xử lý nhiều thông tin rời rạc trong hành trình kéo dài nhiều ngày/tuần. Các nền tảng hiện tại không nhớ quá trình tìm kiếm, không học từ phản hồi và không giúp người dùng tiến gần hơn đến quyết định sau mỗi lần quay lại.

## 3. WHO — Người dùng mục tiêu
MVP ưu tiên:
Người trẻ/gia đình trẻ đang tìm THUÊ nhà để ở:
- khoảng 24–35 tuổi;
- ở Hà Nội hoặc thành phố lớn;
- dự kiến chuyển nhà trong 1–3 tháng;
- có ngân sách tương đối rõ;
- phải xem nhiều tin trong nhiều ngày;
- cần cân bằng vị trí, ngân sách, diện tích, số phòng, nơi làm việc, trường học, tiện ích.

Không lấy Sale làm người dùng trung tâm.
Sale chỉ là stakeholder phụ/future scope.

## 4. Desired Outcome
Người dùng muốn:
- không phải nhập lại nhu cầu mỗi lần quay lại;
- giảm thời gian đọc tin không phù hợp;
- nhớ rõ căn đã xem;
- biết vì sao một căn phù hợp/không phù hợp;
- dễ so sánh;
- hiểu rõ ưu tiên và sự đánh đổi;
- tạo được shortlist;
- tự tin hơn khi ra quyết định.

Desired Outcome:
“Giúp người tìm nhà tiếp tục hành trình ở đúng điểm đã dừng, nhanh chóng thu hẹp lựa chọn và tự tin hơn khi quyết định.”

## 5. Business/Product Outcome
Business Outcome MVP:
Giữ người dùng quay lại và tiếp tục hành trình tìm nhà.

North Star Metric:
Tỷ lệ người dùng quay lại phiên thứ hai và tiếp tục tìm nhà bằng hồ sơ/lịch sử/phản hồi đã có mà không phải nhập lại từ đầu.

Metrics:
- Profile Completion Rate
- Time to First Value
- Second-session Return Rate
- Resume Success Rate
- Repeat-question Rate
- Feedback Rate
- Shortlist Creation Rate
- Recommendation Acceptance
- Hallucination Rate

## 6. Vai trò của AI
AI phải làm tốt:
1. Understand
   - hiểu yêu cầu tự nhiên;
   - trích xuất thông tin đã có.
2. Clarify
   - xác định thông tin còn thiếu;
   - hỏi đúng câu tiếp theo theo ngữ cảnh;
   - không hỏi một form cố định.
3. Detect trade-offs
   - phát hiện tiêu chí mâu thuẫn/khó đáp ứng cùng lúc;
   - hỏi người dùng muốn ưu tiên điều gì.
4. Build memory
   - nhớ hồ sơ nhu cầu;
   - nhớ căn đã xem;
   - nhớ căn đã lưu/loại;
   - nhớ lý do thích/không thích;
   - nhớ tiêu chí thay đổi.
5. Personalize
   - học từ feedback;
   - điều chỉnh trọng số ưu tiên;
   - lần sau gợi ý phù hợp hơn.
6. Explain
   - giải thích vì sao đề xuất;
   - nêu tiêu chí đạt/chưa đạt/chưa có dữ liệu;
   - so sánh trade-off giữa các căn.

AI không được:
- bịa giá;
- bịa địa chỉ;
- bịa trạng thái căn;
- viết raw SQL để thao tác DB;
- tự commit thao tác nhạy cảm;
- tự xác nhận booking;
- tự tư vấn pháp lý/tín dụng.

## 7. Kiến trúc MVP
Ưu tiên đơn giản, dễ debug, chạy end-to-end trong 6 tuần.

Luồng:
User
→ AI Agent / Planner
→ Tool có schema cố định
→ Service
→ Repository
→ PostgreSQL
→ JSON result
→ AI giải thích

Không dùng trong MVP nếu chưa thực sự cần:
- Multi-Agent
- Microservices
- Event Bus
- TSP
- Redis orchestration phức tạp
- Vector DB nếu PostgreSQL đủ
- Google Calendar 2 chiều
- CRM thật
- Notification đa kênh
- Dashboard Sale phức tạp
- Mobile app riêng

## 8. Planner–Executor hiện tại
Team đang thử Planner–Executor:
- Planner (LLM): hiểu yêu cầu, xác định hành động, chọn Tool.
- Executor: thực thi Tool.
- Tool: validate input/output và gọi business service.
- Service: xử lý nghiệp vụ.
- Repository: truy vấn PostgreSQL.
- LLM: nhận kết quả có cấu trúc và giải thích.

Lỗi kỹ thuật đang gặp:
LLM → Tool → SQL → Tool Result → LLM chưa ổn định.

Khả năng lỗi:
- sai tên tham số;
- schema không khớp;
- Tool chưa bind/register đúng;
- async/await;
- SQLAlchemy session;
- ORM object không serialize;
- tool_call_id/ToolMessage không khớp;
- graph routing sai.

Nguyên tắc debug:
1. Repository trực tiếp.
2. Service trực tiếp.
3. Tool trực tiếp, chưa dùng LLM.
4. Tool trả JSON chuẩn.
5. Cho LLM gọi 1 Tool.
6. Sau khi ổn mới thêm Tool tiếp theo.

## 9. Bộ Tool MVP
Ưu tiên 5 Tool:

1. update_user_profile
   - cập nhật nhu cầu/ưu tiên.

2. search_properties
   - tìm căn theo hard constraints.

3. record_property_feedback
   - lưu LIKE/DISLIKE/SAVE/REJECT;
   - lưu lý do;
   - ghi nhận preference mới.

4. get_user_journey
   - lấy profile;
   - lịch sử;
   - căn đã xem/lưu/loại;
   - lý do;
   - điểm đang dừng.

5. compare_properties
   - so sánh các căn theo hồ sơ cá nhân.

Tool result chuẩn:
{
  "success": true,
  "data": {},
  "error": null,
  "source": "POSTGRESQL",
  "tool_name": "..."
}

Khi lỗi:
{
  "success": false,
  "data": null,
  "error": {
    "code": "...",
    "message": "..."
  },
  "source": "...",
  "tool_name": "..."
}

## 10. Data model tối thiểu
users
- id
- name
- email_or_identifier
- created_at

user_profiles
- user_id
- transaction_type
- budget_min
- budget_max
- household_size
- preferred_areas
- workplace_locations
- school_locations
- bedroom_min
- move_in_date
- max_commute_minutes
- must_have
- priorities
- flexible_criteria
- unknown_fields
- updated_at

properties
- id
- title
- transaction_type
- district
- address
- rent_price
- sale_price
- bedrooms
- area
- property_type
- furnished
- pets_allowed
- status
- source
- verified_at

property_feedback
- id
- user_id
- property_id
- action: LIKE | DISLIKE | SAVE | REJECT
- reason
- created_at

user_journey_events
- id
- user_id
- event_type
- payload_json
- created_at

shortlist
- id
- user_id
- property_id
- created_at

## 11. Recommendation MVP
Không cần ML model phức tạp.

Bước 1 — Hard filter:
- ngân sách cứng;
- đúng loại giao dịch;
- đủ số phòng;
- đúng khu vực nếu must-have;
- trạng thái hợp lệ.

Bước 2 — Soft scoring:
- khu vực;
- khoảng giá;
- số phòng;
- diện tích;
- commute;
- preferences học được từ feedback.

Bước 3 — AI explanation:
AI chỉ diễn giải kết quả backend:
- tiêu chí đạt;
- chưa đạt;
- trade-off;
- dữ liệu thiếu;
- vì sao tốt hơn/khác căn đã xem trước.

## 12. Memory / Retention Loop
Session 1:
Conversation
→ Profile
→ Recommendation
→ Feedback
→ Memory
→ Shortlist

Session 2:
AI recap
→ dùng lại profile
→ dùng lại lịch sử
→ gợi ý mới phù hợp hơn
→ so sánh với căn cũ
→ tiếp tục hành trình.

Retention loop:
Conversation
→ Profile
→ Recommendation
→ Feedback
→ Memory
→ Better recommendation next session
→ Return

## 13. UX/UI MVP
AI phải là trung tâm.

Màn hình 1 — AI Conversation
- chat chính;
- profile progress;
- “AI đang hiểu gì về bạn”;
- quick actions;
- property card xuất hiện trong chat.

Màn hình 2 — User Profile / AI Memory
- nhu cầu hiện tại;
- ưu tiên;
- must-have;
- flexible criteria;
- lịch sử thay đổi;
- sửa/xóa memory.

Màn hình 3 — AI Recommendations
- tối đa 3 căn;
- lý do phù hợp;
- trade-offs;
- feedback buttons.

Màn hình 4 — Shortlist & Compare
- căn đang cân nhắc;
- so sánh side-by-side;
- AI summary.

Màn hình 5 — Journey History / Resume
- lần trước đã làm gì;
- căn đã xem;
- căn đã loại và lý do;
- “tiếp tục từ đây”.

Booking:
Chỉ cần nút “Tôi muốn xem căn này”
→ ghi nhận request/Pending.
Không xây hệ thống booking phức tạp trong MVP.

## 14. Demo chính
Session 1:
User: “Tôi muốn thuê nhà khoảng 18 triệu, gia đình 3 người, tôi làm ở Cầu Giấy.”

AI:
- trích xuất;
- hỏi thêm số phòng;
- hỏi commute;
- hỏi trường học nếu có;
- tạo profile;
- tìm 3 căn.

User:
- lưu căn A;
- loại căn B vì bếp nhỏ;
- loại căn C vì đi làm xa.

System lưu feedback.

Session 2:
AI mở đầu:
“Lần trước anh/chị đang tìm căn 2PN dưới 18 triệu, ưu tiên đi Cầu Giấy dưới 35 phút. Anh/chị đã loại 2 căn vì bếp nhỏ và thời gian di chuyển. Tôi đã ưu tiên các căn có bếp rộng hơn và thời gian đi làm ngắn hơn. Hiện có 2 phương án mới.”

Demo này phải chứng minh:
- memory;
- personalization;
- retention;
- explainability;
- AI value.

## 15. Success criteria MVP
- AI trích xuất đúng thông tin: >= 90%
- AI phát hiện đúng trường còn thiếu: >= 90%
- AI không hỏi lại dữ liệu đã biết: >= 90%
- Hồ sơ được user xác nhận đúng: >= 90%
- Recommendation có giải thích: 100%
- Dữ liệu căn có source: 100%
- AI bịa giá/địa chỉ/trạng thái: 0
- Có >=1 feedback trong >=70% phiên test
- Có shortlist trong >=60% phiên test
- User quay lại session 2 trong test: mục tiêu >=50%

Đây là giả thuyết mục tiêu MVP, không phải cam kết kinh doanh.

## 16. Roadmap 6 tuần
Week 1 — Problem validation
- phỏng vấn 5–8 người;
- chốt persona/problem statement;
- Who–What–How;
- Outcome;
- OST;
- schema profile/feedback.

Week 2 — Chat + Profile
- AI conversation;
- extraction;
- missing-field detection;
- profile live update;
- edit profile;
- seed data.

Week 3 — Search + Explain
- hard filter;
- soft scoring;
- search_properties;
- top 3;
- AI explanation;
- hallucination guardrail.

Week 4 — Feedback + Memory
- save/like/dislike/reject;
- reason;
- persistent history;
- preference update;
- get_user_journey.

Week 5 — Return Experience
- resume journey;
- recap previous session;
- improved recommendation;
- shortlist;
- compare.

Week 6 — Evaluation + Demo
- test 2 sessions/user;
- time-to-first-value;
- repeat-question rate;
- profile accuracy;
- recommendation relevance;
- fix bugs;
- final demo.

## 17. Opportunity Solution Tree
Outcome:
Tăng tỷ lệ user quay lại session 2 và tiếp tục mà không phải nhập lại nhu cầu.

Opportunity 1: User chưa thấy value sớm.
Solutions:
- extract từ câu đầu;
- live profile;
- gợi ý sơ bộ sau 3–5 câu.

Opportunity 2: User phải tìm lại từ đầu.
Solutions:
- persistent profile;
- history;
- AI recap;
- resume journey.

Opportunity 3: Recommendation chung chung.
Solutions:
- feedback;
- learn preferences;
- rescore;
- explain changes.

Opportunity 4: User khó ra quyết định.
Solutions:
- shortlist;
- compare;
- trade-off summary;
- checklist xem nhà.

## 18. Impact Mapping
Goal:
Tăng tỷ lệ user quay lại và tiếp tục hành trình tìm nhà.

Actors:
- người tìm nhà;
- AI companion;
- admin dữ liệu.

Desired impacts:
- user chia sẻ đủ context;
- user phản hồi thích/không thích;
- user lưu shortlist;
- user quay lại;
- AI không hỏi lại;
- AI gợi ý tốt hơn sau feedback.

Deliverables:
- conversational onboarding;
- memory;
- feedback;
- recommendation;
- shortlist;
- resume journey.

## 19. Không tự ý xây thêm
Không mở rộng nếu chưa có yêu cầu:
- Multi-Agent
- Microservices
- Event-driven architecture
- Kafka/Redis event bus
- TSP sale assignment
- advanced soft hold
- Google Calendar 2-way sync
- CRM integration
- SMS/Zalo/Push multi-channel
- complex Sale Dashboard
- AI Pricing
- AI Analytics
- investment advisor
- legal/loan advisor
- mobile native app

Lý do:
Dự án chỉ 6 tuần và chương trình cần làm nổi bật vai trò AI.

## 20. Coding principles cho Codex
1. Ưu tiên code đơn giản, modular, testable.
2. Không over-engineer.
3. Mọi Tool có Pydantic/JSON schema rõ.
4. LLM không truy cập DB trực tiếp.
5. Repository chịu SQL/ORM.
6. Service chịu business logic.
7. Tool adapter chịu validate/serialize.
8. LLM chỉ hiểu/chọn tool/giải thích.
9. Mọi property fact phải có source.
10. Không tạo fake fact trong response.
11. Log tool name, arguments, result, error, latency, session/user.
12. Test Repository → Service → Tool.
13. Tool test pass rồi mới nối LLM.
14. Giữ một happy path end-to-end trước khi thêm exception.

## 21. Source-of-truth priority
Các tài liệu cũ có thể thiên về:
- booking/sale automation;
- Multi-Agent/Microservices;
- Soft Hold/TSP/Calendar.

Xem chúng là tài liệu lịch sử/future scope.

Ưu tiên hiện tại:
**AI-centered + user-centered + memory + personalization + retention.**

## 22. Prompt mặc định cho Codex
Khi xử lý yêu cầu trong repo:
1. Việc này phục vụ Outcome nào?
2. Có nằm trong MVP không?
3. AI thực sự cần làm gì?
4. Backend cần làm gì?
5. Data contract là gì?
6. Test tối thiểu nào chứng minh feature đúng?

Không tự thêm kiến trúc hoặc dependency lớn.
Nếu phát hiện yêu cầu mâu thuẫn với scope, cảnh báo trước khi code.
