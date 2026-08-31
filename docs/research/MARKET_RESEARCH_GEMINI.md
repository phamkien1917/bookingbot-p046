# Nghiên cứu thị trường — Báo cáo Gemini Deep Research

**Mã tài liệu:** `docs/research/MARKET_RESEARCH_GEMINI.md`
**Nguồn:** Google Gemini Deep Research
**Ngày:** 08/2026
**Vai trò:** Nguồn khung (framework) cho bộ slide và các tài liệu phân tích khác. Số liệu Việt Nam đặc thù được kiểm chứng lại bằng khảo sát thực địa — xem [`FIELD_RESEARCH_SYNTHESIS.md`](FIELD_RESEARCH_SYNTHESIS.md).

> **Lưu ý:** Bản dán vào chat trước đó bị cắt ở ~50.000 ký tự. Nội dung dưới đây là phần
> nhận được; phần sau mục nguồn cần dán bổ sung tại chỗ đánh dấu.

---

## Nghiên Cứu Thị Trường: Phân Tích Bài Toán "Phễu Đứt Gãy Kép" Trong Giao Dịch Bất Động Sản Và Tiềm Năng Ứng Dụng Trợ Lý AI Nera

### Tóm Tắt Điều Hành

Thị trường giao dịch bất động sản trực tuyến đang đối mặt với một nghịch lý nghiêm trọng mang tính cấu trúc: sự phát triển của công nghệ tìm kiếm không tỷ lệ thuận với tốc độ và chất lượng kết nối ngoại tuyến (offline). Báo cáo phân tích chuyên sâu này được thực hiện nhằm bóc tách bài toán "phễu đứt gãy kép" – trạng thái nghẽn mạch cục bộ ở cả phía người tìm mua/thuê nhà và phía chuyên viên môi giới (Sales) – qua đó đánh giá tính khả thi và không gian thị trường của sản phẩm trợ lý trí tuệ nhân tạo (AI) theo mô hình O2O (Online-to-Offline) mang tên Nera. Mục tiêu tối thượng của Nera không phải là một công cụ trò chuyện (chatbot) cung cấp thông tin đơn thuần, mà là một cỗ máy chuyển đổi trực tiếp nhu cầu ngôn ngữ tự nhiên của khách hàng thành các lịch hẹn xem nhà thực tế, giải quyết triệt để vấn đề chồng chéo lịch hẹn (double-booking) đang nhức nhối trên thị trường.

Thông qua việc đối chiếu chéo các tập dữ liệu quy mô lớn từ Hiệp hội Chuyên gia Bất động sản Quốc gia Mỹ (NAR), Viện Công nghệ Massachusetts (MIT), Tạp chí Harvard Business Review (HBR), kết hợp cùng bối cảnh bản địa từ Hội Môi giới Bất động sản Việt Nam (VARS) và các đơn vị nghiên cứu thị trường (Savills, CBRE, Batdongsan.com.vn), bức tranh toàn cảnh về sự đứt gãy này đã được định lượng một cách sắc nét. Ở phía người tiêu dùng, mặc dù tỷ lệ sử dụng internet trong quá trình tìm nhà đã chạm ngưỡng tuyệt đối 100%, người mua vẫn bị vắt kiệt sức lực trong một hành trình kéo dài trung bình lên tới 10 tuần. Nguyên nhân cốt lõi xuất phát từ sự nghèo nàn của các nền tảng tìm kiếm hiện hành, nơi nhu cầu đa chiều của con người bị ép buộc phải chuyển ngữ thành các bộ lọc tĩnh cứng nhắc, dẫn đến hiện tượng quá tải nhận thức. Tồi tệ hơn, khi họ quyết định liên hệ để xem nhà, họ rơi vào một khoảng không chờ đợi vô tận.

Ở phía môi giới, điểm nghẽn mang tên "tốc độ phản hồi tiềm năng" (speed-to-lead) đang là lỗ hổng gây thất thoát doanh thu nghiêm trọng nhất. Các nghiên cứu học thuật kinh điển đã chứng minh rằng việc phản hồi khách hàng trong vòng 5 phút đầu tiên giúp tăng khả năng kết nối lên 100 lần và tỷ lệ chuyển đổi (qualify) lên 21 lần so với việc chờ đến phút thứ 30. Tuy nhiên, thời gian phản hồi trung bình của ngành bất động sản hiện đang neo ở mức 15 giờ, và hơn 63% khách hàng tiềm năng không bao giờ nhận được phản hồi. Sự chậm trễ này không hoàn toàn do sự lười biếng, mà là hệ quả của một quy trình vận hành thủ công, nơi môi giới phải dành tới 70% thời gian cho các công việc hành chính và điều phối lịch qua các ứng dụng nhắn tin cá nhân như Zalo. Tình trạng này sinh ra vấn nạn chồng chéo lịch hẹn, làm tổn hại trải nghiệm khách hàng trong một thị trường mà 80% người mua mang tâm lý "chỉ chọn làm việc với một môi giới duy nhất".

Đặc biệt, thị trường Việt Nam đang bước vào một cuộc đại thanh lọc mang tính bản lề nhờ chất xúc tác là Luật Kinh doanh Bất động sản 2024 (hiệu lực từ ngày 01/08/2024). Đạo luật này nghiêm cấm hành nghề môi giới tự do, buộc hàng trăm ngàn cá nhân phải quy tụ về các doanh nghiệp và sàn giao dịch có tổ chức. Sự thay đổi pháp lý này ép buộc các sàn giao dịch phải số hóa toàn diện quy trình quản lý khách hàng và phân bổ lịch hẹn để kiểm soát hiệu suất, tạo ra một thị trường mục tiêu (TAM) khổng lồ, cấp thiết, và có khả năng chi trả cao cho mô hình phần mềm dịch vụ (SaaS) định giá theo tài khoản (per-seat) như Nera.

### Phương Pháp Tiếp Cận Và Danh Sách Nguồn Khảo Cứu

Để đảm bảo tính toàn vẹn, khách quan và chiều sâu của các luận điểm phân tích, báo cáo này áp dụng phương pháp nghiên cứu định lượng kết hợp diễn dịch (deductive reasoning), dựa trên việc đối chiếu chéo (cross-reference) giữa xu hướng hành vi tâm lý toàn cầu và bối cảnh cấu trúc đặc thù của thị trường Việt Nam.

Khung phân tích được xây dựng trên ba trụ cột dữ liệu chính. Trụ cột thứ nhất bao gồm các nghiên cứu về hành vi người dùng và tốc độ chuyển đổi ở quy mô quốc tế. Nguồn dữ liệu cốt lõi được khai thác từ chuỗi Báo cáo Hồ sơ Người Mua và Bán Nhà (Profile of Home Buyers and Sellers) giai đoạn 2020-2025 của Hiệp hội Chuyên gia Bất động sản Quốc gia Mỹ (NAR). Bên cạnh đó, để định lượng thiệt hại của sự chậm trễ trong phản hồi, báo cáo sử dụng công trình nghiên cứu kinh điển về "Lead Response Management" của Tiến sĩ James Oldroyd thực hiện tại Viện Công nghệ Massachusetts (MIT) và được công bố rộng rãi trên Harvard Business Review (HBR), cùng các báo cáo cập nhật năm 2026 về thực trạng Proptech và thiết kế trải nghiệm người dùng (UX).

Trụ cột thứ hai tập trung vào khung pháp lý và thực trạng vận hành môi giới tại Việt Nam. Các văn bản quy phạm pháp luật, trọng tâm là Luật Kinh doanh Bất động sản 2023/2024 (số 29/2023/QH15) được phân tích chuyên sâu nhằm đánh giá tác động tái cấu trúc thị trường. Các số liệu thống kê ngành được tham chiếu từ Hội Môi giới Bất động sản Việt Nam (VARS), kết hợp với thực trạng quản lý hệ thống từ các nền tảng CRM nội địa đang hoạt động như MeeyCRM, CloudGO, và SlimCRM.

Trụ cột thứ ba là bối cảnh vĩ mô và tâm lý thị trường Việt Nam, được định hình qua Báo cáo Tâm lý Người Tiêu dùng (Consumer Sentiment Study) các năm 2024 - 2025 của Batdongsan.com.vn, cùng các báo cáo phân tích biến động nguồn cung, lượng giao dịch từ hai tổ chức tư vấn quốc tế hàng đầu là Savills và CBRE. Việc kết hợp ba trụ cột này cho phép nội suy ra những khoảng trống thị trường mà công nghệ AI đàm thoại của Nera có thể can thiệp và tạo ra dòng doanh thu bền vững.

### Phần A: Phía Người Tìm Nhà - Sự Kiệt Quệ Trong Hành Trình Số Hóa Nửa Vời

Hành trình tìm kiếm bất động sản của khách hàng đang bị mắc kẹt giữa hai thái cực đối lập: sự bùng nổ vô tận của thông tin trực tuyến và sự nghèo nàn tột độ trong khả năng cá nhân hóa trải nghiệm. Phân tích lớp dữ liệu từ phía người mua cho thấy hàng loạt các chỉ báo về sự đứt gãy nghiêm trọng trong quá trình chuyển đổi từ ý định (intent) sang hành động thực tế (action).

**Sự Chuyển Dịch Nhân Khẩu Học Và Áp Lực Của Thời Gian Tìm Kiếm Kéo Dài.** Một trong những phát hiện nhất quán và đáng báo động nhất từ các báo cáo thường niên của NAR là sự gia tăng và neo giữ ở mức cao của thời gian tìm kiếm nhà. Trong suốt giai đoạn từ năm 2022 đến 2025, thời gian trung bình (median) mà một người mua nhà phải bỏ ra để tìm kiếm đã tăng từ 8 tuần lên 10 tuần. Khoảng thời gian hai tháng rưỡi này không phải là một hành trình tận hưởng sự tự do lựa chọn, mà thực chất là một quá trình bào mòn tâm lý nghiêm trọng, sinh ra hội chứng mệt mỏi vì quyết định (decision fatigue). Hơn một nửa số người mua (56%) thừa nhận rằng việc tìm kiếm đúng căn nhà phù hợp là bước khó khăn và áp lực nhất trong toàn bộ quy trình.

Báo cáo năm 2025 của NAR chỉ ra một bước ngoặt lịch sử: tỷ lệ người mua nhà lần đầu đã giảm xuống mức thấp kỷ lục chỉ còn 21% (so với mức trung bình 40% trước cuộc đại suy thoái). Cùng với đó, độ tuổi trung bình của nhóm khách hàng lần đầu mua nhà đã bị đẩy lên mức cao nhất mọi thời đại là 40 tuổi. Nhóm người mua lặp lại (repeat buyers) hiện chiếm tới 79% thị trường, với độ tuổi trung bình lên tới 62 tuổi. Những khách hàng ở độ tuổi 40 đến trên 60 là những cá nhân đã đạt độ chín về sự nghiệp, có khả năng tài chính vững vàng (30% người mua lặp lại thanh toán hoàn toàn bằng tiền mặt, tỷ lệ trả trước trung bình lên tới 23%), nhưng quỹ thời gian của họ lại cực kỳ eo hẹp.

Hành vi khởi đầu của người mua đã chuyển dịch hoàn toàn sang không gian số. Dữ liệu chỉ ra rằng từ 41% đến 47% người mua nhà chọn việc tìm kiếm trên mạng internet làm bước đi đầu tiên. Tỷ lệ sử dụng internet tại bất kỳ điểm nào trong hành trình tìm kiếm đã đạt mức tuyệt đối 100% vào năm 2024 và 2025, với 70% người dùng thực hiện qua các thiết bị di động. Hơn một nửa (52%) số người mua khẳng định họ tìm thấy chính căn nhà mình sẽ mua thông qua internet. Tuy nhiên, dù 100% người mua dùng internet, có đến 88% người mua cuối cùng vẫn phải hoàn tất giao dịch thông qua một chuyên viên môi giới.

**Sự Bất Lực Của Bộ Lọc Cứng Và Kỷ Nguyên NLP.** Hầu hết các nền tảng tìm kiếm bất động sản lớn, từ Zillow đến Batdongsan.com.vn hay Chợ Tốt, đều vận hành dựa trên kiến trúc cũ: ép buộc người dùng sử dụng các bộ lọc cứng (Rigid Filters). Kiến trúc tìm kiếm dựa trên từ khóa mang những khiếm khuyết chí mạng về mặt ngữ nghĩa: sự vắng mặt của bối cảnh, hạn chế trong việc hiểu ý định thực sự, không có khả năng xử lý các truy vấn dài, và bất lực trước những từ khóa mơ hồ. Một khách hàng có nhu cầu "căn hộ yên tĩnh, phù hợp cho gia đình có con nhỏ, cách chỗ làm ở quận 1 khoảng 30 phút đi xe máy, không ngập nước, giá dưới 5 tỷ" sẽ không thể tìm thấy bất kỳ ô đánh dấu nào tương ứng. Nghiên cứu về xu hướng Proptech năm 2026 chỉ ra rằng việc trình bày một bảng điều khiển gồm 15 đến 20 bộ lọc tạo ra một rào cản ma sát khổng lồ, khiến tỷ lệ rời bỏ trang tăng vọt.

**Hiệu Ứng "Người Thắng Lấy Tất Cả" Trong Việc Lựa Chọn Môi Giới.** Theo dữ liệu khảo sát từ NAR và các đơn vị nghiên cứu độc lập, có tới 80% người mua nhà chỉ phỏng vấn hoặc làm việc với đúng MỘT môi giới duy nhất trước khi đưa ra quyết định. Ở các khảo sát với biên độ khác, con số này luôn dao động ở mức 65% đến 74% người dùng chỉ phỏng vấn một môi giới. Dữ liệu từ Salesforce củng cố khi báo cáo rằng 78% khách hàng sẽ chốt mua hàng từ doanh nghiệp có khả năng phản hồi họ đầu tiên.

**Quyền Lực Của "Quy Tắc 5 Phút".** Nghiên cứu Lead Response Management do Tiến sĩ James Oldroyd thực hiện tại MIT cùng InsideSales.com vào năm 2007, phân tích hơn 100.000 điểm dữ liệu cuộc gọi: nếu phản hồi khách hàng trong vòng 5 phút đầu tiên so với việc chờ đến phút thứ 30, tỷ lệ kết nối thành công cao gấp 100 lần, cơ hội qualify cao gấp 21 lần. Sau mốc 5 phút đầu tiên, chất lượng của lead sụt giảm theo phương thẳng đứng, bốc hơi tới 80% giá trị. Nghiên cứu ban đầu của HBR phơi bày thời gian phản hồi trung bình (median) của các doanh nghiệp được khảo sát lên tới 42 giờ; dữ liệu cập nhật 2026 cho thấy 63.5% lead không bao giờ nhận được bất kỳ phản hồi nào. Riêng ngành dịch vụ bất động sản, thời gian phản hồi trung bình đang neo ở mức 15 giờ.

### Phần B: Phía Môi Giới Và Sự Tái Cấu Trúc Thị Trường Việt Nam

**Sự Lãng Phí Năng Lực.** Các nhân viên phát triển kinh doanh và môi giới (SDRs/Brokers) chỉ dành khoảng 30% thời lượng ngày làm việc cho các hoạt động bán hàng sinh lời trực tiếp. 70% còn lại bị thiêu vào các công việc hành chính: cập nhật CRM thủ công, nghiên cứu thông tin dự án, đăng tin, sàng lọc khách ảo, và tổ chức sắp xếp lịch hẹn.

**Hệ Sinh Thái Công Cụ Phân Mảnh Và Thảm Họa Trùng Lịch.** Dựa trên phân tích từ MeeyCRM, CloudGO, SlimCRM: phần lớn môi giới vẫn quản lý vòng đời khách hàng qua sổ tay, ứng dụng ghi chú, Google Sheets/Excel độc lập, và phổ biến nhất là các đoạn chat cá nhân hoặc nhóm trên Zalo, Messenger. Điểm yếu: thất thoát dữ liệu (thông tin giỏ hàng, sở thích khách trôi mất giữa hàng ngàn tin nhắn); chậm đồng bộ trạng thái (quá trình "chia bài" thủ công qua nhiều tầng làm mất "thời điểm vàng 5 phút"); và xung đột trùng lịch hẹn (do không có nguồn sự thật duy nhất theo thời gian thực, hai môi giới có thể cùng xếp lịch đưa hai khách đến xem cùng một căn cùng một khung giờ).

**Cú Hích Pháp Lý: Luật Kinh Doanh Bất Động Sản 2024.** VARS chỉ ra toàn thị trường hiện có khoảng 300.000 người hoạt động dưới danh nghĩa môi giới; chỉ khoảng 30.000 đến 40.000 người (10% đến 13%) có chứng chỉ hành nghề hợp pháp. Luật Kinh doanh Bất động sản mới số 29/2023/QH15 (hiệu lực 01/08/2024): Khoản 2 Điều 61 quy định cá nhân môi giới không được phép hành nghề tự do, bắt buộc phải làm việc trong một doanh nghiệp có đăng ký pháp nhân; Điều 63 quy định cá nhân môi giới không được trực tiếp nhận thù lao từ khách hàng. Đạo luật là một cuộc "gom quân" quy mô lớn: sàn giao dịch trở thành chủ thể nắm quyền lực tuyệt đối, buộc phải đầu tư vào hệ thống quản trị trung tâm để thu hồi quyền kiểm soát dữ liệu khách hàng. Thị trường mua phần mềm chuyển từ B2C nhỏ giọt sang B2B theo tài khoản (per-seat).

### Phần C: Bối Cảnh Thị Trường Và Mức Độ Sẵn Sàng Tại Việt Nam

**Tâm lý khát khao tích lũy bất động sản.** Báo cáo Tâm lý Người Tiêu dùng của Batdongsan.com.vn 2024: trong số 1.000 người khảo sát, 65% có ý định và kế hoạch cụ thể mua bất động sản trong vòng 12 tháng tới. Khát khao mạnh nhất ở giới trẻ và gia đình trẻ trung lưu đang tích lũy tài sản.

**Quy mô thị trường.** Theo Savills, quý II/2025 riêng Hà Nội ghi nhận 8.000 căn hộ mở bán mới; tổng 6 tháng đầu năm khoảng 14.900 căn (tăng 121% so với cùng kỳ). Giá bán sơ cấp trung bình Hà Nội 91 triệu đồng/m2. Theo CBRE, thanh khoản sơ cấp quý I/2025 tại Hà Nội đạt 7.914 căn; dự báo cả năm 2025 nguồn cung mở bán mới của Hà Nội đạt khoảng 31.000 căn; toàn quốc kỳ vọng khoảng 579.718 giao dịch. Với giá chung cư Hà Nội trung bình 4-5 tỷ đồng/căn, hoa hồng cho môi giới và sàn từ 80 đến 150 triệu đồng (2%-3%).

### Đối Chiếu Hành Vi: Điểm Tương Đồng Toàn Cầu Và Đặc Thù Bản Địa

**Suy rộng được:** tâm lý không khoan nhượng với sự chờ đợi (đường cong Intent Decay phổ quát, quy tắc 100x/21x của MIT giữ nguyên giá trị); xu hướng thiên vị người phản hồi đầu tiên (First-responder Bias, 80% người mua chỉ làm việc với 1 môi giới); nhu cầu diễn đạt bằng ngôn ngữ tự nhiên.

**Không áp đặt được:** mức độ minh bạch dữ liệu (Mỹ có hệ thống MLS trung tâm, Việt Nam chưa có, vấn nạn tin ảo/nhà treo giá thấp phổ biến); thói quen công cụ liên lạc (phương Tây dùng email/SMS, Việt Nam phụ thuộc gần như hoàn toàn vào Zalo — Nera nên tích hợp Zalo Mini App thay vì ép tải app mới).

### Bảng Tổng Hợp Số Liệu Định Lượng Cốt Lõi

| Hiện tượng / Tiêu chí | Số liệu | Nguồn | Năm |
|---|---|---|---|
| Thời gian tìm kiếm trung bình | 10 tuần | NAR Profile of Home Buyers & Sellers | 2024, 2025 |
| Điểm xuất phát trên không gian số | 41%-47% bắt đầu online; 100% dùng internet | NAR | 2024, 2025 |
| Tính độc quyền và sự trung thành | 80% người mua chỉ làm việc với 1 môi giới | NAR / Angell Real Estate | 2025 |
| Quy tắc 5 phút | Phản hồi trong 5 phút: 100x cơ hội kết nối, 21x cơ hội qualify (so với 30 phút) | MIT / InsideSales / HBR (Oldroyd) | 2007, 2011 |
| Khoảng hở kỳ vọng thực tế | B2B mất 42-47 giờ phản hồi; BĐS riêng mất 15 giờ; 63.5% lead không được trả lời | HBR / RevenueHero / Blazeo | 2011, 2024, 2026 |
| Lãng phí nguồn lực môi giới | 70% thời gian cho tác vụ hành chính, sắp lịch, CRM thủ công | Blazeo / Apten AI | 2026 |
| Cấu trúc lực lượng môi giới VN | ~300.000 người hành nghề, chỉ 10%-13% có chứng chỉ | VARS | 2023, 2024 |
| Luật Kinh doanh BĐS | Cấm hành nghề tự do (Điều 61), bắt buộc gắn với doanh nghiệp/sàn | Luật số 29/2023/QH15 | Hiệu lực 01/08/2024 |
| Động lực mua nhà tại VN | 65% có dự định mua BĐS trong 12 tháng tới | Batdongsan.com.vn CSS | 2024, 2025 |
| Quy mô thị trường | Q1&2/2025 Hà Nội bán hơn 15.000 căn; cả năm dự kiến 31.000 căn; toàn quốc ~580.000 giao dịch | Savills, CBRE | 2025 |

### Khoảng Trống Dữ Liệu (Data Gaps)

1. Số lượng căn nhà thực tế đã xem trước khi chốt mua tại Việt Nam, và bao nhiêu chuyến đi lãng phí do tin ảo.
2. Chỉ số lãng phí thời gian thao tác vi mô: số phút/giờ mỗi ngày môi giới Việt Nam thực sự tiêu tốn để chốt một slot hẹn.
3. Tần suất xung đột lịch thực tế (Double-booking Frequency).
4. Tỷ lệ bỏ rơi khách hàng (Abandoned Lead Rate) riêng tại Việt Nam; chỉ số tắc nghẽn bộ lọc.

*(Các khoảng trống này đã được kiểm chứng bằng khảo sát thực địa — xem `FIELD_RESEARCH_SYNTHESIS.md`.)*

### Gợi ý câu hỏi khảo sát thực địa

Báo cáo đề xuất bộ câu hỏi cho hai nhóm (quản lý sàn/môi giới và người tìm nhà) để lấp các khoảng trống dữ liệu. Bộ câu hỏi này đã được phát triển thành công cụ hoàn chỉnh — xem [`FIELD_SURVEY.md`](FIELD_SURVEY.md) và [`SURVEY_FRAMEWORK.md`](SURVEY_FRAMEWORK.md). Kết quả chạy thực địa: [`FIELD_RESEARCH_SYNTHESIS.md`](FIELD_RESEARCH_SYNTHESIS.md).

### Nguồn trích dẫn

1. The Digital Imperative in Homebuying: U.S. and U.K. Buyers Begin — https://landlister.co.uk/guides/the-digital-imperative-in-homebuying
2. 88% of Home Buyers Still Rely on Agents, NAR 2025 Report Finds — https://nowbam.com/88-of-home-buyers-still-rely-on-agents-nar-2025-report-finds/
3. Latest Trends in Buyer Demographics 2026: NAR Analysis — https://aihomedesign.com/blog/real-estate/nar-profile-of-home-buyers-and-sellers/
4. NAR Profile of Home Buyers and Sellers 2025 — https://crosscountrymortgage.com/mortgage/resources/nar-profile-home-buyers-sellers-2025/
5. NAR survey finds that percentage of sellers using an agent is at all — https://www.respanews.com/rn/articlesrn/nar-survey-finds-that-percentage-of-sellers-using-95872.aspx
6. Key Takeaways from NAR's 2025 Profile of Home Buyers and Sellers — https://virginiarealtors.org/2025/12/08/key-takeaways-from-nars-2025-profile-of-home-buyers-and-sellers/
7. NLP Real Estate: How to Elevate Your Portal with AI Property Search? — https://ascendixtech.com/ai-property-search-marketplaces/
8. Real Estate App UX: How to Design Property Search That Actually — https://thefinch.design/real-estate-app-ux-design-property-search-converts-buyers/
9. Lead Response Time: Every Study (MIT, HBR, Drift) - AInora — https://ainora.lt/blog/lead-response-time-statistics-every-study-2026
10. Speed to Lead: The Harvard Research That Changed Mortgage — https://sayvo.ai/insights/speed-to-lead-harvard-research-mortgage
11. How Fast Should You Respond to a Lead? 2026 Data & Benchmarks — https://greetnow.com/blog/how-fast-should-you-respond-to-a-lead
12. Speed to Lead in 2026: 78% of B2B Buyers Pick the First Vendor to — https://marketbetter.ai/blog/speed-to-lead-guide/
13. Lead Response Time Statistics 2026: Why Speed Wins Deals — https://www.plura.ai/articles/lead-response-time-statistics-2026
14. Speed to Lead Automation in the USA: Every Lead Answered in — https://leadsnow.ai/speed-to-lead-automation-usa/
15. Speed-to-Lead Benchmarks 2026: The Data Behind Why Most — https://www.apten.ai/blog/speed-to-lead-benchmarks-2026
16. CRM Cá Nhân Cho Môi Giới: Giải Pháp Tối Ưu Data & Tăng Doanh — https://meeycrm.com/tin-tuc/crm-ca-nhan-cho-moi-gioi
17. CRM cho sàn môi giới bất động sản: Chọn đúng để không mất khách — https://cloudgo.vn/crm-cho-san-moi-gioi-bat-dong-san
18. Top 8 App tìm trọ giúp khách thuê tìm phòng nhanh, uy tín — https://smartosbooking.com/vi/docs/top-8-app-tim-tro-giup-khach-thue-tim-phong-nhanh-uy-tin
19. Why 91% of Sellers Still Choose Real Estate Agents — https://angellrealestate.com/blog/why-91--of-sellers-still-choose-real-estate-agents---even-after-all-the-headlines
20. Why Sellers Are Still Choosing Real Estate Agents — https://www.jaydabramo.com/blog/2025/11/20/why-sellers-are-still-choosing-real-estate-agents-even-in-a-year-full-of-headlines
21. Tổng hợp điểm mới về hoạt động môi giới bất động sản từ 01/8/2024 — https://luatvietnam.vn/dat-dai-nha-o/tong-hop-diem-moi-ve-hoat-dong-moi-gioi-bat-dong-san-tu-01-8-2024-567-98596-article.html
22. 14 điểm mới, đáng chú ý của Luật Kinh doanh bất động sản 2024 — https://richnguyen.vn/14-diem-moi-dang-chu-y-cua-luat-kinh-doanh-bat-dong-san-2024/
23. Những quy định mới trong Luật Kinh doanh bất động sản 2024 — https://luatduongtri.vn/luat-kinh-doanh-bat-dong-san-2024/
24. Điều kiện kinh doanh dịch vụ bất động sản - AZLAW — https://azlaw.vn/dieu-kien-kinh-doanh-dich-vu-bat-dong-san.htm
25. NAR 2025 Profile of Home Buyers and Sellers — https://www.vermontrealtors.com/buyerseller/
26. Why Data, Not AI, Will Decide The Future Of Property Search — https://www.onlinemarketplaces.com/articles/why-data-not-ai-will-decide-the-future-of-property-search/
27. What are the biggest AI proptech trends in residential property — https://realtigence.com/knowledge/what_are_the_biggest_ai_proptech_trends_in_residential_property_search_for_2026.php
28. Luật Kinh Doanh Bất Động Sản Mới Nhất Tác Động Gì Tới Thị — https://wiki.batdongsan.com.vn/wiki/luat-kinh-doanh-bat-dong-san-817313
29. Luật Kinh Doanh Bất Động Sản 2023 - Những Điểm Mới Từ 2024 — https://wiki.batdongsan.com.vn/wiki/luat-kinh-doanh-bat-dong-san-2023-814820
30. Quy định mới về môi giới bất động sản từ 01/08/2024 — https://luatvietan.vn/quy-dinh-ve-moi-gioi-bat-dong-san.html
31. Bước chuyển mình của lực lượng môi giới bất động sản — https://tapchixaydung.vn/buoc-chuyen-minh-cua-luc-luong-moi-gioi-bat-dong-san-20201224000021911.html
32. Hà Nội rà soát các sàn giao dịch bất động sản - Vietnammoi.vn — https://vietnammoi.vn/ha-noi-ra-soat-cac-san-giao-dich-bat-dong-san-202652110225750.htm
33. Điều Kiện Cấp Chứng Chỉ Hành Nghề Môi Giới Bất Động Sản — https://wiki.batdongsan.com.vn/wiki/dieu-kien-cap-chung-chi-hanh-nghe-moi-gioi-bat-dong-san-798013
34. Phần Mềm Quản Lý Bất Động Sản 2027: Top 6 Giải Pháp Tốt Nhất — https://sheet.com.vn/blog/phan-mem-quan-ly-bat-dong-san-cho-moi-gioi-sang-2026
35. Đừng chờ giá chung cư giảm sâu hơn — https://thegioitiepthi.danviet.vn/dung-cho-gia-chung-cu-giam-sau-hon-2024042520220066-d7135.html
36. Thị trường bất động sản vào chu kỳ mới, đất nền sẽ lại lên "cơn sốt" — http://www.scmsteel.com.vn/thi-truong-bat-dong-san-vao-chu-ky-moi-dat-nen-se-lai-len-con-sot-trong-nam-2024
37. Người trẻ lựa chọn tận hưởng cuộc sống hay tích lũy tài sản? - 24H — https://www.24h.com.vn/kinh-doanh/nguoi-tre-lua-chon-tan-huong-cuoc-song-hay-tich-luy-tai-san-c161a1675121.html
38. Giá chung cư Hà Nội vẫn tăng mạnh, dự án cấp tập ra hàng - CafeF — https://cafef.vn/gia-chung-cu-ha-noi-van-tang-manh-du-an-cap-tap-ra-hang-18825090808213893.chn
39. Báo cáo thị trường Bất động sản Việt Nam Q1/2025 - Savills — https://vn.savills.com.vn/research_articles/226806/223536-0
40. SPPI Q42024 (VN) - Savills Việt Nam — https://vn.savills.com.vn/research_articles/226806/220867-0
41. Khoảng hơn 25.000 căn hộ dự kiến mở bán ở Hà Nội năm 2025 — https://daidoanket.vn/khoang-hon-25-000-can-ho-du-kien-mo-ban-o-ha-noi-nam-2025-10299974.html
42. Hà Nội chuẩn bị thêm 13.700 căn hộ, gần 34.000 căn thấp tầng — https://thuongtruong.com.vn/news/ha-noi-chuan-bi-them-13700-can-ho-gan-34000-can-thap-tang-den-nam-2029-168771.html
43. Nguồn cung căn hộ Hà Nội lập kỷ lục, giá thứ cấp lần đầu giảm — https://tapchikinhtetaichinh.vn/nguon-cung-can-ho-ha-noi-lap-ky-luc-gia-thu-cap-lan-dau-giam-sau-gan-4-nam-161086.html
44. Thị trường nhà ở Hà Nội duy trì đà tăng trưởng — https://nhandan.vn/thi-truong-nha-o-ha-noi-duy-tri-da-tang-truong-post913986.html
45. NAR 2025 Profile of Home Buyers, Sellers Reveals Market Extremes — https://www.nar.realtor/news/real-estate-news/nar-2025-profile-of-home-buyers-sellers-reveals-market-extremes
46. Ten Questions to Ask Your Listing Agent At Interview — https://www.sherlockhomesaustin.com/ten-questions-to-ask-your-listing-agent-at-interview/
47. How AI is Revolutionizing Property Search and Recommendation — https://numalis.com/ai-revolutionizing-property-search-and-recommendation/
48. 2017 NAR Profile Can Help Agents Find Buyers And Sellers — https://amazingproperty.com.ng/blog/2017-nar-profile-can-help-agents-find-buyers-and-sellers/
49. Speed-to-Lead Benchmarks 2026: Response-Time Data & SLAs — https://www.digitalapplied.com/blog/speed-to-lead-response-time-benchmarks-2026-data-playbook
50. CRM cho bất động sản: Tối ưu đội môi giới | VNTECH.AI — https://vntech.ai/blog/crm-cho-bat-dong-san-toi-uu-doi-moi-gioi
51. Ứng dụng Zalo Mini App cho Bất động sản hiệu quả - Zalo OA — https://www.oazns.vn/zalo-mini-app-cho-bat-dong-san/
52. Môi Giới Bất động Sản Phải Có Chứng Chỉ Hành Nghề | Houzez Land — https://houzezland.com/moi-gioi-bat-dong-san-phai-co-chung-chi-hanh-nghe/
53. Dual Income Households Stimulating Homebuyer Market — https://nationalmortgageprofessional.com/news/24287/dual-income-households-stimulating-homebuyer-market
54. Giá nhà càng cao, bất động sản càng lún sâu vào khủng hoảng tồn kho — https://1thegioi.vn/gia-nha-cang-cao-bat-dong-san-cang-lun-sau-vao-khung-hoang-ton-kho-ngan-hang-rut-cau-cho-vay-246165.html
55. Giải pháp tìm kiếm bất động sản Vinhomes toàn diện năm 2026 — https://xemnhatot.com/tin-tuc/danh-gia-xemnhatot-com-giai-phap-tim-kiem-bat-dong-san-vinhomes-toan-dien-nam-2026

---

*Phần thân báo cáo ở trên là bản rút gọn từ nội dung nhận qua chat (bị cắt ở ~50.000 ký tự). Nếu cần bản đầy đủ nguyên văn của Gemini, dán vào tài liệu này và xóa dòng ghi chú này.*
