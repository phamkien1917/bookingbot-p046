# Chat architecture

The production chat path is deliberately kept outside `src/agents/**` so that the agent experiments can evolve independently.

```text
Next.js chat page
       |
       v
POST /api/v1/chat ---- session ownership / guest hand-off
       |
       +---- chat_ai_service ---- OpenAI/OpenRouter
       |          |                 |
       |          |                 +-- structured intent
       |          |                 +-- grounded narrative/ranking
       |          |
       |          +-- reconciliation / circuit breaker / visible fallback
       v
chat_orchestrator ---- chat_state_service
       |                    |
       |                    +-- conversation metadata (signed-in user)
       |                    +-- Redis/in-memory cache (guest)
       |
       +-- property search (PostgreSQL)
       +-- booking_service (availability, create, status, cancel, reschedule)
```

The model proposes intent, soft preferences and normalized criteria using a strict schema. The backend reconciles destructive filters against deterministic parsing before SQL execution. For example, a model-inferred property type is discarded unless the user explicitly named that type. The model can reorder only property IDs already returned by PostgreSQL; unknown IDs are ignored.

## State and trust boundaries

- A session retains search criteria, returned property IDs, the selected property, requested date/time, offered slots, and pending confirmations.
- Ordinal references such as "căn số 1" are resolved only against property IDs returned by the current session.
- Booking creation, cancellation, status lookup, and rescheduling use the authenticated customer ID. The chat never invents customer, property, or Sale UUIDs.
- A guest can search and choose a slot. Creating or reading a booking requires login. After login, the same high-entropy session ID is adopted and the pending action can continue.
- Raw crawler fields and seller/source metadata are not copied into chat responses.
- Listing titles/descriptions and user messages are treated as untrusted model input, never as system instructions.
- Search narratives are rendered from model-written context plus server-rendered prices, areas, bedrooms and locations. The model cannot replace those numeric facts.
- Every response exposes `ai_mode`, `ai_model`, `ai_latency_ms`, and a sanitized fallback reason. The UI shows this provenance beside the message.
- The WebSocket mock was disabled. `POST /api/v1/chat` is the single durable chat contract.

## Conversation phases

The orchestrator moves through `SEARCH`, `PROPERTY_SELECTED`, `COLLECTING_SCHEDULE`, `SLOT_SELECTION`, `AUTH_REQUIRED`, and `CONFIRMATION`. A phase is persisted after each successful turn, so a server worker change does not erase an authenticated conversation.

## Ownership

No production changes in this work touch `src/agents/**`. The integration seam is the service layer under `src/services/`, which can later call a validated agent implementation without changing the public API or booking authorization rules.
