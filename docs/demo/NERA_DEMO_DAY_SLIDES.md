---
marp: true
theme: default
size: 16:9
paginate: true
footer: "Nera · 046LTD · Demo Day Phase 1"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');
  :root {
    --ink: #102b24;
    --green: #12372f;
    --green-2: #256a58;
    --sage: #dce8df;
    --cream: #f7f4ed;
    --coral: #d76548;
    --muted: #6f7c77;
  }
  section {
    background: var(--cream);
    color: var(--ink);
    font-family: "Be Vietnam Pro", Arial, sans-serif;
    padding: 54px 68px 48px;
  }
  section::after {
    color: var(--muted);
    font-size: 14px;
  }
  header, footer {
    color: var(--muted);
    font-size: 13px;
  }
  h1 {
    color: var(--ink);
    font-size: 46px;
    line-height: 1.12;
    letter-spacing: -1.4px;
    margin: 0 0 18px;
  }
  h2 {
    color: var(--ink);
    font-size: 34px;
    line-height: 1.18;
    letter-spacing: -0.8px;
    margin: 0 0 18px;
  }
  p, li {
    font-size: 20px;
    line-height: 1.48;
  }
  strong { color: var(--green-2); }
  .eyebrow {
    color: var(--coral);
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 18px;
  }
  .sub {
    color: var(--muted);
    font-size: 20px;
    max-width: 760px;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: 0.92fr 1.08fr;
    gap: 34px;
    align-items: center;
    height: 555px;
  }
  .grid-even {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    align-items: stretch;
  }
  .card {
    background: #fff;
    border: 1px solid rgba(16,43,36,.09);
    border-radius: 24px;
    box-shadow: 0 14px 38px rgba(16,43,36,.08);
    padding: 26px 28px;
  }
  .card h3 {
    color: var(--ink);
    font-size: 22px;
    margin: 0 0 10px;
  }
  .card p {
    color: var(--muted);
    font-size: 17px;
    margin: 0;
  }
  .shot {
    background: #fff;
    border: 10px solid #fff;
    border-radius: 26px;
    box-shadow: 0 18px 54px rgba(16,43,36,.16);
    overflow: hidden;
    position: relative;
  }
  .shot img {
    display: block;
    height: 100%;
    width: 100%;
    object-fit: cover;
  }
  .crop-browser img {
    height: calc(100% + 82px);
    margin-top: -82px;
  }
  .hero-shot { height: 515px; }
  .wide-shot { height: 405px; }
  .small-shot { height: 260px; }
  .dark {
    background: var(--green);
    color: #fff;
  }
  .dark h1, .dark h2, .dark h3 { color: #fff; }
  .dark p, .dark li, .dark .sub { color: #c9d7d1; }
  .pill {
    display: inline-block;
    background: var(--sage);
    border-radius: 999px;
    color: var(--green);
    font-size: 15px;
    font-weight: 700;
    padding: 9px 14px;
    margin: 6px 6px 0 0;
  }
  .metric {
    color: var(--green);
    font-size: 38px;
    font-weight: 700;
    line-height: 1;
  }
  .metric-label {
    color: var(--muted);
    font-size: 15px;
    margin-top: 8px;
  }
  .quote {
    color: #fff;
    font-size: 36px;
    font-weight: 600;
    line-height: 1.32;
    letter-spacing: -0.8px;
  }
  .thumb {
    height: 720px;
    margin: -54px -68px -48px;
    overflow: hidden;
  }
  .thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
---

<div class="thumb">
  <img src="file:///C:/Users/LucVuu/.codex/generated_images/019feeba-5347-7130-a5f6-11c4c2ca22d7/exec-44d4550f-ccc2-4ef4-8bd4-1840b505133b.png" alt="Nera Demo Day thumbnail">
</div>

<!-- _paginate: false -->
<!-- _footer: "" -->

---

<div class="eyebrow">01 · Bài toán</div>

## Người tìm nhà biết điều mình cần — nhưng không biết phải lọc thế nào

<div class="grid-2">
  <div>
    <div class="card"><h3>Nhu cầu diễn đạt tự nhiên</h3><p>“Sống thoáng, ít ồn”, “tốt cho gia đình trẻ”, “giữ giá tốt” — không phải những bộ lọc cứng.</p></div>
    <div style="height:14px"></div>
    <div class="card"><h3>Hành trình dễ đứt đoạn</h3><p>Tiêu chí, căn đã lưu, hội thoại và lịch xem thường nằm ở nhiều nơi khác nhau.</p></div>
  </div>
  <div class="shot crop-browser hero-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154134.png" alt="Nera nhu cầu thật">
  </div>
</div>

---

<div class="eyebrow">02 · Giải pháp</div>

## Chỉ cần kể, Nera sẽ hiểu và tiếp tục từ nơi bạn đã dừng

<div class="grid-2">
  <div>
    <p><strong>Nera</strong> tiếp nhận nhu cầu bằng hội thoại tự nhiên, làm rõ tiêu chí quan trọng và ghi nhớ sở thích theo tài khoản.</p>
    <p>Mục tiêu không phải thay Sale, mà là giúp khách đi từ nhu cầu mơ hồ đến một yêu cầu xem nhà đủ rõ.</p>
    <span class="pill">Hiểu nhu cầu</span>
    <span class="pill">Ghi nhớ tiêu chí</span>
    <span class="pill">Gợi ý có lý do</span>
  </div>
  <div class="shot crop-browser hero-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154129.png" alt="Nera tiếp tục hành trình">
  </div>
</div>

---

<div class="eyebrow">03 · Trải nghiệm</div>

## Bắt đầu theo cách người dùng đang nghĩ

<div class="grid-even">
  <div class="shot crop-browser wide-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154134.png" alt="Khởi đầu theo tình huống">
  </div>
  <div class="shot crop-browser wide-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154138.png" alt="Khám phá theo khu vực">
  </div>
</div>

<p class="sub">Người dùng có thể khởi đầu từ tình huống sống, mục tiêu đầu tư hoặc khu vực đã nghĩ tới; hội thoại tiếp tục tinh chỉnh thay vì bắt họ khai lại từ đầu.</p>

---

<div class="eyebrow">04 · Dữ liệu có thật</div>

## Mỗi gợi ý đều dẫn về căn nhà trong hệ thống

<div class="grid-even">
  <div class="shot crop-browser wide-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154141.png" alt="Kho nhà Nera">
  </div>
  <div class="shot crop-browser wide-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154145.png" alt="Thẻ bất động sản Nera">
  </div>
</div>

<p class="sub">Giá, diện tích, vị trí và trạng thái được lấy từ kho nhà. Người dùng có thể hỏi sâu, lưu căn hoặc chuyển sang đặt lịch.</p>

---

<!-- _class: dark -->

<div class="eyebrow">05 · Nguyên tắc sản phẩm</div>

## AI giải thích. Dữ liệu kiểm chứng. Con người xác nhận.

<div class="grid-2">
  <div>
    <p>Nera không bịa căn ngoài hệ thống và không tự quyết định lịch thay nhân viên Sale.</p>
    <div class="grid-even">
      <div class="card"><h3>Grounded</h3><p>Gợi ý bám vào dữ liệu nhà có thể xem.</p></div>
      <div class="card"><h3>Human-in-the-loop</h3><p>Sale xác nhận khung giờ thực tế.</p></div>
    </div>
  </div>
  <div class="shot crop-browser hero-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154150.png" alt="Nguyên tắc tin cậy của Nera">
  </div>
</div>

---

<div class="eyebrow">06 · MVP hiện tại</div>

## Một hành trình liền mạch từ chat đến đặt lịch

<div class="grid-2">
  <div class="shot crop-browser hero-shot">
    <img src="file:///C:/Users/LucVuu/Pictures/Screenshots/Screenshot%202026-08-24%20154155.png" alt="Nera giữ hành trình người dùng">
  </div>
  <div>
    <div class="card"><h3>Luồng chính đã hoạt động</h3><p>Chat nhiều lượt, ghi nhớ nhu cầu, danh sách nhà, lưu căn và yêu cầu đặt lịch.</p></div>
    <div style="height:14px"></div>
    <div class="grid-even">
      <div class="card"><div class="metric">53</div><div class="metric-label">kiểm thử đạt</div></div>
      <div class="card"><div class="metric">25</div><div class="metric-label">route frontend build</div></div>
    </div>
    <p><strong>Live:</strong> https://www.nerahome.space/</p>
  </div>
</div>

---

<div class="eyebrow">07 · Phase 2</div>

## Từ “agent chạy được” đến “agent được đo lường”

<div class="grid-even">
  <div class="card"><h3>Benchmark</h3><p>Bộ ca kiểm thử nhu cầu thật; đo độ đúng tiêu chí, groundedness và tỉ lệ hoàn tất đặt lịch.</p></div>
  <div class="card"><h3>Trace & observability</h3><p>Theo dõi prompt, tool call, lỗi, độ trễ và chi phí theo từng phiên hội thoại.</p></div>
  <div class="card"><h3>Model evaluation</h3><p>So sánh chất lượng, tốc độ và chi phí trước khi đổi sang model mạnh hơn.</p></div>
  <div class="card"><h3>Data quality</h3><p>Chuẩn hóa dữ liệu nhà, trạng thái còn hàng và vòng phản hồi từ Sale.</p></div>
</div>

---

<!-- _class: dark -->
<!-- _paginate: false -->
<!-- _footer: "" -->

<div style="display:flex;align-items:center;height:100%;">
  <div>
    <div class="eyebrow">NERA · 046LTD</div>
    <div class="quote">“Nera không bắt người dùng học cách dùng bộ lọc — Nera học cách hiểu người dùng.”</div>
    <p style="margin-top:34px"><strong style="color:#f0a087">Trải nghiệm ngay:</strong> www.nerahome.space</p>
  </div>
</div>

