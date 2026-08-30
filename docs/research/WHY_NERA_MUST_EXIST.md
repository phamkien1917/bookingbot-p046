# Vì sao Nera cần tồn tại — Luận cứ từ nghiên cứu

**Mã tài liệu:** `docs/research/WHY_NERA_MUST_EXIST.md`
**Nguồn dữ liệu:** [`FIELD_RESEARCH_SYNTHESIS.md`](FIELD_RESEARCH_SYNTHESIS.md) (n=20 môi giới, n=30 người tìm nhà, 6 phỏng vấn sâu, Hà Nội 08/2026), báo cáo Gemini Deep Research 08/2026, NAR, HBR, VARS, Batdongsan CSS.
**Mục đích:** Trả lời câu hỏi của ban giám khảo — "Vấn đề này có thật không, và tại sao phải là Nera chứ không phải một công cụ đã có?"

---

## 1. Vấn đề: phễu đứt gãy kép, đã được đo

Thị trường môi giới bất động sản Việt Nam có một nghịch lý: công nghệ tìm kiếm phát triển nhưng tốc độ và chất lượng kết nối offline không theo kịp. Khảo sát thực địa xác nhận cả hai phía đều nghẽn:

**Phía người tìm nhà.** Khách mô tả nhu cầu bằng trung bình 6,4 tiêu chí nhưng bộ lọc web chỉ đáp ứng 2,4 — hơn 62% nhu cầu không có cách nào lọc. 90% phải nhập lại bộ lọc từ đầu mỗi phiên tìm. 63% lần liên hệ phải chờ trên một giờ hoặc bị bỏ rơi. Hơn một nửa số lượt đi xem thực tế gặp tin ảo hoặc bị dắt sang căn khác.

**Phía môi giới.** Mỗi người mất 45 phút mỗi ngày chỉ để nhắn tin chốt lịch. 85% bị trùng lịch ít nhất một lần trong ba tháng. Cứ 10 khách để lại thông tin thì 3 người bị bỏ quá 24 giờ. Toàn thị trường có khoảng 300.000 người hành nghề, chỉ 13% có chứng chỉ, gần như tất cả điều phối lịch bằng Zalo.

Đây không phải khó chịu vặt. Đây là chỗ giá trị giao dịch bị rò rỉ: khách bỏ đi, môi giới mất doanh thu, sàn mất uy tín.

---

## 2. Vì sao các giải pháp đang có không bịt được lỗ này

### Marketplace và trang rao vặt (Batdongsan, Chợ Tốt)

Làm tốt việc trưng bày tin, thất bại ở việc chắp nối. Kiến trúc lõi là bộ lọc cứng: quận, giá, số phòng, diện tích. Những tiêu chí quyết định việc thuê hay không — yên tĩnh, không chung chủ, ngõ không ngập, gần chỗ làm tính theo thời gian đi — không nằm trong bất kỳ ô chọn nào. Trang cũng không giữ ngữ cảnh: mỗi lần quay lại là bắt đầu lại. Và các trang này bán lead cho môi giới chứ không chịu trách nhiệm về việc lead đó có được trả lời hay không.

### Chatbot hỏi đáp thông thường

Trả lời được câu hỏi nhưng có hai điểm chết. Thứ nhất, dễ bịa dữ liệu — với bất động sản, một căn nhà bịa ra là mất khách vĩnh viễn. Thứ hai, nó dừng ở câu trả lời, không chuyển được cuộc hội thoại thành một lịch hẹn có người chịu trách nhiệm. Khách vẫn phải tự nhắn môi giới, và vòng lặp chờ đợi lặp lại.

### CRM cho sàn (MeeyCRM, CloudGO, SlimCRM)

Giúp quản lý nắm được lead, chia lead, đo KPI. Nhưng CRM không tự trả lời khách trong 5 phút đầu, không tự hỏi lại khách những tiêu chí còn thiếu, không tự đối chiếu lịch ba bên để chốt giờ. Nó là sổ cái, không phải người trực. Khoảng trống "từ lúc khách nhắn đến lúc có lịch hẹn" vẫn phải lấp bằng tay.

### Thuê thêm nhân viên trực

Không kinh tế và không bao phủ 24/7. Khách nhắn lúc 10 giờ tối — thời điểm hứng thú cao nhất — thì không ai trả lời. Chi phí biên của mỗi lead tăng tuyến tính theo lượng quảng cáo sàn đổ ra.

---

## 3. Vì sao phải là Nera — mỗi điểm nghẽn buộc ra một năng lực

Nera không phải tập hợp tính năng chọn tùy hứng. Từng năng lực là câu trả lời trực tiếp cho một điểm nghẽn đã đo được.

| Điểm nghẽn (bằng chứng) | Năng lực bắt buộc của Nera | Vì sao không thể thiếu |
| :--- | :--- | :--- |
| 62% tiêu chí không lọc được; 90% phải nhập lại (PTN-01, PTN-04) | Tìm kiếm bằng ngôn ngữ tự nhiên + bộ nhớ ngữ cảnh đa lượt | Khách nói cách khách nghĩ, không phải cách database lưu. Hệ thống phải nhớ để lần sau không hỏi lại. |
| 63% chờ trên 1 giờ; 30% lead bỏ rơi quá 24h (PTN-02, H3, H4) | Phản hồi dưới 1 phút, 24/7, tự phân loại ý định | "Thời điểm vàng 5 phút" là quy luật đã được chứng minh. Chỉ máy mới trực được lúc 10 giờ tối. |
| 45 phút/ngày chốt lịch; 85% trùng lịch (PTN-03, H1, H2) | Đối soát lịch ba bên tự động + khóa giữ chỗ 15 phút (row-level lock) | Trùng lịch chỉ hết khi có một nguồn sự thật duy nhất về slot trống, cập nhật tức thời. |
| 53% lượt xem gặp tin ảo (PTN-05) | SQL grounding trên dữ liệu thật + xác thực căn còn trống | Hệ thống tuyệt đối không được "vẽ" ra nhà. Mọi căn đưa cho khách phải truy được về bản ghi thật. |
| Trách nhiệm pháp lý thuộc về sàn (Luật 2024, Điều 61–63) | Human-in-the-loop: Sale phải bấm duyệt lịch mới thành chính thức | Dẫn khách đi xem phát sinh chi phí thật. Quyền quyết định và trách nhiệm phải nằm ở con người. |

Bỏ bất kỳ dòng nào, phễu lại đứt ở đúng chỗ đó.

---

## 4. Vì sao là bây giờ

Ba điều kiện vừa hội tụ, trước đây chưa có:

**Luật Kinh doanh Bất động sản 2024** (hiệu lực 01/08/2024) cấm hành nghề môi giới tự do, buộc hàng trăm nghìn cá nhân quy về sàn có pháp nhân. Sàn giờ chịu trách nhiệm về dòng tiền hoa hồng và tính hợp pháp giao dịch, nên không thể để nhân viên dùng Zalo cá nhân — dữ liệu khách phải là tài sản của sàn. Thị trường mua phần mềm chuyển từ B2C nhỏ giọt sang B2B theo tài khoản. Khảo sát xác nhận: 85% môi giới và quản lý sẵn sàng trả, trung vị 300.000đ/tài khoản/tháng.

**Chi phí mô hình ngôn ngữ đủ rẻ** để trả lời mọi lead trong một phút mà vẫn có biên. Xu hướng 2026 là thay cổng tìm kiếm bằng bộ lọc bằng trợ lý đàm thoại.

**Hạ tầng bản đồ mở** (Goong Maps API) cho phép tính thời gian di chuyển thực tế — thứ khách hỏi nhiều nhất mà không trang nào trả lời được.

---

## 5. Kết luận

Nera không phải một chatbot thêm thắt. Nó là lớp kết nối còn thiếu giữa "khách tìm thấy tin trên mạng" và "khách đứng trong căn nhà đó với môi giới". Khoảng trống này, khảo sát đã đo bằng số: 45 phút mỗi ngày, 85% trùng lịch, 30% lead rơi, 62% nhu cầu không lọc được. Các công cụ hiện có mỗi thứ chạm được một mảnh — không thứ nào đi hết từ câu nhắn đầu tiên đến lịch hẹn được sàn duyệt. Đó là lý do Nera cần tồn tại, và lý do phải là bây giờ.
