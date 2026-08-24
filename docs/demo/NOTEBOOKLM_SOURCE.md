# Nera — Hồ sơ sản phẩm Demo Day Phase 1 (nguồn cho NotebookLM)

> Tài liệu này là nguồn duy nhất, tự chứa, dùng để sinh nội dung slide. Mọi số liệu và mô tả kỹ thuật trong đây đều đã được kiểm chứng trên bản deploy thật, không phải kế hoạch hay dự định.

---

## 1. Thông tin định danh

Sản phẩm tên là **Nera**. Đây là trợ lý AI giúp người dùng tìm nhà và đặt lịch xem nhà hoàn toàn bằng hội thoại tự nhiên, không cần điền form hay thao tác bộ lọc.

Đội thực hiện là **Team 046 LTD**, thuộc AI20K Build Phase Cohort 3, gồm bốn thành viên: Lê Tiến Đạt, Vũ Thế Lực, Phạm Trung Kiên, Nguyễn Thế Anh.

Sản phẩm đang chạy thật tại địa chỉ **nerahome.space**. Mã nguồn nằm tại kho GitHub **github.com/AI20K-Build-Phase-Cohort-3/P-046**.

Đề bài đội chọn là **B22 — Bất động sản, Kinh doanh O2O (Doanh nghiệp bất động sản X)**.

---

## 2. Bối cảnh và vấn đề

Trong ngành môi giới bất động sản hiện nay, việc hẹn khách đi xem nhà mẫu hoặc căn thực tế phải phối hợp đồng thời nhiều thứ: lịch rảnh của nhân viên sale, tình trạng căn hộ còn hay đã có người giữ, và phòng chờ tiếp khách. Toàn bộ việc điều phối này đang được làm thủ công qua tin nhắn chat. Hệ quả là trùng lịch giữa các sale, và bỏ lỡ khách hàng vì phản hồi chậm.

Về phía người đi tìm nhà, có ba điểm đau rõ rệt. Thứ nhất, họ phải tự đọc và tự lọc qua hàng loạt tin đăng rời rạc trên nhiều sàn khác nhau. Thứ hai, mỗi lần quay lại tìm kiếm họ lại phải nhập lại toàn bộ tiêu chí từ đầu, vì hệ thống không nhớ gì về họ. Thứ ba, khi đã ưng một căn, không có kênh nào để đặt lịch xem nhanh gọn — họ phải gọi điện hoặc nhắn tin thủ công rồi chờ đợi.

Vấn đề cốt lõi cần giải quyết là: cần một AI Agent hiểu được yêu cầu của khách bằng ngôn ngữ tự nhiên, biết dùng công cụ để kiểm tra lịch trống của sale và trạng thái căn hộ, đề xuất khung giờ phù hợp, đặt lịch và giữ căn tạm thời.

---

## 3. Giải pháp Nera cung cấp

Nera thay thế toàn bộ trải nghiệm form và bộ lọc bằng một cuộc trò chuyện duy nhất.

Người dùng chỉ cần mô tả nhu cầu bằng lời nói tự nhiên, ví dụ "tôi tìm căn hai phòng ngủ ở Cầu Giấy, tầm ba tỷ". Nera hiểu và trả về những căn có thật trong cơ sở dữ liệu, kèm lý do vì sao căn đó phù hợp.

Nera giữ được ngữ cảnh xuyên suốt cuộc trò chuyện. Khi người dùng hỏi tiếp "còn căn nào rẻ hơn không", họ không cần nhắc lại là đang tìm ở Cầu Giấy hay đang tìm hai phòng ngủ — Nera vẫn nhớ. Đây là điểm khác biệt so với các công cụ tìm kiếm theo bộ lọc thông thường.

Khi người dùng đã chọn được căn ưng ý, việc đặt lịch xem nhà diễn ra ngay bên trong cuộc hội thoại. Nera đọc lịch làm việc thật của các nhân viên sale trong hệ thống, đưa ra những khung giờ thực sự còn trống, và tạo yêu cầu đặt lịch gắn với một nhân viên sale có thật.

---

## 4. Kiến trúc kỹ thuật

Giao diện người dùng được xây bằng **Next.js**, triển khai trên nền tảng **Vercel**.

Phần xử lý phía sau dùng **FastAPI** viết bằng Python, triển khai trên **Render**.

Điều phối hội thoại dùng kiến trúc **multi-agent trên LangGraph**. Mô hình ngôn ngữ sử dụng là **GPT-4o-mini**, được gọi thật qua API, không phải phản hồi dựng sẵn.

Dữ liệu lưu trong **PostgreSQL**. Hệ thống có dùng **Redis** cho phần trạng thái tạm, kèm cơ chế dự phòng bằng bộ nhớ trong khi Redis không sẵn sàng, để hệ thống không sập vì một thành phần phụ.

Dữ liệu bất động sản trong hệ thống là dữ liệu **crawl thật** từ hai sàn giao dịch lớn của Việt Nam là **batdongsan.com.vn** và **chotot.com**, không phải dữ liệu giả sinh ngẫu nhiên.

Hệ thống phân bốn vai trò người dùng riêng biệt, mỗi vai trò có giao diện riêng: **Khách hàng**, **Sale**, **Điều phối viên**, và **Admin**.

Phiên đăng nhập dùng cookie HttpOnly. Mọi API thuộc quyền Sale và Admin, cũng như lịch sử hội thoại của từng khách, đều được kiểm tra vai trò và quyền sở hữu ở phía backend — không dựa vào việc ẩn nút trên giao diện.

---

## 5. Cơ chế đặt lịch và chống trùng

Mỗi ngày hệ thống mở bốn khung giờ xem nhà cố định, mỗi khung kéo dài một tiếng. Khi khách chọn một khung giờ, hệ thống kiểm tra chéo với lịch hiện có của từng nhân viên sale để loại bỏ những người đã bận, và chỉ đề xuất khung giờ thực sự trống.

Sau khi khách gửi yêu cầu, hệ thống **giữ chỗ tạm thời trong mười lăm phút**. Trong khoảng thời gian này, nhân viên sale đăng nhập vào giao diện riêng của mình để **xác nhận hoặc từ chối** yêu cầu.

Đây là điểm quan trọng về mặt thiết kế sản phẩm: Nera **không tự chốt lịch thay con người**. Cơ chế này gọi là Human-in-the-loop, tức là luôn có một nhân viên sale thật đứng ra xác nhận trước khi lịch hẹn được chốt chính thức. Chỉ khi nhân viên sale bấm nhận, hệ thống mới tạo lịch hẹn chính thức và gửi mã đặt lịch cho khách. Điều này vừa tránh việc AI đặt nhầm lịch cho người thật, vừa đảm bảo trách nhiệm cuối cùng thuộc về con người.

---

## 6. Nguyên tắc trung thực của hệ thống

Đây là phần đội đặc biệt chú trọng và là điểm nên nhấn mạnh khi trình bày.

Mỗi câu trả lời mà Nera đưa ra đều kèm theo một nhãn trạng thái công khai, cho biết câu trả lời đó được tạo ra bằng cách nào. Có bốn trạng thái: **llm_grounded** nghĩa là mô hình trả lời dựa trên dữ liệu đã xác minh trong cơ sở dữ liệu; **llm_direct** nghĩa là mô hình trả lời trực tiếp; **llm_intent** nghĩa là mô hình đang trích xuất ý định của người dùng; và **fallback** nghĩa là mô hình gặp lỗi và hệ thống đang trả lời theo luật cứng.

Khi nhà cung cấp mô hình gặp sự cố, giao diện hiển thị rõ dòng chữ "Fallback theo luật" thay vì giả vờ như đó là phản hồi của AI. Người dùng luôn biết mình đang nói chuyện với cái gì.

Phần tư vấn mà Nera viết ra được xây trên dữ liệu PostgreSQL đã xác minh, không phải do mô hình tự nghĩ ra. Backend giữ độc quyền quyết định về phân quyền và đặt lịch — mô hình ngôn ngữ không được phép tự ý thực hiện những hành động này.

Khi thiếu thông tin, hoặc khi người dùng hỏi câu nằm ngoài phạm vi hiểu biết của hệ thống, Nera từ chối trả lời thay vì đoán bừa.

---

## 7. Bằng chứng đã kiểm chứng

Toàn bộ các luồng nghiệp vụ mô tả ở trên đã được **test trực tiếp trên bản deploy thật** tại nerahome.space, không phải chỉ chạy trên máy cá nhân của lập trình viên.

Có log xác nhận hệ thống gọi mô hình ngôn ngữ thật trong quá trình test.

Đội đã chạy thử trọn vẹn luồng: tìm nhà bằng câu nói tự nhiên, hỏi tiếp mà không nhắc lại tiêu chí cũ, chọn căn, xem khung giờ trống thật, và tạo yêu cầu đặt lịch thành công gắn với nhân viên sale có thật trong hệ thống.

Đây là điểm khác biệt so với sản phẩm chỉ dừng ở mức mockup: ban giám khảo có thể mở thẳng đường dẫn nerahome.space và tự kiểm chứng lại từng bước.

---

## 8. Giới hạn hiện tại (phần đội thừa nhận thẳng)

Hệ thống hiện chỉ hỗ trợ bốn khung giờ cố định mỗi ngày, và việc phát hiện trùng lịch dựa trên kiểm tra chồng lấn đơn giản theo từng nhân viên sale. Hệ thống **chưa** xử lý được các tình huống lịch động phức tạp, ví dụ khi một khách đến muộn kéo theo ảnh hưởng dây chuyền tới các lịch hẹn sau đó. Đây là hạn chế đã biết, không phải lỗi phát sinh.

Phần ước tính tài chính, ví dụ tính khoản vay hay trả góp, hiện do mô hình ngôn ngữ tự tính bằng khả năng suy luận của nó, chưa có công cụ tính toán chuyên dụng đứng sau kiểm chứng. Vì vậy con số đưa ra mang tính tham khảo, chưa nên dùng cho quyết định tài chính thật.

Tính năng cho khách tự chọn nhân viên sale, và tính năng tích hợp bản đồ để tính khoảng cách thật tới trường học, bệnh viện, hiện chưa được xây dựng.

---

## 9. Hướng phát triển tiếp theo

Ưu tiên gần nhất là tích hợp bản đồ để trả lời được những câu hỏi về vị trí thực tế, ví dụ khoảng cách từ căn hộ tới trường học hoặc bệnh viện gần nhất.

Tiếp theo là xây dựng công cụ cố vấn tài chính có kiểm chứng, tính toán khoản vay và lịch trả góp dựa trên thu nhập thực tế của khách hàng, thay vì để mô hình tự ước lượng.

Xa hơn là tối ưu lộ trình cho nhân viên sale dẫn nhiều khách trong cùng một ngày, tự động dời lịch khi phát hiện xung đột, và ghi nhớ khung giờ ưa thích của từng khách hàng qua nhiều lần đặt lịch.

---

## 10. Thông điệp chính cần truyền tải

Nếu chỉ giữ lại một câu, thông điệp là: **Nera không bắt người dùng học cách dùng bộ lọc — Nera học cách hiểu người dùng.**

Ba luận điểm chống đỡ cho thông điệp đó, xếp theo thứ tự quan trọng:

Thứ nhất, sản phẩm chạy thật với dữ liệu thật, có thể kiểm chứng công khai qua đường dẫn, không phải bản demo dựng sẵn.

Thứ hai, hệ thống trung thực về giới hạn của chính nó — công khai nhãn trạng thái mỗi câu trả lời, và từ chối thay vì bịa khi không đủ dữ liệu.

Thứ ba, con người vẫn giữ quyền quyết định cuối cùng thông qua bước nhân viên sale xác nhận, thay vì để AI tự chốt lịch với khách hàng thật.
