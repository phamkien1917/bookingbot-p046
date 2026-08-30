# AGENTS.md

## Project instructions

Before doing any work, read:

- `PROJECT_SOURCE_OF_TRUTH.md`
- `README.md`
- relevant files in `docs/`

`PROJECT_SOURCE_OF_TRUTH.md` is the current product source of truth.

If older PRD, SDS, architecture or code conflicts with it, do not silently follow the old direction. Report the conflict first.

## Current product direction

This project is an AI-centered Home Search Companion.

The core user is the person searching for a home, not the sales agent.

The MVP must emphasize:

1. Natural-language conversation.
2. User need/profile extraction.
3. Missing-information clarification.
4. Persistent memory across sessions.
5. Property feedback: like/dislike/save/reject + reason.
6. Personalized recommendations.
7. Explainable comparison and trade-offs.
8. Resume journey when the user returns.

## MVP architecture

Use:

LLM
→ Tool schema
→ Service
→ Repository
→ PostgreSQL
→ structured JSON
→ LLM explanation

The LLM must not access the database directly.

## Do not over-engineer

Do not introduce these unless explicitly requested:

- Multi-Agent
- Microservices
- Kafka/Event Bus
- TSP Sale Assignment
- complex Soft Hold
- Google Calendar sync
- CRM integration
- multi-channel notifications
- complex Sale Dashboard
- Vector DB unless justified

## Coding rules

- Keep code simple and testable.
- Use typed schemas for tool input/output.
- Repository owns database access.
- Service owns business logic.
- Tool layer validates and serializes.
- LLM handles understanding, tool selection and explanation.
- Never fabricate property facts.
- Property facts must come from the database or another explicit source.
- Test from Repository → Service → Tool → LLM.
- Get one happy path working before adding edge cases.

## Before changing code

First state:

1. What part of the MVP this task belongs to.
2. Which Product Outcome it supports.
3. Which files/modules need changes.
4. What data contract is involved.
5. What tests will verify it.

Do not modify code until this analysis is complete when the user asks for analysis first.

## Product / UI owner scope

The current user working in this repository is primarily responsible for:

- Product management documentation
- Product scope and requirements
- Mentor feedback consolidation
- User flows
- UI/UX design specifications
- Frontend implementation support
- Project coordination documents
- Demo and presentation preparation

Prioritize files under:

- `docs/product/`
- `docs/ui/`
- `docs/meetings/`
- `docs/management/`
- `docs/demo/`
- `frontend/`

Do not modify backend, AI orchestration, database schemas,
tool-calling logic, or infrastructure unless explicitly requested.

You may inspect backend files in read-only mode when needed
to understand data contracts required by the UI.

When implementing UI, do not invent backend APIs.
Use existing API contracts or clearly mark mocked data.

When writing product documents, do not invent completed work.
Clearly distinguish:
- DONE
- IN PROGRESS
- NOT STARTED
- FUTURE SCOPE