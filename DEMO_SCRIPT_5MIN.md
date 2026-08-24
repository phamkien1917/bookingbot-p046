# 🎬 KỊCH BẢN THUYẾT TRÌNH VIDEO DEMO (5 PHÚT)
## DỰ ÁN: NERA (P-046) – HỆ THỐNG TRỢ LÝ BẤT ĐỘNG SẢN AI ĐA TÁC NHÂN

* **Người thuyết trình:** Cá nhân tự trình bày
* **Thời lượng mục tiêu:** ~ 5 phút (05:00)
* **Phong cách:** Gãy gọn, chuyên nghiệp, tập trung vào tính năng kỹ thuật và luồng nghiệp vụ thực tế (không dùng từ ngữ hoa mỹ/sến súa).
* **Môi trường demo:** `https://www.nerahome.space` (hoặc `http://localhost:3000`)

---

## 🛠️ CÔNG TÁC CHUẨN BỊ TRƯỚC KHI BẤM QUAY (1 PHÚT)

Mở sẵn 3 cửa sổ trên màn hình để chuyển đổi bằng phím tắt `Alt + Tab`:
1. **Cửa sổ 1 (Trình duyệt Chrome thường):** Mở Trang chủ `https://www.nerahome.space` (Giao diện Khách hàng).
2. **Cửa sổ 2 (Cửa sổ Ẩn danh `Ctrl + Shift + N`):** Mở `https://www.nerahome.space/sale` (Đã đăng nhập sẵn tài khoản Sale, ví dụ: `hanh.bt.sale0@xhome.com`).
3. **Cửa sổ 3 (Trình duyệt Edge/Brave):** Mở `https://www.nerahome.space/admin` (Đã đăng nhập sẵn tài khoản Admin).

*💡 Công cụ quay đề xuất: Dùng **Snipping Tool (`Win + Shift + S` chọn biểu tượng Máy quay)** để quay toàn màn hình.*

---

## ⏱️ CHI TIẾT TỪNG PHÂN ĐOẠN (TIMELINE & LỜI THUYẾT MINH)

---

### 📍 PHẦN 1: MỞ ĐẦU & TỔNG QUAN HỆ THỐNG (0:00 – 0:40)

* 🖥️ **Thao tác trên màn hình:**
  - Quay Trang chủ `https://www.nerahome.space`.
  - Cuộn nhẹ trang từ trên xuống: lướt qua Hero section, các dự án/căn hộ nổi bật, sau đó di chuột lên Header bấm vào nút **"Nói với Nera"** (hoặc truy cập `/chat`).
* 🎙️ **Lời thuyết minh:**
  > "Xin chào thầy cô và các bạn. Hôm nay em xin demo sản phẩm **Nera – Trợ lý bất động sản AI thông minh** thuộc dự án P-046.
  > 
  > Dự án được xây dựng nhằm giải quyết hai vấn đề lớn trên thị trường: Một là người mua mất quá nhiều thời gian lọc hàng ngàn tin đăng không phù hợp; Hai là khâu kết nối lịch hẹn giữa người mua và môi giới thường bị chậm trễ và rời rạc.
  > 
  > Để giải quyết bài toán này, Nera áp dụng kiến trúc **LangGraph Multi-Agent** gồm 3 tác nhân chính: **Supervisor Agent** điều phối intent, **Inventory Agent** phụ trách truy vấn dữ liệu bất động sản, và **Booking Agent** xử lý nghiệp vụ đặt lịch xem nhà theo thời gian thực."

---

### 📍 PHẦN 2: TÌM KIẾM TỰ NHIÊN & DUY TRÌ NGỮ CẢNH ĐA LƯỢT (0:40 – 1:40)

* 🖥️ **Thao tác trên màn hình:**
  1. Trong ô chat, gõ câu lệnh tìm kiếm diện rộng:
     `tìm nhà dưới 5 tỷ ở miền bắc`
     ➜ Nhấn Enter. Nera phản hồi danh sách các căn kèm thẻ thông tin (giá, diện tích, vị trí và lý do gợi ý).
  2. Gõ tiếp câu truy vấn thu hẹp ngữ cảnh (Multi-turn):
     `chỉ lấy căn 2 phòng ngủ ở cầu giấy`
     ➜ Nhấn Enter. Nera tự động giữ ngân sách $\le$ 5 tỷ và lọc tiếp theo Quận Cầu Giấy + 2PN.
* 🎙️ **Lời thuyết minh:**
  > "Đầu tiên là khả năng **Tìm kiếm bằng ngôn ngữ tự nhiên**. Em nhập câu lệnh: *'tìm nhà dưới 5 tỷ ở miền bắc'*. Inventory Agent sẽ bóc tách thực thể vùng miền, khoảng giá và truy vấn cơ sở dữ liệu PostgreSQL để trả về các bất động sản phù hợp, đi kèm lý do gợi ý cụ thể cho từng căn.
  > 
  > Tiếp theo, khi em nhập tiếp câu lệnh: *'chỉ lấy căn 2 phòng ngủ ở cầu giấy'*, hệ thống thể hiện khả năng **duy trì ngữ cảnh đa lượt (Multi-turn Context)**. Supervisor Agent tự động kế thừa mức ngân sách dưới 5 tỷ từ lượt chat trước và kết hợp với tiêu chí mới là Quận Cầu Giấy và 2 phòng ngủ, thay vì reset lại từ đầu như các chatbot thông thường."

---

### 📍 PHẦN 3: TRÍ NHỚ DÀI HẠN (SEMANTIC MEMORY) (1:40 – 2:30)

* 🖥️ **Thao tác trên màn hình:**
  1. Bấm vào mục **Trí nhớ (Memory)** trên thanh điều hướng (`/memory`) ➜ Cho người xem thấy bảng hồ sơ sở thích (Ngân sách, Khu vực quan tâm, Tiện ích mong muốn).
  2. Bấm về lại **Trang chủ (`/`)** ➜ Trỏ chuột vào Card chào mừng: *"Chào bạn quay lại – Lần trước bạn quan tâm: Quận Cầu Giấy..."*.
  3. Bấm vào nút **"Tiếp tục hành trình →"** ➜ Màn hình chuyển vào chat, Nera tự động nạp tiêu chí cũ và đưa ra danh sách căn hộ phù hợp ngay lập tức.
* 🎙️ **Lời thuyết minh:**
  > "Tính năng cốt lõi thứ hai của Nera là **Trí nhớ dài hạn (Semantic Memory)**. Thông qua quá trình trò chuyện, hệ thống tự động trích xuất và cập nhật hồ sơ sở thích của người dùng vào cơ sở dữ liệu.
  > 
  > Như thầy cô thấy trên trang Memory, hệ thống đã lưu lại các thông tin: tài chính dưới 5 tỷ, khu vực Cầu Giấy và căn 2 phòng ngủ.
  > 
  > Khi người dùng quay lại trang chủ sau nhiều ngày, hệ thống sẽ nhận diện và hiển thị card tiếp nối hành trình. Khi em bấm *'Tiếp tục hành trình'*, Nera lập tức khởi tạo phiên làm việc mới, nạp lại toàn bộ tiêu chí đã nhớ và đề xuất ngay các căn hộ mới nhất mà người dùng không cần nhập lại bất kỳ thông tin nào."

---

### 📍 PHẦN 4: ĐẶT LỊCH XEM NHÀ & DUYỆT THỜI GIAN THỰC PHÍA SALE (2:30 – 3:45)

* 🖥️ **Thao tác trên màn hình:**
  1. Trong ô chat, gõ câu lệnh đặt lịch:
     `đặt lịch căn CĂN HỘ Fodacon Bắc Hà – Mỗ Lao, Hà Đông ngày mai lúc 14h`
     ➜ Nhấn Enter. Nera nhận diện đúng căn hộ, kiểm tra slot trống và tạo Tour Request `TR-XXXXX` trạng thái Chờ duyệt.
  2. Bấm `Alt + Tab` chuyển sang **Cửa sổ 2 (Giao diện Sale: `/sale`)** ➜ Yêu cầu `TR-XXXXX` vừa tạo xuất hiện ngay trên danh sách Lịch hẹn mới.
  3. Bấm nút **"Xác nhận" (Approve)** trên giao diện Sale.
  4. Bấm `Alt + Tab` quay lại **Cửa sổ 1 (Khách hàng)** ➜ Trong chat và trang `/my-bookings`, trạng thái đổi thành Đã xác nhận (`CONFIRMED`) kèm mã Booking, tên Sale và SĐT liên hệ.
* 🎙️ **Lời thuyết minh:**
  > "Bây giờ em sẽ thực hiện quy trình **Đặt lịch xem nhà**. Trong khung chat, em nhắn: *'đặt lịch căn Fodacon Bắc Hà ngày mai lúc 14h'*.
  > 
  > Booking Agent sẽ định danh chính xác bất động sản, kiểm tra tính khả dụng của chuyên viên Sale phụ trách khu vực và khởi tạo một yêu cầu lịch hẹn ở trạng thái Chờ duyệt.
  > 
  > Ngay lập tức, em chuyển sang màn hình làm việc của Sale. Yêu cầu vừa tạo đã hiển thị theo thời gian thực. Sale kiểm tra thông tin và bấm nút *'Xác nhận'*.
  > 
  > Quay trở lại phía khách hàng, hệ thống lập tức đồng bộ trạng thái sang *Đã xác nhận*, cung cấp mã Booking chính thức cùng thông tin liên hệ của chuyên viên Sale phụ trách. Toàn bộ luồng dữ liệu từ AI đến nhân viên vận hành được kết nối khép kín."

---

### 📍 PHẦN 5: TỐI ƯU LỘ TRÌNH CHO SALE & TRANG QUẢN TRỊ ADMIN (3:45 – 4:35)

* 🖥️ **Thao tác trên màn hình:**
  1. Tại Cửa sổ 2 (Sale), bấm vào mục **"Lộ trình di chuyển"** (`/sale/route-map`) ➜ Màn hình hiển thị bản đồ các điểm hẹn trong ngày và đường đi tối ưu.
  2. Bấm `Alt + Tab` sang **Cửa sổ 3 (Admin Dashboard: `/admin`)** ➜ Lướt nhanh qua Quản lý kho Bất động sản (`/admin/properties`) và Quản lý đội ngũ Sale (`/admin/sales`).
* 🎙️ **Lời thuyết minh:**
  > "Để hỗ trợ đội ngũ kinh doanh làm việc hiệu quả, Nera tích hợp tính năng **Tối ưu lộ trình di chuyển (Route Map)**. Thuật toán sẽ tự động tính toán khoảng cách địa lý và sắp xếp thứ tự các điểm hẹn xem nhà trong ngày của Sale theo tuyến đường ngắn nhất, giúp tiết kiệm thời gian di chuyển.
  > 
  > Cuối cùng là **Trang quản trị Admin**. Tại đây, ban quản lý có thể giám sát toàn bộ danh mục bất động sản trên hệ thống, kiểm soát tình trạng tin đăng và phân bổ nhân sự phụ trách theo từng dự án hoặc khu vực địa lý."

---

### 📍 PHẦN 6: TỔNG KẾT (4:35 – 5:00)

* 🖥️ **Thao tác trên màn hình:**
  - Bấm `Alt + Tab` quay về Trang chủ `https://www.nerahome.space`, dừng lại ở giao diện tổng quan.
* 🎙️ **Lời thuyết minh:**
  > "Tổng kết lại, dự án Nera đã hoàn thiện toàn bộ các module từ: Trợ lý AI hội thoại đa tác nhân với LangGraph, Bộ nhớ dài hạn Semantic Memory, Hệ thống đặt lịch và đồng bộ thời gian thực cho Sale, đến Thuật toán tối ưu lộ trình.
  > 
  > Hệ thống được triển khai trên nền tảng FastAPI backend, Next.js 16 frontend và cơ sở dữ liệu PostgreSQL.
  > 
  > Em xin kết thúc phần trình bày demo tại đây. Cảm ơn thầy cô và các bạn đã lắng nghe."

---

## 📋 BẢNG TỔNG HỢP CÂU LỆNH MẪU (COPY ĐỂ DÁN KHI DEMO)

Để tránh bị gõ nhầm hoặc mất thời gian gõ phím khi quay, bạn có thể copy sẵn các câu lệnh này:

1. **Lệnh 1 (Tìm kiếm ban đầu):**
   ```text
   tìm nhà dưới 5 tỷ ở miền bắc
   ```
2. **Lệnh 2 (Lọc đa lượt):**
   ```text
   chỉ lấy căn 2 phòng ngủ ở cầu giấy
   ```
3. **Lệnh 3 (Đặt lịch xem nhà):**
   ```text
   đặt lịch căn CĂN HỘ Fodacon Bắc Hà – Mỗ Lao, Hà Đông ngày mai lúc 14h
   ```
