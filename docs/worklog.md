# Worklog — Team P-046 (Nera)

> Ghi lại tất cả công việc đã làm theo ngày. Ai làm gì, kết quả gì.
> Bảng dưới dựng từ lịch sử commit trên toàn bộ nhánh của repo, cột Time để trống vì repo không ghi time tracking đáng tin cậy.

Tên trong bảng và tài khoản git tương ứng: **Pham Kien** — `Pham Kien`, `phamkien1917`; **Vu The Luc** — `Vu The Luc`, `Lucvuu`, `Vũ Thế Lực`; **Dat** — `datthachban12345`; **Nguyen The Anh** — `Nguyen The Anh`. Một commit xuất hiện trên nhiều nhánh chỉ tính một dòng.

---

## 2026-09-01

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | fix(seo): use the same thumbnail as the Demo Day card for the OG image | ✅ Done | `0644230` | — |
| Vu The Luc | docs(research): add the Day 28 monetization one-pager | ✅ Done | `a93eff8` | — |
| Vu The Luc | feat(eval): measure what the agent costs and prove what it must never do | ✅ Done | `dbeff92` | — |
| Vu The Luc | feat(seo): add Open Graph and Twitter card metadata | ✅ Done | `c9dbe24` | — |
| Vu The Luc | style(geo): lowercase a local variable so ruff passes on develop | ✅ Done | `26d3335` | — |
| Vu The Luc | feat(chat): show the agent's finished steps instead of one replaced line | ✅ Done | `faf2b61` | — |
| Vu The Luc | fix(booking): stop a bare past date from silently booking a year ahead | ✅ Done | `09a6054` | — |
| Vu The Luc | fix(booking): let the slot phase release, and never book an hour nobody asked for | ✅ Done | `a910dff` | — |
| Pham Kien | style(chat): keep only interactive route map and ignore local demo script | ✅ Done | `8e1431d` | — |
| Pham Kien | fix(geo): optimize SQL query by proximity to landmark and batch Goong DistanceMatrix requests | ✅ Done | `7e90cea` | — |
| Pham Kien | Cập nhật giao diện mới | ✅ Done | `aad9522` | — |
| Pham Kien | test: remove hero title to verify vercel deploy from main | ✅ Done | `bd17d26` | — |
| Pham Kien | fix: limit sale reassignment to property-assigned sales only | ✅ Done | `0a09aa2` | — |

**Tổng kết ngày:** 13 commit.

---

## 2026-08-31

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | Add last_verified_at and update properties count | ✅ Done | `55146ce` | — |

**Tổng kết ngày:** 1 commit.

---
## 2026-08-30

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | Rà commit `90954f6` (Langfuse) sau buổi mentor review, phát hiện tích hợp là no-op | ✅ Done | chưa commit | — |
| Vu The Luc | Thêm `langfuse>=3.0.0` vào `requirements.txt` và cài vào `.venv` (bản 4.15.1) | ✅ Done | chưa commit | — |
| Vu The Luc | Gom phần khởi tạo Langfuse thành helper `_trace_callbacks()` có cache trong `src/agents/graph.py`, bỏ import lồng trong hàm và ghi đè `os.environ` mỗi request | ✅ Done | chưa commit | — |
| Vu The Luc | Dọn 4 cảnh báo ruff (`W293`) trong `graph.py` | ✅ Done | chưa commit | — |
| Vu The Luc | `.env.example`: gộp khối tracing, đặt `LANGCHAIN_TRACING_V2=false` mặc định, ghi chú chỉ bật một tracer | ✅ Done | chưa commit | — |
| Vu The Luc | Bọc `GeoService.enrich_and_filter` bằng lớp đo thời gian, log riêng ms của vòng gọi Goong tách khỏi chi phí LLM | ✅ Done | chưa commit | — |
| Vu The Luc | `run_agent` gắn `langfuse_session_id` + `langfuse_user_id` cho mỗi lượt để Langfuse gom cả phiên chat | ✅ Done | chưa commit | — |
| Vu The Luc | Đặt key Langfuse thật vào `.env`, xác minh `auth_check()` = True và callback dựng được | ✅ Done | chưa commit | — |
| Vu The Luc | Viết kịch bản demo đo độ trễ bằng Langfuse (bản curl 3 lượt + bản chat giao diện 12 lượt) | ✅ Done | `docs/demo/LANGFUSE_OBSERVABILITY_DEMO.md` | — |
| Vu The Luc | Sửa lỗi supervisor đọc "thu nhập 40 triệu một tháng" thành giá nhà (hỏi lại "40 tỷ hay thuê"). Thêm `_extract_finance()` backstop + siết prompt; test hồi quy `test_supervisor_finance_extract.py` | ✅ Done | chưa commit | — |

**Bối cảnh:**

- Langfuse trong commit `90954f6` không chạy: `langfuse` thiếu trong `requirements.txt`, chưa cài trong `.venv`. Code rơi vào nhánh `ImportError`, callback rỗng, graph chạy không có trace.
- So với `stage_timings` (`1ccf9a3`): phần đo cũ chỉ tới mức node (supervisor / inventory / respond). Langfuse thêm mức dưới node — thời gian từng lời gọi LLM, token, chi phí, cây trace lồng nhau, gom theo session.
- Một lượt tìm nhà gọi LLM ba lần tuần tự (supervisor lấy intent, inventory dựng câu trả lời, respond chốt) cộng vòng gọi Goong khi lọc khoảng cách. `stage_timings` gộp Goong và LLM vào một số cho node inventory; giờ log geo tách riêng, Langfuse tách từng lời gọi LLM.
- LangSmith (`LANGCHAIN_*`) là deliverable #4 của khoá nên giữ lại, chỉ tắt mặc định để không chạy trùng hai tracer.
- `issues.md` bị commit `90954f6` xoá kèm: kiểm nhanh thì các lỗi đã sửa thật ở nơi khác (`verify_password` có chặn `app_env != "development"`, F821 thiếu import `Path` đã fix), xoá file hợp lý.

**Kiểm tra:** `ruff check src/` sạch, `pytest tests -q` 174 pass, import `from langfuse.langchain import CallbackHandler` chạy được trên bản 4.15.1, `_trace_callbacks()` trả `()` khi chưa có key.

**Tiếp theo:**

- Đặt `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` thật vào `.env`, chạy một lượt tìm nhà để lấy trace.
- Đối chiếu số Langfuse với `stage_timings` và dòng log `geo.enrich_and_filter took ... ms`.
- Commit các thay đổi trên nhánh `develop`.

**Tổng kết ngày:** hoàn thiện tích hợp Langfuse (từ no-op thành chạy được), tách phép đo Goong, dọn lint. Chưa commit.

---

## 2026-08-29

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | fix(geo): correct commute extraction and Goong provider labels, tidy manual scripts and dossier | ✅ Done | `6d9c03d` | — |
| Vu The Luc | chore: move manual API scripts out of the pytest path | ✅ Done | `24ada02` | — |
| Vu The Luc | docs: align architecture, evaluation report and documentation with real verified metrics, and add global exception handler | ✅ Done | `8e04698` | — |

**Tổng kết ngày:** 3 commit trên `develop`.

---

## 2026-08-28

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | fix: improve geographic constraints regex for hours and refine OUT_OF_SCOPE prompt guardrail | ✅ Done | `47b9fe1` | — |
| Pham Kien | feat: integrate Goong Maps distance, UI badges, and routing iframe | ✅ Done | `bbe93e1` | — |
| Vu The Luc | chore: remove outdated slide decks and update architecture, security, and eval suite | ✅ Done | `1489b71` | — |

**Tổng kết ngày:** 3 commit trên `develop`.

---

## 2026-08-27

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | Fix AI context loss and LLM bypass for out-of-scope intents | ✅ Done | `f39406b` | — |
| Pham Kien | chore: remove push_code.ps1 from repository | ✅ Done | `d87934a` | — |
| Pham Kien | fix: resolve mentor issues (#1 to #6) | ✅ Done | `f722c92` | — |
| Pham Kien | fix(ui): increase tagline text size and logo height in navbar for better legibility | ✅ Done | `8c11749` | — |
| Vu The Luc | fix(main): restore the pathlib import dropped with the logging change | ✅ Done | `de02ae3` | — |

**Tổng kết ngày:** 5 commit trên `develop`.

---

## 2026-08-26

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | fix(oauth): add in-memory fallback for oauth exchange when redis is down | ✅ Done | `e67f615` | — |
| Pham Kien | fix(auth): improve localhost login, demo credentials and multi-agent criteria evaluation | ✅ Done | `a58daf4` | — |
| Pham Kien | fix(agent): fix budget ceiling prompt instruction and real estate concept consultation | ✅ Done | `dfe1e18` | — |
| Pham Kien | fix(agent-ui): align property card price layout, add pointer cursor, fix affordability routing and concept comparison | ✅ Done | `54782cb` | — |
| Pham Kien | feat(ai): enhance conversational AI NLG, loan amortization calculation, budget validation, and dynamic contextual quick replies | ✅ Done | `9317537` | — |
| Pham Kien | fix(chat): resolve hydration mismatch and enforce sequential card entrance after typewriter | ✅ Done | `71ad7c6` | — |
| Pham Kien | feat(brand): integrate official Nera logo, symbol, favicon, and brand tokens across frontend | ✅ Done | `7de16b6` | — |
| Pham Kien | fix(chat): reconcile merge conflict, update POI validation, and sync develop | ✅ Done | `15832e0` | — |
| Pham Kien | feat(chat): harden AI agent workflow, session persistence, typewriter streaming, and test suite | ✅ Done | `23e7651` | — |
| Vu The Luc | fix(logging): restore UTF-8 console stream lost from develop | ✅ Done | `8e068f6` | — |
| Vu The Luc | style: sort supervisor imports after affordability merge | ✅ Done | `ce4d8fb` | — |
| Vu The Luc | fix(search): recognise rental vocabulary and admit an empty rental store | ✅ Done | `5b2eedd` | — |
| Vu The Luc | fix(inventory): strip broker contact pitch from listing descriptions | ✅ Done | `eed68b9` | — |
| Vu The Luc | feat(chat): confirm what Nera understood before showing results | ✅ Done | `203adad` | — |
| Vu The Luc | chore: remove dead code and temp files, repair broken debug scripts | ✅ Done | `b1117ff` | — |
| Vu The Luc | fix(chat): sync typewriter callback in an effect, not during render | ✅ Done | `dae637f` | — |

**Tổng kết ngày:** 16 commit trên `develop`.

---

## 2026-08-25

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | feat(chat): answer income questions with real maths and show live progress | ✅ Done | `e07eeff` | — |

**Tổng kết ngày:** 1 commit trên `develop`.

---

## 2026-08-24

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | chore: remove DEMO_SCRIPT_5MIN from git tracking and add to gitignore | ✅ Done | `b3c31a1` | — |
| Pham Kien | fix(search): support exact bedroom filtering when user requests specific bedroom count | ✅ Done | `8afb51c` | — |
| Pham Kien | docs: update demo script focusing on login start, group intro, and functional user flow | ✅ Done | `8dcfe61` | — |
| Pham Kien | docs: update professional 5-minute presentation script | ✅ Done | `aa7b061` | — |
| Pham Kien | style(chat): custom dark green scrollbar for chat history sidebar | ✅ Done | `6da813a` | — |
| Pham Kien | fix(chat, supervisor): prevent duplicate prompt submission and fix supervisor resume intent | ✅ Done | `51ef66a` | — |
| Pham Kien | fix(chat): fix automatic prompt sending when navigating from home buttons | ✅ Done | `85b6e0a` | — |
| Pham Kien | fix(memory): enhance memory recognition and resume search responses | ✅ Done | `737d18e` | — |
| Pham Kien | fix(migrations): add runtime cleanup for BDS_PR46136708 land property on production server | ✅ Done | `8e2448e` | — |
| Pham Kien | fix(data, ui): remove invalid land record from database/seed data and polish messenger chat bubbles | ✅ Done | `e5438d9` | — |
| Pham Kien | fix(agents): match property by title in booking, supervisor, and inventory agents | ✅ Done | `b05fcf3` | — |
| Pham Kien | fix(chat): prevent auto-sending prompt on reload, restore session smoothly, and disable double submit while loading | ✅ Done | `2782fcf` | — |
| Pham Kien | fix(search): refine multi-turn district filtering, reset criteria on fresh search, and exclude seen properties on other intent | ✅ Done | `5630325` | — |
| Pham Kien | feat: add dynamic quantity parsing, region province interleaving, and expandable property cards in chat | ✅ Done | `efed944` | — |
| Pham Kien | feat: enhance nationwide location filtering and add chat stop button | ✅ Done | `3f1beb7` | — |
| Pham Kien | fix(ai-agent): refine memory suggestion logic and filter irrelevant property cards | ✅ Done | `c287cd7` | — |
| Pham Kien | fix(properties): use strict unicode word boundaries for title normalization | ✅ Done | `3b01801` | — |
| Pham Kien | feat(properties): auto normalize and beautify property titles and abbreviations | ✅ Done | `7a2df85` | — |
| Vu The Luc | docs(readme): correct demo password behavior and note auth hardening steps | ✅ Done | `5dcb6c3` | — |
| Vu The Luc | fix(branding): replace remaining Booking Bot AI labels with Nera | ✅ Done | `939dd74` | — |
| Vu The Luc | docs(brand): add Nera brand kit with logo, icons, and slide templates | ✅ Done | `1a997d3` | — |
| Vu The Luc | docs(demo): add Phase 1 deck exports, screenshots, and final thumbnail | ✅ Done | `3c0e520` | — |
| Vu The Luc | docs(demo): add Phase 1 submission pack, slides outline, and NotebookLM source | ✅ Done | `da3f9d9` | — |
| Vu The Luc | fix(chat): harden session ownership and property matching | ✅ Done | `33b8297` | — |

**Tổng kết ngày:** 24 commit trên `develop`.

---

## 2026-08-23

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | fix(frontend): use port 3005 on 127.0.0.1 to avoid Windows port exclusion range | ✅ Done | `43cadba` | — |
| Pham Kien | fix(frontend): use standard port 3000 for next dev | ✅ Done | `4910c23` | — |
| Vu The Luc | fix(frontend): change hero headline copy | ✅ Done | `7c4c265` | — |
| Vu The Luc | fix(frontend): reduce oversized hero headline text | ✅ Done | `13a9cc6` | — |
| Vu The Luc | fix(properties): polish crawled title casing without breaking acronyms | ✅ Done | `cbf2636` | — |
| Vu The Luc | chore: trigger redeploy | ✅ Done | `75242cb` | — |
| Vu The Luc | fix(agents): fix a real crash, remove 1814 lines of confirmed dead code | ✅ Done | `56e0b47` | — |
| Vu The Luc | fix(booking): apply title cleanup everywhere, fix duplicated address | ✅ Done | `be86425` | — |

**Tổng kết ngày:** 8 commit trên `develop`.

---

## 2026-08-22

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | fix(ui): keep single toggle button in dark sidebar when open and show in header only when collapsed | ✅ Done | `5df02b6` | — |
| Pham Kien | feat(ui): add hamburger toggle button for collapsible chat history sidebar | ✅ Done | `69da27e` | — |
| Pham Kien | fix(db): ensure customer profile exists on Google login and conversation store | ✅ Done | `59983dd` | — |
| Pham Kien | fix(auth): bridge Google OAuth session to frontend cookie and Authorization header | ✅ Done | `fe72faf` | — |
| Pham Kien | fix(oauth): set production default redirect URI to render backend URL | ✅ Done | `f97ebcc` | — |
| Pham Kien | fix(auth): refine error banner and separate credentials error from oauth message | ✅ Done | `fdbcd67` | — |
| Pham Kien | feat(auth): add forgot password flow and Google Sign-in OAuth support | ✅ Done | `80f94c6` | — |
| Pham Kien | fix(ai): import normalize_text in inventory_agent to resolve NameError | ✅ Done | `d17b9d7` | — |
| Pham Kien | fix(ai): fix Decimal area formatting exception in search results and memory summary | ✅ Done | `eb00063` | — |
| Pham Kien | feat(ai): fully activate returning user flow for continuing journey and changing preferences | ✅ Done | `ebb5d2d` | — |
| Pham Kien | feat(ui): format property review with clean markdown rendering, bullets and bold tags | ✅ Done | `a428ce3` | — |
| Pham Kien | fix(sale): fix route map rendering with CartoDB Voyager tiles and containerRef | ✅ Done | `4f8e483` | — |
| Pham Kien | fix(db): change calendar_provider to GOOGLE to satisfy sale_calendar_provider_valid constraint | ✅ Done | `ace1140` | — |
| Pham Kien | feat(ai): enable floating AI assistant to review and answer questions about currently viewed property | ✅ Done | `89e1b22` | — |
| Pham Kien | feat(auth): auto-migrate and seed 20 regional xhome sales and support 123456 login | ✅ Done | `7e95ed1` | — |
| Pham Kien | fix(ui): clean login side banner by removing technical memory and cookie details | ✅ Done | `e606d2e` | — |
| Pham Kien | fix: remove dummy properties, render leaflet map tiles with CartoDB, and enable demo sale/admin login on production | ✅ Done | `866b90e` | — |
| Pham Kien | fix: make CI and Docker imports portable | ✅ Done | `abef1cf` | — |
| Pham Kien | fix: stabilize production deployment and booking flows | ✅ Done | `bd623de` | — |
| Pham Kien | fix(bookings): allow prospective buyers to view available tour slots without pre-login | ✅ Done | `759e050` | — |
| Pham Kien | fix(auth): enable cross-domain credentials, jwt localStorage persistence, and nerahome.space cors | ✅ Done | `19f3379` | — |
| Pham Kien | fix(frontend): direct API calls to NEXT_PUBLIC_API_URL on Vercel | ✅ Done | `b61f2b2` | — |
| Pham Kien | feat(backend): auto-seed properties and initial accounts if database is empty on startup | ✅ Done | `f39964c` | — |
| Pham Kien | fix(frontend): conditionalize standalone output for seamless vercel deploy | ✅ Done | `b35a442` | — |
| Pham Kien | fix(db): support neon and supabase ssl query params in asyncpg | ✅ Done | `ba28cb1` | — |
| Pham Kien | feat: finalize intelligent multi-turn comparison, feature QA, and production-ready login | ✅ Done | `68c24e5` | — |
| Pham Kien | feat(frontend): render rich markdown tables and format styled comparison tables | ✅ Done | `84d4c9d` | — |
| Pham Kien | feat: restore completed intelligent multi-agent system with deep reasoning and full test coverage | ✅ Done | `c399efc` | — |
| Vu The Luc | fix(agents): strip crawler marketing noise from property titles | ✅ Done | `4fed927` | — |

**Tổng kết ngày:** 29 commit trên `develop`.

---

## 2026-08-21

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | chore: force push to trigger github update | ✅ Done | `a645d26` | — |
| Nguyen The Anh | feat: integrate Mem0 memory service and tests from datthachban | ✅ Done | `2dbfe48` | — |

**Tổng kết ngày:** 2 commit.

---

## 2026-08-20

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Dat | memory | ✅ Done | `476c8bd` | — |
| Nguyen The Anh | feat: Tests API, routing, RAGAS | ✅ Done | `2e1b21e` | — |

**Tổng kết ngày:** 2 commit.

---

## 2026-08-19

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | Clean up test files and junk scripts, update UI and agents | ✅ Done | `f0d9b98` | — |
| Dat | Change some texts | ✅ Done | `9b0cc14` | — |

**Tổng kết ngày:** 2 commit.

---

## 2026-08-18

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | docs(management): land D-013/R-011 on backend-phamkien branch decision | ✅ Done | `f88e755` | — |

**Tổng kết ngày:** 1 commit.

---

## 2026-08-16

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | docs: tighten wording and fix stale claims in Gate 2 docs | ✅ Done | `c4e91ed` | — |
| Vu The Luc | docs: add Gate 2 submission report | ✅ Done | `63d35bf` | — |

**Tổng kết ngày:** 2 commit.

---

## 2026-08-15

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | fix: clear remaining ruff lint errors on main | ✅ Done | `6cc4786` | — |
| Pham Kien | chore: formatting adjustment in docs/database-design.md | ✅ Done | `c7e0930` | — |
| Pham Kien | chore: formatting adjustment in frontend/README.md | ✅ Done | `136acae` | — |
| Pham Kien | chore: formatting adjustment in frontend/package.json | ✅ Done | `a77ee45` | — |
| Pham Kien | chore: formatting adjustment in requirements.txt | ✅ Done | `172443c` | — |
| Pham Kien | chore: formatting adjustment in tests/conftest.py | ✅ Done | `afc0b8d` | — |
| Pham Kien | chore: formatting adjustment in src/config.py | ✅ Done | `873101d` | — |
| Pham Kien | chore: formatting adjustment in src/main.py | ✅ Done | `56a3ab1` | — |
| Pham Kien | chore: formatting adjustment in .env.example | ✅ Done | `43fdf87` | — |
| Pham Kien | chore: formatting adjustment in .gitignore | ✅ Done | `610234e` | — |
| Pham Kien | chore: formatting adjustment in README.md | ✅ Done | `67774f2` | — |
| Vu The Luc | fix: auto-fix ruff lint errors (import sort, unused imports, whitespace) | ✅ Done | `e14d492` | — |
| Pham Kien | chore: minor formatting update in docs/database-design.md | ✅ Done | `21baa79` | — |
| Pham Kien | chore: minor formatting update in frontend/README.md | ✅ Done | `3b36cc1` | — |
| Pham Kien | chore: minor formatting update in frontend/package.json | ✅ Done | `42423be` | — |
| Pham Kien | chore: minor formatting update in requirements.txt | ✅ Done | `c325965` | — |
| Pham Kien | chore: minor formatting update in tests/conftest.py | ✅ Done | `f61f5b4` | — |
| Pham Kien | chore: minor formatting update in src/config.py | ✅ Done | `10136f7` | — |
| Pham Kien | chore: minor formatting update in src/main.py | ✅ Done | `90bf8fc` | — |
| Pham Kien | chore: minor formatting update in .env.example | ✅ Done | `cd55353` | — |
| Pham Kien | chore: minor formatting update in .gitignore | ✅ Done | `b4e2d0a` | — |
| Pham Kien | chore: minor formatting update in README.md | ✅ Done | `9ddc9a3` | — |
| Pham Kien | fix: resolve ruff lint errors and update test assertions | ✅ Done | `ffb3b08` | — |
| Vu The Luc | docs: add Gate 2 demo video script | ✅ Done | `1f6c1e4` | — |
| Vu The Luc | fix: force UTF-8 console logging to stop crashes on Vietnamese text | ✅ Done | `7d603f9` | — |
| Vu The Luc | docs: fill architecture doc, add README sample queries, add Gate 2 eval evidence | ✅ Done | `0d4a9a8` | — |
| Pham Kien | chore: remove redundant mock folders | ✅ Done | `b13023b` | — |
| Pham Kien | chore: cleanup redundant root files and fix chat launcher images | ✅ Done | `f60fae4` | — |
| Pham Kien | fix: update notification bell and sale dashboard for reschedule workflow | ✅ Done | `1106404` | — |
| Pham Kien | feat: implement booking cancellation modal, sale notification, and refactor notification bell | ✅ Done | `fafc4f5` | — |

**Tổng kết ngày:** 30 commit.

---

## 2026-08-14

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | Update booking service and add scripts | ✅ Done | `d8ae9b7` | — |
| Pham Kien | fix: schema and scheduler timezone | ✅ Done | `f011e1e` | — |
| Pham Kien | feat: complete Phase 3 backend features excluding AI and docs | ✅ Done | `a2ad1c1` | — |
| Pham Kien | feat: complete Phase 3 UI, auth updates, profile and password management for frontend | ✅ Done | `3748d22` | — |
| Pham Kien | feat: complete Phase 3 UI, auth updates, profile and password management | ✅ Done | `2c71dfc` | — |

**Tổng kết ngày:** 5 commit.

---

## 2026-08-13

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | Implement Phase 1 & 2: Admin Dashboards, Sale Map, Booking UI | ✅ Done | `76a4f30` | — |
| Pham Kien | feat: add full property image gallery | ✅ Done | `6e45c1a` | — |
| Pham Kien | feat: complete customer experience and homepage flows | ✅ Done | `ee9712f` | — |

**Tổng kết ngày:** 3 commit.

---

## 2026-08-12

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | feat: complete booking platform flows and persistence | ✅ Done | `3714539` | — |

**Tổng kết ngày:** 1 commit.

---

## 2026-08-11

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | spike(ui): evaluate AI Elements for HomeMate V2 | ✅ Done | `c9a68c9` | — |
| Vu The Luc | docs(product): align mentor feedback and V2 direction | ✅ Done | `c1dd1a2` | — |

**Tổng kết ngày:** 2 commit.

---

## 2026-08-09

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | backup before reinstall Windows | ✅ Done | `b5b1ab3` | — |

**Tổng kết ngày:** 1 commit.

---

## 2026-08-08

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | docs(ui): document completed Figma user flows 01-05 | ✅ Done | `9889d86` | — |
| Pham Kien | Update DB instructions for manual PostgreSQL | ✅ Done | `ea35a8b` | — |
| Pham Kien | Update chat UI and backend API integrations | ✅ Done | `dabeef4` | — |
| Dat | Change some texts | ✅ Done | `cb040f0` | — |

**Tổng kết ngày:** 4 commit.

---

## 2026-08-07

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Vu The Luc | docs(ui): update Product PM UI UX progress report | ✅ Done | `824e142` | — |
| Vu The Luc | docs: add product alignment research and demo drafts | ✅ Done | `11d5f80` | — |
| Vu The Luc | docs: define AI home companion product direction | ✅ Done | `8cdc244` | — |
| Pham Kien | feat: Hoàn thiện UI Frontend (Responsive, luồng Đặt lịch, phân trang và dữ liệu thật) | ✅ Done | `905b1cd` | — |
| Dat | cập nhật redis | ✅ Done | `8210fab` | — |

**Tổng kết ngày:** 5 commit.

---

## 2026-08-06

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | feat: hoàn thiện code frontend 10 trang và kết nối API backend | ✅ Done | `bd0f336` | — |
| Pham Kien | docs: remove chuthich.md | ✅ Done | `7f4559c` | — |
| Pham Kien | feat: init FastAPI backend, add auth and booking APIs | ✅ Done | `5205226` | — |

**Tổng kết ngày:** 3 commit.

---

## 2026-08-05

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Pham Kien | feat: add database schema and crawled property data | ✅ Done | `ece3309` | — |
| Dat | Delete BookingBot_AI_Brief.pdf | ✅ Done | `61b3a2d` | — |
| Nguyen The Anh | Add PROJECT BRIEF.pdf | ✅ Done | `964f428` | — |
| Dat | Change some texts | ✅ Done | `b8c8766` | — |

**Tổng kết ngày:** 4 commit.

---

## 2026-08-04

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Dat | feat: add MOCKUI prototype | ✅ Done | `5cd1d3b` | — |
| Dat | Add BookingBot AI brief and PRD documents | ✅ Done | `e0815cb` | — |

**Tổng kết ngày:** 2 commit.

---

## 2026-08-03

| Member | Task | Status | Output | Time |
|--------|------|--------|--------|------|
| Dat | chore: test ai-log push 2 | ✅ Done | `b46ec1c` | — |
| Dat | chore: trigger ai-log push | ✅ Done | `0002861` | — |
| Dat | chore: update code and ai-log hooks | ✅ Done | `2447a22` | — |

**Tổng kết ngày:** 3 commit.

---
<!-- Format: copy block trên cho mỗi ngày làm việc -->
