# Chat evaluation report

Date: 2026-08-22  
Environment: local development API at `127.0.0.1:8000`, seeded PostgreSQL, Next.js production build

## Result

The repaired service-layer chat passes the executable P0 paths used for the demo. The 50-scenario catalog is a coverage specification; it is not being represented as 50 fully automated passes.

| Check | Result | Evidence |
|---|---:|---|
| API liveness | PASS | `/health` returned `status: ok` |
| Frontend/API HTTP smoke | PASS | `/chat` on port 3001 and `/docs` on port 8000 both returned HTTP 200 |
| Anonymous multi-turn smoke | PASS | 6 turns through the real model, 1.7-6.7 s locally, non-empty responses, property context retained, no DB side effect |
| Real LLM grounded search | PASS | `gpt-4o-mini` extracted hard/soft constraints, returned 5 verified properties, disclosed uncertainty, and reported provider latency |
| Authenticated customer booking | PASS | `SEARCH -> SLOT -> WAITING_APPROVAL -> STATUS -> CANCELLED` using a real seeded property and customer |
| Sale approval | PASS | Assigned Sale accepted the request, a real `BK...` appointment was returned, chat reported `BOOKED`, cleanup succeeded |
| Frontend lint | PASS with warnings | 0 errors, 19 pre-existing/non-blocking warnings |
| Frontend production build | PASS | Next.js compiled, type-checked, and generated all 24 routes |
| Scenario catalog | PASS | Valid JSON; 50 cases across 21 categories |
| `src/agents/**` ownership boundary | PASS | `git diff --name-only -- src/agents` is empty |
| Python unit suite | NOT RUN | The repository venv points to a missing Python executable and no Python launcher is installed for new processes |
| Docker compose validation | NOT RUN | Docker is not installed in this environment |
| Visual browser interaction | NOT RUN | The listed in-app browser skill cache was unavailable; no visual pass is claimed |

## Regressions directly verified

- “đặt lịch” no longer becomes the LAND property type after accent normalization.
- Bare district names such as “ở Thanh Xuân” replace the previous location without requiring the word “Quận”.
- A new search no longer inherits hidden area, bedroom, or property-type filters; a following “3 phòng ngủ” still refines the active search.
- Search-result quick replies now offer property selections instead of asking for bedroom count again, and card addresses no longer repeat district/province text.
- Natural requests now call a real model through a strict structured schema. Model-proposed destructive filters are reconciled before SQL, and unknown model-ranked property IDs are discarded.
- The API/UI disclose whether a turn used grounded generation, intent-only AI, direct AI, or deterministic fallback.
- “căn số 1” resolves to the property returned by the prior search turn.
- Guest search and slot choice survive the login boundary; booking data remains protected by customer authentication.
- Booking creation uses domain services and real database foreign keys rather than generated placeholder UUIDs.
- The Sale-approval response reloads the new appointment instead of returning stale `appointment: null` data.
- Status and cancellation are scoped to the signed-in customer.
- The old scripted WebSocket response is disabled so it cannot contradict the durable HTTP chat path.

## Commands

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_smoke.ps1

$env:BOOKINGBOT_TEST_EMAIL="customer.demo@example.com"
$env:BOOKINGBOT_TEST_PASSWORD="Demo@123"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_booking.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_chat_sale_approval.ps1

cd frontend
npm.cmd run lint
npm.cmd run build
```

Before production deployment, restore a working Python 3.11 environment and run the Python test suite, then validate the full Compose stack in an environment with Docker. These are release gates, not claimed passes in this report.
