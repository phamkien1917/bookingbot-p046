# Memory Integration Guide - Mem0 OSS

## Overview

MemoryService là abstraction layer cho Mem0 OSS, cung cấp:
- **Conversation History**: Lưu lịch sử hội thoại trong PostgreSQL
- **Semantic Memory**: Vector search với Chroma/Qdrant/pgvector
- **Structured Preferences**: Facts được trích xuất và lưu structured
- **User Isolation**: Mỗi user chỉ access memory của mình
- **Extraction Policy**: LLM-based fact extraction

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MemoryService                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ ConversationStore │  │  SemanticMemory  │               │
│  │   (PostgreSQL)   │  │ (Chroma/Qdrant)  │               │
│  └──────────────────┘  └──────────────────┘               │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ PreferenceStore  │  │ ExtractionPolicy │               │
│  │   (PostgreSQL)   │  │     (LLM)        │               │
│  └──────────────────┘  └──────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

Thêm vào `.env`:

```bash
# Mem0 OSS Configuration
MEM0_PROVIDER=chroma  # chroma, qdrant, postgres
MEM0_COLLECTION_NAME=bookingbot_memory

# Chroma (default)
CHROMA_PERSIST_DIR=./data/chroma

# Hoặc Qdrant (optional)
# QDRANT_URL=http://localhost:6333

# Vector cleanup (days)
MEMORY_FORGET_AFTER_DAYS=90
```

## Usage

### 1. Basic Usage

```python
from src.services.mem0_service import get_memory_service

# Get singleton
memory = get_memory_service()

# Add message to history
await memory.add_message(
    session_id="session-123",
    user_id="user-456",
    role="user",
    content="Tôi muốn tìm căn hộ quận Cầu Giấy"
)

# Build context for LLM
context = await memory.get_context(
    user_id="user-456",
    session_id="session-123",
    current_query="Tìm căn giá rẻ"
)
# context.preferences, context.recent_conversation, etc.
```

### 2. Storing Preferences

```python
# Save a preference
await memory.save_preference(
    user_id="user-456",
    key="preferred_district",
    value="Cầu Giấy",
    confidence=0.9
)

# Get all preferences
prefs = await memory.get_preferences("user-456")
# {'preferred_district': 'Cầu Giấy', 'budget_max': 3000000000}
```

### 3. Semantic Search

```python
# Add a memory
await memory.add_memory(
    user_id="user-456",
    content="User prefers quiet neighborhoods",
    category="preference"
)

# Search memories
results = await memory.search_memories(
    user_id="user-456",
    query="neighborhood preferences",
    limit=5
)
```

### 4. Integration with Routes

Memory đã được tích hợp vào `/api/v1/chat`:

```python
# routes.py đã tự động:
# 1. Load preferences trước khi xử lý
# 2. Merge preferences vào criteria
# 3. Save messages sau khi response
```

## What Memory Stores

### ✅ Lưu vào Memory
- **User preferences**: quận ưa thích, ngân sách, loại căn
- **Conversation history**: lịch sử hội thoại
- **Learned facts**: thông tin cá nhân từ conversation
- **Context**: để LLM hiểu conversation flow

### ❌ KHÔNG Lưu vào Memory
- **Business data**: giá bất động sản, tình trạng còn trống
- **Booking status**: trạng thái lịch xem (source of truth = DB)
- **Property details**: thông tin căn hộ cụ thể
- **System prompts**: internal agent instructions

## Extraction Policy

ExtractionPolicy sử dụng LLM để trích xuất facts từ conversation:

```python
# Extracts: preferred_district, budget_max, preferred_time_slots, etc.
# Filters: greetings, acknowledgments, business data
```

System prompt trong `mem0_service.py`:

```
## CHỈ trích xuất:
- Sở thích về bất động sản
- Ngân sách
- Thời gian
- Thành viên gia đình

## KHÔNG trích xuất:
- Giá cả bất động sản (business data)
- Tình trạng còn trống (use DB)
- Trạng thái booking (use DB)
```

## Performance

Memory operations được thiết kế **non-blocking**:

```python
# Trong routes.py:
try:
    memory_context = await memory_service.get_context(...)
except Exception:
    # Non-blocking - vẫn tiếp tục nếu memory lỗi
    memory_context = None
```

Benchmark (với mocks):
- Context building: < 100ms
- Message save: < 50ms
- Search: < 200ms

## Testing

```bash
# Run memory tests
pytest tests/test_mem0_service.py -v

# Expected: 13 passed
```

## Dependencies

```bash
# Add to requirements.txt
chromadb>=0.4.0
# mem0ai>=0.1.0  # Uncomment when stable
# qdrant-client>=1.7.0  # For Qdrant
```

## API Reference

### MemoryService

| Method | Description |
|--------|-------------|
| `add_message()` | Save message to conversation history |
| `get_history()` | Get conversation history |
| `add_memory()` | Add semantic memory |
| `search_memories()` | Search semantic memories |
| `save_preference()` | Save structured preference |
| `get_preferences()` | Get all preferences |
| `get_context()` | Build context for LLM |
| `forget_memory()` | Delete a memory |

### MemoryContext

```python
class MemoryContext:
    user_id: str
    relevant_memories: list[MemoryEntry]
    preferences: dict[str, Any]
    recent_conversation: list[dict]
    summary: Optional[str]
```

## Troubleshooting

### Chroma not available
```python
# Graceful fallback - returns empty results
semantic = SemanticMemory(provider="chroma")
# Works without Chroma installed
```

### PostgreSQL connection error
```python
# Memory save/read will fail gracefully
# Agent still works (memory is optional)
```

### Extraction fails
```python
# Non-blocking - logs warning and continues
try:
    facts = await extractor.extract_facts(messages)
except Exception:
    pass  # Continue without extracted facts
```

## Future Enhancements

1. **Mem0 OSS Integration**: Khi Mem0 ổn định, thay thế SemanticMemory bằng:
   ```python
   from mem0.ai import Mem0
   m = Mem0(config={"vector_store": {...}})
   ```

2. **PostgreSQL pgvector**: Cho production:
   ```python
   MEM0_PROVIDER=postgres
   ```

3. **Cleanup Job**: Scheduled task để xóa old memories:
   ```python
   await memory.cleanup_old_memories(days=90)
   ```

4. **Memory Analytics**: Track memory hit rate, extraction accuracy
