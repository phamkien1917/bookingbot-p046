# 🎬 KỊCH BẢN VIDEO DEMO 5 PHÚT: DỰ ÁN NERA (P-046)
**Hệ thống Trợ lý Bất động sản AI Đa tác nhân (AI Multi-Agent Real Estate Companion)**

* **Thời lượng mục tiêu:** 5 phút (05:00)
* **Chất lượng video đề xuất:** 1080p Full HD (60fps) / 2K, tỷ lệ 16:9
* **Trọng tâm demo:** Chat Multi-Agent, Trí nhớ dài hạn (Semantic Memory), Đặt lịch thông minh & Phê duyệt thời gian thực (Sale Approval Flow), Tối ưu lộ trình (Route Map).

---

## 📋 CÔNG TÁC CHUẨN BỊ TRƯỚC KHI QUAY (30 GIÂY SETUP)

1. **Terminal 1 (Backend):** `python -m uvicorn src.main:app --reload --port 8000` (đang chạy).
2. **Terminal 2 (Frontend):** `npm run dev` trong thư mục `frontend` (đang chạy tại `http://localhost:3000`).
3. **Tab Trình duyệt 1 (Khách hàng):** Mở `http://localhost:3000` (đăng nhập tài khoản khách hàng nếu có).
4. **Tab Trình duyệt 2 (Sale Staff):** Mở tab ẩn danh hoặc trình duyệt khác tại `http://localhost:3000/sale` (đăng nhập sẵn tài khoản sale, ví dụ: `hanh.bt.sale0@xhome.com`).

---

## ⏱️ CHI TIẾT TỪNG PHÂN CẢNH (TIMELINE)

### 📌 PHẦN 1: MỞ ĐẦU & GIỚI THIỆU TỔNG QUAN (0:00 – 0:40)

| Mốc thời gian | 🖥️ Thao tác trên màn hình (Hành động) | 🎙️ Lời thoại thuyết minh (Nói gì) |
| :--- | :--- | :--- |
| **0:00 - 0:20** | - Quay màn hình Trang chủ Nera (`http://localhost:3000`).<br>- Cuộn trang nhẹ nhàng từ trên xuống dưới: lướt qua Hero section, các căn hộ nổi bật, và phần giới thiệu trợ lý ảo. | *"Xin chào thầy cô và các bạn! Hôm nay em xin trình bày video demo 5 phút giới thiệu sản phẩm **Nera – Trợ lý bất động sản AI thông minh** thuộc dự án P-046. Trong thị trường bất động sản, người mua thường tốn rất nhiều thời gian lọc hàng ngàn tin đăng và gặp khó khăn khi kết nối lịch xem nhà với môi giới. Nera ra đời để giải quyết bài toán đó bằng kiến trúc Multi-Agent hiện đại, Semantic Memory và luồng điều phối bán hàng tự động."* |
| **0:20 - 0:40** | - Di chuột lên thanh điều hướng (Header), chỉ vào nút **"Nói với Nera"** và bấm vào để chuyển sang trang `/chat`. | *"Nera không phải là một chatbot đơn lẻ, mà là một hệ thống đa tác nhân gồm **Supervisor Agent, Inventory Agent và Booking Agent**, phối hợp nhịp nhàng để hiểu ngôn ngữ tự nhiên, phân tích bất động sản đa tiêu chí và hỗ trợ đặt lịch xem nhà tức thì."* |

---

### 📌 PHẦN 2: TÌM KIẾM TỰ NHIÊN & TRÒ CHUYỆN ĐA LƯỢT (0:40 – 1:50)

| Mốc thời gian | 🖥️ Thao tác trên màn hình (Hành động) | 🎙️ Lời thoại thuyết minh (Nói gì) |
| :--- | :--- | :--- |
| **0:40 - 1:15** | - Trong ô chat, gõ câu lệnh tìm kiếm ban đầu:<br>`tìm nhà dưới 5 tỷ ở miền bắc`<br>- Nhấn Enter.<br>- Nera phản hồi danh sách các căn hộ/nhà ở Miền Bắc giá $\le$ 5 tỷ kèm thẻ tóm tắt: giá bán, diện tích, vị trí và mục *"Vì sao Nera gợi ý căn này?"*. | *"Đầu tiên là tính năng **Tìm kiếm bằng ngôn ngữ tự nhiên**. Em nhập yêu cầu 'tìm nhà dưới 5 tỷ ở miền bắc'. Inventory Agent lập tức xử lý ngôn ngữ, trích xuất thực thể khu vực và khoảng giá, sau đó truy vấn cơ sở dữ liệu để đưa ra các căn nhà phù hợp nhất kèm giải thích lý do đề xuất rất trực quan."* |
| **1:15 - 1:50** | - Nhập câu hỏi tinh chỉnh ngữ cảnh (Multi-turn Context):<br>`chỉ lấy căn 2 phòng ngủ ở cầu giấy`<br>- Nhấn Enter.<br>- Nera tự động giữ ngân sách $\le$ 5 tỷ, lọc tiếp theo Quận Cầu Giấy và số phòng ngủ = 2.<br>- Chỉ chuột vào các bóng chat Messenger/Zalo gọn gàng, bấm nút **"Chi tiết"** để xem thông tin mở rộng. | *"Điểm mạnh vượt trội của Nera là khả năng **duy trì ngữ cảnh đa lượt (Multi-turn Memory)**. Khi em yêu cầu 'chỉ lấy căn 2 phòng ngủ ở cầu giấy', Supervisor Agent tự động kế thừa tiêu chí ngân sách dưới 5 tỷ từ câu trước và kết hợp cùng bộ lọc mới. Giao diện chat được thiết kế theo phong cách Messenger/Zalo hiện đại, bóng chat co giãn vừa vặn theo nội dung và hỗ trợ đầy đủ hình ảnh, thông số kỹ thuật."* |

---

### 📌 PHẦN 3: TRÍ NHỚ DÀI HẠN (SEMANTIC MEMORY) (1:50 – 2:45)

| Mốc thời gian | 🖥️ Thao tác trên màn hình (Hành động) | 🎙️ Lời thoại thuyết minh (Nói gì) |
| :--- | :--- | :--- |
| **1:50 - 2:20** | - Bấm vào mục **Trí nhớ (Memory)** trên thanh điều hướng (`/memory`).<br>- Màn hình hiển thị hồ sơ khách hàng, các thông tin ưu tiên về ngân sách, khu vực, loại hình nhà ở đã được trích xuất tự động qua Mem0. | *"Một trong những tính năng cốt lõi của dự án là **Trí nhớ ngữ cảnh dài hạn (Semantic Memory)**. Hệ thống tự động phân tích các cuộc trò chuyện để trích xuất hồ sơ sở thích cá nhân hóa: từ tầm tài chính, quận huyện quan tâm, cho đến tiện ích mong muốn mà không cần người dùng phải khai báo thủ công."* |
| **2:20 - 2:45** | - Quay lại Trang chủ (`/`).<br>- Thấy Card chào mừng khách quay lại: *"Chào bạn quay lại – Tiếp tục từ nơi bạn đã dừng"*, bấm nút **"Tiếp tục hành trình"**.<br>- Hệ thống mở ra một phiên chat mới độc lập với câu hỏi định hướng sát theo nhu cầu đã lưu. | *"Khi khách hàng quay lại sau một thời gian, Nera vẫn nhớ rõ nhu cầu trước đó. Người dùng chỉ cần bấm 'Tiếp tục hành trình', Nera sẽ khởi tạo phiên tư vấn tiếp nối cực kỳ thông minh và tiện lợi."* |

---

### 📌 PHẦN 4: ĐẶT LỊCH XEM NHÀ & DUYỆT TỨC THÌ PHÍA SALE (2:45 – 4:10)

| Mốc thời gian | 🖥️ Thao tác trên màn hình (Hành động) | 🎙️ Lời thoại thuyết minh (Nói gì) |
| :--- | :--- | :--- |
| **2:45 - 3:25** | - Trong ô chat, gõ câu đặt lịch trực tiếp bằng tên dự án:<br>`đặt lịch căn CĂN HỘ Fodacon Bắc Hà – Mỗ Lao, Hà Đông ngày mai lúc 14h`<br>- Nhấn Enter.<br>- Nera tự động nhận diện căn hộ theo tên thực thể, kiểm tra slot trống của chuyên viên Sale phụ trách và tạo Tour Request `TR-XXXXX` ở trạng thái Chờ duyệt (`WAITING_APPROVAL`). | *"Tiếp theo là quy trình **Đặt lịch xem nhà thông minh**. Khách hàng chỉ cần nhắn 'đặt lịch căn Fodacon Bắc Hà ngày mai lúc 14h'. Booking Agent tự động nhận diện chính xác căn hộ, kiểm tra tính khả dụng của chuyên viên phụ trách và gửi yêu cầu đặt lịch đến hệ thống quản trị Sale."* |
| **3:25 - 3:55** | - Chuyển nhanh sang Tab 2 (Giao diện Sale: `http://localhost:3000/sale`).<br>- Trang Dashboard của Sale hiển thị ngay yêu cầu `TR-XXXXX` vừa được tạo trong danh sách **Lịch hẹn mới**.<br>- Bấm nút **"Xác nhận lịch hẹn" (Approve)**. | *"Ngay lập tức, trên giao diện làm việc của Chuyên viên Sale, yêu cầu đặt lịch xuất hiện theo thời gian thực. Sale có thể xem chi tiết thông tin căn hộ, thời gian và chỉ cần bấm một nút **Xác nhận** để đồng ý tiếp đón khách hàng."* |
| **3:55 - 4:10** | - Quay lại Tab 1 (Giao diện Khách hàng: `/chat` hoặc `/my-bookings`).<br>- Trong ô chat/danh sách lịch hẹn, trạng thái đã chuyển thành **Đã xác nhận (CONFIRMED)** kèm mã Booking `BK-XXXXX`, tên Sale và số điện thoại liên hệ. | *"Quay trở lại phía khách hàng, hệ thống lập tức cập nhật thông báo xác nhận lịch hẹn chính thức kèm mã Booking và thông tin liên hệ của chuyên viên Sale. Toàn bộ luồng kết nối giữa AI, Khách hàng và Sale diễn ra hoàn toàn tự động, minh bạch và chính xác."* |

---

### 📌 PHẦN 5: TỐI ƯU LỘ TRÌNH (SALE) & TRANG QUẢN TRỊ ADMIN (4:10 – 4:45)

| Mốc thời gian | 🖥️ Thao tác trên màn hình (Hành động) | 🎙️ Lời thoại thuyết minh (Nói gì) |
| :--- | :--- | :--- |
| **4:10 - 4:25** | - Ở Tab Sale, bấm vào menu **"Lộ trình di chuyển"** (`/sale/route-map`).<br>- Bản đồ hiển thị các điểm hẹn trong ngày và đường đi tối ưu đã được tính toán bằng thuật toán Nearest Neighbour. | *"Bên cạnh đó, Nera còn hỗ trợ tính năng **Tối ưu lộ trình di chuyển (Route Optimizer)** cho Sale, tự động sắp xếp thứ tự các điểm hẹn xem nhà trong ngày để tiết kiệm tối đa thời gian di chuyển."* |
| **4:25 - 4:45** | - Chuyển sang trang **Admin Dashboard** (`http://localhost:3000/admin`).<br>- Lướt nhanh qua các mục: Quản lý kho Bất động sản (`/admin/properties`) và Quản lý đội ngũ Sale (`/admin/sales`). | *"Đối với cấp quản lý, hệ thống cung cấp trang **Admin Dashboard** toàn diện: cho phép theo dõi toàn bộ kho bất động sản, kiểm duyệt tin đăng và phân bổ chuyên viên Sale phụ trách theo từng dự án, khu vực một cách trực quan."* |

---

### 📌 PHẦN 6: KẾT LUẬN (4:45 – 5:00)

| Mốc thời gian | 🖥️ Thao tác trên màn hình (Hành động) | 🎙️ Lời thoại thuyết minh (Nói gì) |
| :--- | :--- | :--- |
| **4:45 - 5:00** | - Quay trở lại Trang chủ Nera, hiển thị giao diện tổng thể và logo dự án. | *"Tóm lại, dự án Nera đã tích hợp thành công **FastAPI, Next.js 16, LangGraph Multi-Agent, PostgreSQL và Semantic Memory** để mang lại một giải pháp toàn diện từ tìm kiếm đến quản trị bất động sản. Em xin chân thành cảm ơn thầy cô và các bạn đã theo dõi!"* |

---

## 💡 MẸO QUAY VIDEO MƯỢT MÀ & ĐẠT ĐIỂM CAO

1. **Chuẩn bị sẵn 2 tab song song:**
   - Tab 1: Khách hàng ở `http://localhost:3000/chat`.
   - Tab 2: Sale ở `http://localhost:3000/sale` (đăng nhập sẵn).
2. **Kỹ thuật gõ phím:** Có thể copy sẵn câu lệnh (`tìm nhà dưới 5 tỷ ở miền bắc`, `chỉ lấy căn 2 phòng ngủ ở cầu giấy`, `đặt lịch căn CĂN HỘ Fodacon Bắc Hà – Mỗ Lao, Hà Đông ngày mai lúc 14h`) vào clipboard để paste cho nhanh và không bị gõ nhầm.
3. **Thao tác chuột:** Di chuyển chuột chậm rãi, dứt khoát, tránh lia chuột lung tung trên màn hình.
4. **Âm thanh:** Thu âm ở nơi yên tĩnh, giọng đọc tự tin, rõ ràng.
