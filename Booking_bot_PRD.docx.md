# **SOFTWARE DESIGN SPECIFICATION (SDS)**

## ---

**Hệ Thống BookingBot AI Agent – Trợ Lý Đặt Lịch Xem Nhà & Giữ Căn Tự Động**

**Phiên bản:** 2.0 | **Trạng thái:** Approved | **Kiến trúc:** Microservices & Multi-Agent Event-Driven

## **1\. Phân Tích Bài Toán (Problem Analysis)**

### **1.1 Business Problem**

Các công ty môi giới bất động sản đang gặp khó khăn trong việc vận hành lịch hẹn thủ công. Việc điều phối giữa **Khách hàng**, **Nhân viên kinh doanh (Sale)**, và **Quỹ căn (Inventory)** thường xuyên xảy ra tình trạng:

* Xung đột lịch hẹn (*Double-booking*).  
* Phản hồi khách hàng chậm trễ làm giảm tỷ lệ chuyển đổi.  
* Phân công Sale không tối ưu lộ trình di chuyển dẫn đến trễ giờ (*Running late*) và bỏ lỡ cơ hội bán hàng.

### **1.2 Pain Points**

* **Khách hàng:** Chờ đợi xác nhận lịch xem nhà quá lâu; trải nghiệm rời rạc.  
* **Sale:** Quá tải lịch trình, di chuyển kém hiệu quả giữa các khu vực, dễ trễ hẹn.  
* **Quản lý:** Mất kiểm soát quỹ căn do giữ chỗ thủ công không nhả đúng hạn; không theo dõi được hiệu suất thực tế của Sale.

### **1.3 Stakeholders**

* **Customer (Khách hàng):** Người tìm kiếm, đặt lịch và xem bất động sản.  
* **Sale Agent / Realtor (Nhân viên Sale):** Người tiếp nhận thông báo và trực tiếp dẫn khách xem nhà.  
* **Manager / Admin:** Giám sát vận hành, can thiệp vào các trường hợp ngoại lệ (**HITL**).  
* **BookingBot Systems:** AI Agent Orchestrator tự động hóa toàn bộ luồng nghiệp vụ.

### **1.4 Functional Requirements (FR)**

* **FR-01:** Tìm kiếm và đề xuất bất động sản thông minh theo tiêu chí nhu cầu.  
* **FR-02:** Tích hợp bản đồ (Google Maps) cung cấp vị trí và lộ trình tương tác.  
* **FR-03:** Giữ căn tự động (*Auto Hold*) với cơ sở dữ liệu thời gian thực (Buffer Time / Lock).  
* **FR-04:** Tính toán thời gian xem nhà dự kiến (*Estimated End Time*).  
* **FR-05:** Phân công Sale thông minh dựa trên Điểm số (*Assignment Score*) và Tối ưu lộ trình (*TSP \- Traveling Salesperson Problem*).  
* **FR-06:** Đồng bộ lịch 2 chiều với Google Calendar.  
* **FR-07:** Gửi thông báo/nhắc nhở tự động đa kênh (Email, SMS, Push Notification).  
* **FR-08:** Cơ chế can thiệp con người **Human-in-the-loop (HITL)**.

### **1.5 Non-Functional Requirements (NFR)**

* **Scalability:** Kiến trúc Microservices & Event-Driven, scale độc lập các module (đặc biệt là AI Orchestrator).  
* **Reliability & Data Integrity:** Đảm bảo tính ACID cho các giao dịch giữ căn và đặt lịch; tuyệt đối tránh double-booking.  
* **Performance:** Độ trễ phản hồi hội thoại AI \< 2.0s. Hệ thống chịu tải cao qua Message Broker.  
* **Maintainability:** Thiết kế module hóa cho các Tools và AI Agents.

### **1.6 Business Constraints & Rules**

* **Rule 01:** SQL Database là **Single Source of Truth (SSOT)**, không phải Google Calendar.  
* **Rule 02:** AI không được phép gọi trực tiếp Google Calendar API để thao tác dữ liệu, bắt buộc thông qua Calendar Sync Service.  
* **Rule 03:** Một căn hộ chỉ được khóa (*Hold*) cho 1 giao dịch booking tại 1 thời điểm trong khoảng time buffer an toàn.

## **2\. Thiết Kế Kiến Trúc Tổng Thể (System Architecture)**

Hệ thống thiết kế theo mô hình **Layered Architecture** kết hợp **Event-Driven Architecture**:

\+-----------------------------------------------------------------------+  
|                             CLIENT LAYER                              |  
|                   \[Web / Mobile App\]   \[Chat Interface\]               |  
\+-----------------------------------+-----------------------------------+  
                                    |  
                                    v  
\+-----------------------------------------------------------------------+  
|                         API & GATEWAY LAYER                           |  
|                        \[API Gateway / FastAPI\]                         |  
\+-----------------------------------+-----------------------------------+  
                                    |  
                                    v  
\+-----------------------------------------------------------------------+  
|                       AI & ORCHESTRATOR LAYER                         |  
|   \[LangGraph Orchestrator\] \<---\> \[Multi-Agent System\] \<---\> \[Redis\]  |  
\+-----------------------------------+-----------------------------------+  
                                    |  
                                    v  
\+-----------------------------------------------------------------------+  
|                          CORE SERVICE LAYER                           |  
| \[Booking Service\] \[Inventory Service\] \[Assignment Engine\] ...         |  
\+-----------------------------------+-----------------------------------+  
                                    |  
                                    v  
\+-----------------------------------------------------------------------+  
|                     INFRASTRUCTURE & DATA LAYER                        |  
|             \[PostgreSQL (SSOT)\]     \[Redis Queue / PubSub\]            |  
\+-----------------------------------------------------------------------+

### **Trách Nhiệm Từng Tầng:**

* **Client Layer:** Cung cấp giao diện tương tác cho Customer, Sale App và Admin Dashboard.  
* **API Layer (FastAPI):** Tiếp nhận Requests, Authentication/Authorization, Rate Limiting.  
* **AI Orchestrator (LangGraph):** Điều phối luồng giao tiếp giữa các Agents, duy trì State cuộc hội thoại.  
* **Agent Layer:** Các AI Sub-Agents xử lý ngôn ngữ tự nhiên và ra quyết định chuyên biệt.  
* **Core Service Layer:** Chứa Core Business Logic độc lập với AI.  
* **Infrastructure & Data Layer:** SQL Database (PostgreSQL \- SSOT) và Redis (Caching, Memory, Event Queue).

## **3\. Thiết Kế Multi-Agent Architecture**

Hệ thống sử dụng mô hình **Supervisor-Workers**:

* **Conversation Agent (Supervisor):** Điều phối trung tâm, tiếp nhận yêu cầu từ người dùng và phân công tác vụ cho các Worker Agents.  
* **Inventory Agent:** Quản lý quỹ căn, tìm kiếm bất động sản theo yêu cầu và kiểm tra trạng thái khóa căn. (Tools: *SearchPropertyTool, CheckAvailabilityTool, HoldPropertyTool*)  
* **Booking & Scheduling Agent:** Tính toán thời gian khả dụng, tính toán thời lượng xem nhà (Estimated End) và tạo booking. (Tools: *CalculateEstimatedEndTool, CreateBookingTool*)  
* **Sale Assignment Agent:** Lựa chọn Sale tối ưu dựa trên điểm số và lộ trình di chuyển. (Tools: *CalculateAssignmentScoreTool, AssignSaleTool*)  
* **HITL (Human-in-the-Loop) Agent:** Kích hoạt tạm dừng luồng AI tự động khi gặp sự cố/ngoại lệ để chờ Admin/Manager phê duyệt.

## **4\. Thiết Kế Scheduling Engine**

### **4.1 Công Thức Tính Estimated End & Buffer Time**

Để tránh Sale bị quá tải và trễ hẹn (*Running late*), thời gian xem nhà dự kiến được tính toán động:

Estimated End \= Start Time \+ Base Viewing Time \+ Buffer Time \+ Travel Time

Trong đó:

* **Base Viewing Time:** Phụ thuộc vào loại hình BĐS (ví dụ: Căn hộ 3PN \= 45 phút).  
* **Travel Time:** Thời gian di chuyển từ vị trí lịch liền trước đến địa điểm mới (lấy từ Google Maps API).  
* **Buffer Time:** Thời gian dự phòng đệm (gửi xe, thủ tục sảnh, mật độ giao thông).

### **4.2 Tiêu Chí Xác Định Sale Availability**

Một Sale được coi là "Rảnh" cho khung giờ \[Start Time, Estimated End\] khi thỏa mãn:

1. Không có booking nào ở trạng thái CONFIRMED hoặc IN\_PROGRESS đè lên khoảng thời gian này.  
2. Estimated End (Lịch trước) \+ Travel Time \<= Start Time (Lịch mới).  
3. Trạng thái Sale \= ACTIVE và không bị gắn flag RUNNING\_LATE.

## **5\. Thiết Kế Sale Assignment Engine**

Phân công Sale sử dụng bài toán tối ưu lộ trình (**TSP \- Traveling Salesperson Problem**) kết hợp **Công thức tính điểm đa tiêu chí (Assignment Score)**:

Assignment Score \= 0.30\*S\_route \+ 0.20\*S\_workload \+ 0.20\*S\_performance \+ 0.15\*S\_response \+ 0.15\*S\_rating

| Tiêu chí | Trọng số | Mô tả   |
| :---- | :---- | :---- |
| **Route Efficiency (S\_route)** | 30% | Mức độ tối ưu khi chèn lịch mới vào lộ trình di chuyển trong ngày của Sale. |
| **Workload (S\_workload)** | 20% | Ưu tiên Sale có ít booking hơn trong ngày để cân bằng tải. |
| **Performance (S\_performance)** | 20% | Tỷ lệ chốt sale / chốt lịch thành công trong tháng. |
| **Response Time (S\_response)** | 15% | Tốc độ phản hồi nhận lịch trung bình trên App. |
| **Customer Rating (S\_rating)** | 15% | Đánh giá trung bình từ khách hàng. |

## **6\. Google Calendar Integration & Notification Service**

### **6.1 Google Calendar Integration Pattern**

* AI tuyệt đối không gọi trực tiếp Google Calendar API.  
* Dữ liệu được cập nhật thành công vào **PostgreSQL (SSOT)** $\\rightarrow$ Hệ thống phát Event BookingConfirmed tới Redis Queue $\\rightarrow$ **Calendar Sync Service** lắng nghe và đồng bộ lên Google Calendar.

### **6.2 Notification Milestones**

* **T \- 48h:** Email xác nhận & lịch trình tổng quan.  
* **T \- 24h:** SMS/Zalo nhắc nhở kèm nút xác nhận tham dự.  
* **T \- 2h:** Push Notification tới App của Sale chuẩn bị di chuyển.  
* **T \- 30m:** SMS cho Khách hàng chứa Link Google Maps và thông tin Sale đón.

## **7\. AI Memory Architecture**

* **Short-term Memory (Redis):** Lưu trữ Session Chat History, State hội thoại trong thời gian thực. Tự động xóa sau 60 phút không tương tác.  
* **Long-term Memory (PostgreSQL \+ Vector DB):** Lưu trữ tóm tắt nhu cầu, lịch sử tương tác và mã hóa **Customer Preference Vector** (khoảng giá, hướng nhà, khung giờ ưu tiên).

## **8\. Tool Design (Function Calling)**

| Tool Name | Input Parameters | Output | Điều Kiện Gọi | Fallback / Handling   |
| :---- | :---- | :---- | :---- | :---- |
| SearchPropertyTool | district, min\_price, max\_price, type | List\[Property\] | Khách tìm kiếm nhà | Return empty list & suggest adjust criteria |
| SearchAmenityTool | property\_id, radius, amenity\_type | List\[Amenity\] | Khách hỏi tiện ích xung quanh | Return cached static data |
| GenerateMapLinkTool | property\_id, customer\_id | map\_url, static\_image | Khách yêu cầu xem vị trí/đường đi | Return text address |
| HoldPropertyTool | property\_id, customer\_id | hold\_id, hold\_until | Khách chốt muốn giữ căn | Suggest alternative properties |
| AssignSaleTool | booking\_id | sale\_id, assignment\_score | Tạo Booking thành công | Trigger HITL workflow |
| CheckRunningLateTool | sale\_id | is\_late, delay\_minutes | Quét định kỳ / Trước khi assign | Default is\_late \= False |

## **9\. System Evaluation Metrics**

* **Booking Success Rate:** Tỷ lệ chuyển đổi từ phiên chat có nhu cầu sang Booking hoàn tất.  
* **No-Show Rate:** Tỷ lệ khách hủy phút chót hoặc không xuất hiện (dùng để phân loại Watchlist).  
* **Late Arrival Rate:** Độ chênh lệch giữa thời gian thực tế và dự kiến, dùng làm Feedback Loop để điều chỉnh Buffer Time cho từng Sale.