# Product Alignment Action Tracker

## Trạng thái sử dụng

- `Chưa bắt đầu`: Chưa có bằng chứng công việc đã bắt đầu.
- `Bản nháp đã tạo`: Đã có output nháp nhưng chưa được team xác nhận.
- `Đang thực hiện`: Có owner và bằng chứng tiến độ.
- `Blocked`: Có dependency cụ thể đang chặn.
- `Hoàn tất`: Output đã tồn tại và được người có thẩm quyền chấp nhận.

Việc một file được tạo không có nghĩa nội dung đã được team phê duyệt.

## Action tracker

| ID | Task | Owner | Priority | Status | Dependency | Output | Deadline |
|---|---|---|---|---|---|---|---|
| A-001 | Review và xác nhận Product Brief hiện tại | Product/PM + Project Lead | P0 | Bản nháp đã tạo | Team review | `docs/product/PRODUCT_BRIEF.md` được xác nhận | TBD |
| A-002 | Xác nhận ranh giới MUST/SHOULD/FUTURE/DEPRECATED | Product/PM + Project Lead | P0 | Bản nháp đã tạo | A-001 | `docs/product/MVP_SCOPE.md` được xác nhận | TBD |
| A-003 | Xác nhận phân loại material Current/Reusable/Historical/Future/Deprecated | Product/PM | P0 | Bản nháp đã tạo | A-001, A-002 | `docs/product/SCOPE_STATUS.md` được review | TBD |
| A-004 | Xác nhận Journey Session 1 và Session 2 với toàn team | Product/PM + UI/UX + Demo Lead | P0 | Bản nháp đã tạo | A-001 | `docs/product/USER_JOURNEY.md` được xác nhận | TBD |
| A-005 | Xác nhận Product Outcome, North Star và cách tính metric | Product/PM + Project Lead | P0 | Bản nháp đã tạo | A-001 | `docs/product/PRODUCT_OUTCOMES.md` được xác nhận | TBD |
| A-006 | Review IA chỉ gồm 5 trải nghiệm MVP | UI/UX + Product/PM | P0 | Bản nháp đã tạo | A-002, A-004 | `docs/ui/INFORMATION_ARCHITECTURE.md` được xác nhận | TBD |
| A-007 | Review screen requirements và acceptance criteria với frontend | UI/UX + Frontend Coordinator | P0 | Bản nháp đã tạo | A-006 | `docs/ui/SCREEN_REQUIREMENTS.md` được xác nhận | TBD |
| A-008 | Xác nhận owner cho Product, UI, research, demo và repository administration | Project Lead | P0 | Chưa bắt đầu | Team availability | RACI/owner list được ghi nhận | TBD |
| A-009 | Thu thập và ghi lại mentor feedback thực tế | Product/PM | P0 | Chưa bắt đầu | Mentor notes/meeting | Entries có xác nhận trong `MENTOR_FEEDBACK.md` | TBD |
| A-010 | Review các quyết định hiện tại và bổ sung ngày/owner nếu có bằng chứng | Product/PM + Project Lead | P0 | Bản nháp đã tạo | Team review | `DECISION_LOG.md` được xác nhận | TBD |
| A-011 | Review risk log và gán owner cho risk Cao/Cao | Project Lead + Product/PM | P0 | Bản nháp đã tạo | A-008 | `RISK_LOG.md` có owner được xác nhận | TBD |
| A-012 | Xác nhận và đưa Source of Truth/governance files vào version control | Project Lead / Repository Admin | P0 | Chưa bắt đầu | Nội dung được team xác nhận | Các file governance được repository theo dõi | TBD |
| A-013 | Lập kế hoạch phỏng vấn 5–8 người dùng mục tiêu | Product/Research | P0 | Bản nháp đã tạo | Cần xác nhận research owner và pilot guide | `docs/research/RESEARCH_PLAN.md`, `INTERVIEW_GUIDE.md`, `SYNTHESIS_TEMPLATE.md` | TBD |
| A-014 | Thực hiện user validation và tổng hợp insight | Product/Research | P1 | Chưa bắt đầu | A-013 | Research findings và implications | TBD |
| A-015 | Cập nhật Product Brief/Journey sau validation nếu cần | Product/PM | P1 | Chưa bắt đầu | A-014; decision approval | Phiên bản tài liệu có changelog | TBD |
| A-016 | Lập component reuse/deprecation inventory cho UI | UI/UX | P1 | Chưa bắt đầu | A-006, A-007 | UI component inventory | TBD |
| A-017 | Thiết kế UI cho 5 trải nghiệm theo requirements đã xác nhận | UI/UX | P1 | Chưa bắt đầu | A-007, A-016 | Wireframe/high-fidelity design | TBD |
| A-018 | Chuẩn bị frontend handoff và UX acceptance checklist | UI/UX + Frontend Coordinator | P1 | Chưa bắt đầu | A-017 | Handoff package | TBD |
| A-019 | Viết demo storyboard hai phiên | Product/PM + Demo Lead | P1 | Bản nháp đã tạo | Cần xác nhận A-004, A-005 và khả năng demo thực tế | `docs/demo/DEMO_STORYBOARD.md`, `DEMO_SCRIPT.md` | TBD |
| A-020 | Chuẩn bị pitch deck, demo plan và fallback assets | Demo Lead + Product/PM | P1 | Bản nháp đã tạo | A-019; cần owner, môi trường và asset thực tế | `docs/demo/DEMO_RUNBOOK.md`, `PITCH_DECK_OUTLINE.md`; deck/assets chưa có | TBD |
| A-021 | Chạy usability test và cập nhật metrics report | Product/Research + UI/UX | P1 | Chưa bắt đầu | A-014, A-017 | Test report với sample size và evidence | TBD |

## Quy tắc cập nhật

1. Owner cần là người hoặc vai trò được team xác nhận; tên cá nhân hiện để theo vai trò vì repository chưa có RACI đáng tin cậy.
2. Deadline giữ `TBD` cho đến khi project plan được xác nhận.
3. Không chuyển sang `Hoàn tất` chỉ vì file đã tồn tại.
4. Mỗi task hoàn tất cần liên kết output hoặc bằng chứng review.
5. Task ngoài MVP phải đi qua quyết định phạm vi trước khi thêm vào tracker.
