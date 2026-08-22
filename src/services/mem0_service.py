"""MemoryService - Mem0 OSS Abstraction Layer.

This module provides a unified memory interface that:
1. Abstracts vector store provider (Mem0 OSS)
2. Stores conversation history in PostgreSQL
3. Provides semantic memory with user isolation
4. Extracts structured facts from conversations
5. Falls back gracefully when vector store is unavailable

NOT used for:
- Property availability/pricing (source of truth = DB)
- Booking status (source of truth = DB)
- Business-critical data

Architecture:
    MemoryService
    ├── ConversationStore (PostgreSQL) - Full conversation history
    ├── SemanticMemory (Mem0) - Embeddings + vector search
    ├── PreferenceStore (PostgreSQL) - Structured facts
    └── ExtractionPolicy (LLM) - Extract facts from messages
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.config import get_settings

logger = logging.getLogger(__name__)

# ============== Pydantic Models ==============


class MemoryEntry(BaseModel):
    """A single memory entry."""
    id: str
    user_id: str
    content: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    category: Optional[str] = None  # preference, fact, plan, etc.


class ExtractedFact(BaseModel):
    """A fact extracted from conversation."""
    key: str  # e.g., "preferred_district", "budget_max"
    value: Any
    confidence: float = Field(ge=0.0, le=1.0)
    source: str = "extracted"
    category: str = "preference"


class MemoryContext(BaseModel):
    """Context passed to LLM for response generation."""
    user_id: str
    relevant_memories: list[MemoryEntry] = Field(default_factory=list)
    preferences: dict[str, Any] = Field(default_factory=dict)
    recent_conversation: list[dict] = Field(default_factory=list)
    summary: Optional[str] = None


# ============== Extraction Policy ==============


class ExtractionPolicy:
    """LLM-based policy to extract facts from conversations.

    Filters out:
    - Business data (availability, prices - use DB)
    - Greetings and acknowledgments
    - Repeated/similar facts
    - Low-confidence extractions
    """

    # System prompt for extraction
    SYSTEM_PROMPT = """Bạn là một AI trợ lý bất động sản. Nhiệm vụ của bạn là trích xuất THÔNG TIN CÁ NHÂN của khách hàng từ cuộc trò chuyện.

## CHỈ trích xuất:
1. **Sở thích về bất động sản**: quận ưa thích, loại căn hộ, diện tích mong muốn
2. **Ngân sách**: giá tối đa/tối thiểu, phương thức thanh toán
3. **Thời gian**: ngày giờ rảnh, múi giờ ưa thích
4. **Thành viên**: số người ở, có trẻ em hay không
5. **Mục đích**: mua ở, đầu tư, mua để ở cùng gia đình
6. **Yêu cầu đặc biệt**: cần thang máy, chỗ để xe, view đẹp

## KHÔNG trích xuất:
- Giá cả bất động sản hiện tại (đây là dữ liệu kinh doanh)
- Tình trạng còn trống (source of truth = database)
- Trạng thái booking (source of truth = database)
- Thông tin về căn hộ cụ thể (user chưa yêu cầu)
- Lời chào, lời cảm ơn
- Các câu ngắn không có nội dung

## Output format:
Trả về JSON array các fact:
```json
[
  {"key": "preferred_district", "value": "Cầu Giấy", "confidence": 0.9, "category": "preference"},
  {"key": "budget_max", "value": 3000000000, "confidence": 0.8, "category": "preference"}
]
```

Nếu không có fact nào, trả về: []"""

    def __init__(self):
        self._llm = None  # Lazy init

    def _get_llm(self):
        """Lazy LLM initialization."""
        if self._llm is None:
            from src.services.llm import get_llm
            from langchain_core.messages import SystemMessage
            self._llm = get_llm()
            self._system = SystemMessage(content=self.SYSTEM_PROMPT)
        return self._llm

    async def extract_facts(self, messages: list[dict]) -> list[ExtractedFact]:
        """Extract facts from a batch of messages.

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            List of extracted facts
        """
        if not messages:
            return []

        # Filter to only user messages
        user_messages = [m for m in messages if m.get("role") == "user"]
        if not user_messages:
            return []

        # Format conversation for extraction
        conversation_text = "\n".join([
            f"{m.get('role', 'unknown')}: {m.get('content', '')}"
            for m in user_messages[-5:]  # Last 5 user messages
        ])

        try:
            llm = self._get_llm()
            from langchain_core.messages import HumanMessage
            result = await llm.ainvoke([
                self._system,
                HumanMessage(content=f"Trích xuất từ cuộc trò chuyện:\n{conversation_text}")
            ])

            content = result.content if hasattr(result, 'content') else str(result)

            # Parse JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            facts_data = json.loads(content.strip())

            return [
                ExtractedFact(**f) for f in facts_data
                if f.get("confidence", 0) >= 0.6  # Filter low confidence
            ]
        except Exception as e:
            logger.warning(f"Failed to extract facts: {e}")
            return []


# ============== Semantic Memory (Mem0 Abstraction) ==============


class SemanticMemory:
    """Mem0 OSS abstraction for semantic memory.

    Provides:
    - Add/search/delete memories with user isolation
    - Provider abstraction (Chroma, Qdrant, PostgreSQL pgvector)
    - Graceful fallback when vector store unavailable
    """

    def __init__(self, provider: str = "chroma", collection_name: str = "bookingbot_memory"):
        self.provider = provider
        self.collection_name = collection_name
        self._client = None
        self._initialized = False

    def _get_client(self):
        """Get or create Mem0 client."""
        if self._client is not None:
            return self._client

        settings = get_settings()

        try:
            if self.provider == "chroma":
                import chromadb
                from chromadb.config import Settings as ChromaSettings

                self._client = chromadb.PersistentClient(
                    path=settings.chroma_persist_dir,
                    settings=ChromaSettings(anonymized_telemetry=False)
                )
            elif self.provider == "qdrant":
                # Qdrant client - requires qdrant-client package
                from qdrant_client import QdrantClient
                self._client = QdrantClient(url=settings.qdrant_url or "http://localhost:6333")
            elif self.provider == "postgres":
                # Use pgvector via Mem0
                # Requires: mem0-ai with postgres config
                from mem0.configs import Mem0Config
                self._client = {"type": "postgres", "config": settings}
            else:
                raise ValueError(f"Unknown provider: {self.provider}")

            self._initialized = True
            logger.info(f"SemanticMemory initialized with {self.provider}")
            return self._client

        except ImportError as e:
            logger.warning(f"Vector store package not available: {e}")
            self._client = None
            return None
        except Exception as e:
            logger.warning(f"Failed to initialize vector store: {e}")
            self._client = None
            return None

    async def add(
        self,
        user_id: str,
        content: str,
        metadata: Optional[dict] = None,
        category: Optional[str] = None,
    ) -> Optional[str]:
        """Add a memory entry.

        Args:
            user_id: User UUID (for isolation)
            content: Memory text
            metadata: Additional metadata
            category: Memory category

        Returns:
            Memory ID if successful, None otherwise
        """
        client = self._get_client()
        if client is None:
            return None

        memory_id = f"{user_id}:{int(time.time() * 1000)}"

        try:
            if self.provider == "chroma":
                collection = client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )

                collection.add(
                    documents=[content],
                    ids=[memory_id],
                    metadatas=[{
                        "user_id": user_id,
                        "category": category or "general",
                        **(metadata or {})
                    }]
                )
            elif self.provider == "qdrant":
                from qdrant_client.models import Distance, VectorParams, PointStruct
                from mem0.ai import Mem0

                m = Mem0(config={
                    "vector_store": {
                        "provider": "qdrant",
                        "config": {
                            "collection_name": self.collection_name,
                            "client": client
                        }
                    }
                })
                # Mem0 add_memory equivalent
                result = m.add(content, user_id=user_id, metadata=metadata)
                if result:
                    memory_id = result.get("id", memory_id)

            logger.debug(f"Added memory {memory_id} for user {user_id}")
            return memory_id

        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            return None

    async def search(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
    ) -> list[MemoryEntry]:
        """Search memories for a user.

        Args:
            user_id: User UUID
            query: Search query
            limit: Max results
            category: Filter by category

        Returns:
            List of matching memories
        """
        client = self._get_client()
        if client is None:
            return []

        try:
            if self.provider == "chroma":
                collection = client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )

                results = collection.query(
                    query_texts=[query],
                    n_results=limit,
                    where={"user_id": user_id} if not category else {
                        "user_id": user_id,
                        "category": category
                    }
                )

                memories = []
                for i, doc in enumerate(results.get("documents", [[]])[0]):
                    memories.append(MemoryEntry(
                        id=results["ids"][0][i],
                        user_id=user_id,
                        content=doc,
                        metadata=results.get("metadatas", [{}])[0].get(i, {}),
                        score=results.get("distances", [[1.0]])[0][i],
                        category=results.get("metadatas", [{}])[0].get(i, {}).get("category"),
                    ))
                return memories

            elif self.provider == "qdrant":
                from mem0.ai import Mem0
                m = Mem0(config={"vector_store": {"provider": "qdrant"}})
                results = m.search(query, user_id=user_id, limit=limit)
                return [
                    MemoryEntry(
                        id=r.get("id", ""),
                        user_id=user_id,
                        content=r.get("text", ""),
                        metadata=r.get("metadata", {}),
                        score=r.get("score", 1.0),
                        category=r.get("category"),
                    )
                    for r in results
                ]

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def delete(self, memory_id: str, user_id: str) -> bool:
        """Delete a memory.

        Args:
            memory_id: Memory ID
            user_id: User UUID (for validation)

        Returns:
            True if deleted
        """
        client = self._get_client()
        if client is None:
            return False

        try:
            if self.provider == "chroma":
                collection = client.get_or_create_collection(name=self.collection_name)
                collection.delete(ids=[memory_id], where={"user_id": user_id})
                return True
            elif self.provider == "qdrant":
                from mem0.ai import Mem0
                m = Mem0(config={"vector_store": {"provider": "qdrant"}})
                m.delete(memory_id, user_id=user_id)
                return True
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return False

        return False

    async def get_recent(self, user_id: str, limit: int = 10) -> list[MemoryEntry]:
        """Get recent memories for a user.

        Args:
            user_id: User UUID
            limit: Max results

        Returns:
            List of recent memories
        """
        return await self.search(user_id, "", limit=limit)


# ============== Conversation Store ==============


class ConversationStore:
    """PostgreSQL-based conversation storage.

    Stores full conversation history linked to sessions.
    Used for:
    - Building context for LLM
    - Extracting facts for memory
    - User analytics
    """

    def __init__(self):
        pass

    async def save_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> str:
        """Save a message to conversation history.

        Args:
            session_id: Session identifier
            user_id: User UUID
            role: Message role (user/assistant/system)
            content: Message content
            metadata: Additional metadata

        Returns:
            Message ID
        """
        from src.database.connection import get_session_context
        from src.database.models import Conversation, Message, MessageRole
        import uuid

        async with get_session_context() as session:
            # Get or create conversation
            from sqlalchemy import select
            stmt = select(Conversation).where(
                Conversation.customer_user_id == UUID(user_id),
                Conversation.status == "OPEN"
            ).order_by(Conversation.created_at.desc())
            result = await session.execute(stmt)
            conversation = result.scalar_one_or_none()

            if not conversation:
                conversation = Conversation(
                    id=uuid.uuid4(),
                    customer_user_id=UUID(user_id),
                    status="OPEN",
                )
                session.add(conversation)

            # Add message
            message = Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role=MessageRole[role.upper()] if role.upper() in MessageRole.__members__ else MessageRole.USER,
                content_redacted=content[:2000],  # Truncate long messages
                structured_payload=metadata or {},
                created_at=datetime.utcnow(),
            )
            session.add(message)
            await session.flush()

            return str(message.id)

    async def get_conversation_history(
        self,
        session_id: str,
        user_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """Get conversation history for context.

        Args:
            session_id: Session identifier
            user_id: User UUID
            limit: Max messages to return

        Returns:
            List of message dicts
        """
        from src.database.connection import get_session_context
        from src.database.models import Conversation, Message
        from sqlalchemy import select

        async with get_session_context() as session:
            # Get latest open conversation
            stmt = select(Conversation).where(
                Conversation.customer_user_id == UUID(user_id),
                Conversation.status == "OPEN"
            ).order_by(Conversation.created_at.desc())
            result = await session.execute(stmt)
            conversation = result.scalar_one_or_none()

            if not conversation:
                return []

            # Get messages
            stmt = select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at.desc()).limit(limit)
            result = await session.execute(stmt)
            messages = result.scalars().all()

            return [
                {
                    "id": str(m.id),
                    "role": m.role.value.lower(),
                    "content": m.content_redacted,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in reversed(list(messages))  # Oldest first
            ]

    async def summarize_conversation(self, session_id: str, user_id: str) -> str:
        """Generate a summary of the conversation.

        Args:
            session_id: Session identifier
            user_id: User UUID

        Returns:
            Summary text
        """
        history = await self.get_conversation_history(session_id, user_id, limit=20)

        if not history:
            return ""

        conversation_text = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in history
        ])

        try:
            from src.services.llm import get_llm
            from langchain_core.messages import HumanMessage

            llm = get_llm()
            prompt = f"""Tóm tắt cuộc trò chuyện sau trong 2-3 câu tiếng Việt, tập trung vào:
1. Mục đích của khách hàng (đang tìm căn nào, yêu cầu gì)
2. Các thông tin đã thu thập được (ngân sách, khu vực, loại căn)
3. Trạng thái hiện tại (đã đặt lịch chưa, đang xem căn nào)

Cuộc trò chuyện:
{conversation_text}

Tóm tắt:"""

            result = await llm.ainvoke([HumanMessage(content=prompt)])
            summary = result.content if hasattr(result, 'content') else str(result)
            return summary.strip()

        except Exception as e:
            logger.warning(f"Failed to summarize: {e}")
            return f"Cuộc trò chuyện có {len(history)} tin nhắn"


# ============== Preference Store ==============


class PreferenceStore:
    """Structured preferences storage using existing CustomerPreference table."""

    async def save(
        self,
        user_id: str,
        key: str,
        value: Any,
        confidence: float = 1.0,
        source: str = "extracted",
    ) -> bool:
        """Save a preference.

        Args:
            user_id: User UUID
            key: Preference key
            value: Preference value
            confidence: Confidence level
            source: Source of preference

        Returns:
            True if saved
        """
        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference
        import uuid
        from datetime import datetime

        async with get_session_context() as session:
            # Check existing
            from sqlalchemy import select
            stmt = select(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(user_id),
                CustomerPreference.preference_key == key,
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                existing.preference_value = {"value": value}
                existing.confidence = confidence
                existing.source = source.upper()
                existing.last_confirmed_at = datetime.utcnow()
            else:
                pref = CustomerPreference(
                    id=uuid.uuid4(),
                    customer_user_id=UUID(user_id),
                    preference_key=key,
                    preference_value={"value": value},
                    confidence=confidence,
                    source=source.upper(),
                    last_confirmed_at=datetime.utcnow(),
                )
                session.add(pref)

            await session.flush()
            return True

    async def get_all(self, user_id: str) -> dict[str, Any]:
        """Get all preferences for a user.

        Args:
            user_id: User UUID

        Returns:
            Dict of key -> value
        """
        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference
        from sqlalchemy import select

        async with get_session_context() as session:
            stmt = select(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(user_id),
            )
            result = await session.execute(stmt)
            prefs = result.scalars().all()

            return {
                p.preference_key: p.preference_value.get("value")
                for p in prefs
                if p.preference_value
            }

    async def delete(self, user_id: str, key: str) -> bool:
        """Delete a preference.

        Args:
            user_id: User UUID
            key: Preference key

        Returns:
            True if deleted
        """
        from src.database.connection import get_session_context
        from src.database.models import CustomerPreference
        from sqlalchemy import delete

        async with get_session_context() as session:
            stmt = delete(CustomerPreference).where(
                CustomerPreference.customer_user_id == UUID(user_id),
                CustomerPreference.preference_key == key,
            )
            result = await session.execute(stmt)
            return result.rowcount > 0


# ============== Main MemoryService ==============


class MemoryService:
    """Unified memory service for the AI agent.

    Provides:
    - Conversation history storage
    - Semantic memory with user isolation
    - Structured preference storage
    - LLM-based fact extraction
    - Context building for LLM calls

    Usage:
        service = MemoryService()
        await service.initialize()

        # Add message to history
        await service.add_message(session_id, user_id, "user", "Tôi muốn tìm căn hộ quận 7")

        # Build context for LLM
        context = await service.get_context(user_id, session_id, "Tìm căn giá rẻ")
        # context.user_id, context.recent_conversation, context.relevant_memories, etc.

        # Get preferences
        prefs = await service.get_preferences(user_id)
    """

    def __init__(
        self,
        semantic_provider: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
        settings = get_settings()

        self.semantic_provider = semantic_provider or settings.mem0_provider
        self.collection_name = collection_name or settings.mem0_collection_name
        self.extraction_enabled = settings.memory_extraction_enabled
        self.max_context_messages = settings.memory_max_context_messages

        # Sub-components
        self.conversations = ConversationStore()
        self.preferences = PreferenceStore()
        self.semantic = SemanticMemory(
            provider=self.semantic_provider,
            collection_name=self.collection_name,
        )
        self.extractor = ExtractionPolicy()

        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the memory service."""
        if self._initialized:
            return

        logger.info(f"MemoryService initializing with {self.semantic_provider}")
        self._initialized = True

    # ---- Message Operations ----

    async def add_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> str:
        """Add a message to conversation history.

        Args:
            session_id: Session identifier
            user_id: User UUID
            role: Message role (user/assistant)
            content: Message content

        Returns:
            Message ID
        """
        message_id = await self.conversations.save_message(
            session_id, user_id, role, content, metadata
        )

        # Trigger extraction on user messages
        if role == "user" and self.extraction_enabled:
            await self._extract_and_store(user_id, session_id)

        return message_id

    async def get_history(
        self,
        user_id: str,
        session_id: str,
        limit: Optional[int] = None,
    ) -> list[dict]:
        """Get conversation history.

        Args:
            user_id: User UUID
            session_id: Session identifier
            limit: Max messages

        Returns:
            List of messages
        """
        limit = limit or self.max_context_messages
        return await self.conversations.get_conversation_history(
            session_id, user_id, limit
        )

    # ---- Memory Operations ----

    async def add_memory(
        self,
        user_id: str,
        content: str,
        category: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[str]:
        """Add a semantic memory.

        Args:
            user_id: User UUID
            content: Memory text
            category: Memory category
            metadata: Additional metadata

        Returns:
            Memory ID
        """
        return await self.semantic.add(user_id, content, metadata, category)

    async def search_memories(
        self,
        user_id: str,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
    ) -> list[MemoryEntry]:
        """Search semantic memories.

        Args:
            user_id: User UUID
            query: Search query
            limit: Max results
            category: Filter by category

        Returns:
            List of matching memories
        """
        return await self.semantic.search(user_id, query, limit, category)

    async def forget_memory(self, memory_id: str, user_id: str) -> bool:
        """Delete a memory.

        Args:
            memory_id: Memory ID
            user_id: User UUID

        Returns:
            True if deleted
        """
        return await self.semantic.delete(memory_id, user_id)

    # ---- Preferences ----

    async def save_preference(
        self,
        user_id: str,
        key: str,
        value: Any,
        confidence: float = 1.0,
    ) -> bool:
        """Save a structured preference.

        Args:
            user_id: User UUID
            key: Preference key
            value: Preference value
            confidence: Confidence level

        Returns:
            True if saved
        """
        return await self.preferences.save(user_id, key, value, confidence)

    async def get_preferences(self, user_id: str) -> dict[str, Any]:
        """Get all preferences for a user.

        Args:
            user_id: User UUID

        Returns:
            Dict of preferences
        """
        return await self.preferences.get_all(user_id)

    # ---- Context Building ----

    async def get_context(
        self,
        user_id: str,
        session_id: str,
        current_query: Optional[str] = None,
    ) -> MemoryContext:
        """Build context for LLM response generation.

        This is the main method to get context for the agent.

        Args:
            user_id: User UUID
            session_id: Session identifier
            current_query: Current user query (for semantic search)

        Returns:
            MemoryContext with all relevant information
        """
        # Get recent conversation
        recent = await self.get_history(user_id, session_id)

        # Get preferences
        prefs = await self.get_preferences(user_id)

        # Get relevant memories via semantic search
        memories = []
        if current_query:
            memories = await self.search_memories(
                user_id,
                current_query,
                limit=5,
            )

        # Get conversation summary
        summary = await self.conversations.summarize_conversation(session_id, user_id)

        return MemoryContext(
            user_id=user_id,
            recent_conversation=recent,
            preferences=prefs,
            relevant_memories=memories,
            summary=summary,
        )

    # ---- Extraction Pipeline ----

    async def _extract_and_store(self, user_id: str, session_id: str) -> None:
        """Extract facts from recent messages and store.

        Called after user messages to build memory.

        Args:
            user_id: User UUID
            session_id: Session identifier
        """
        try:
            # Get recent messages
            messages = await self.get_history(user_id, session_id, limit=10)

            # Extract facts
            facts = await self.extractor.extract_facts(messages)

            # Store extracted facts
            for fact in facts:
                # Save as structured preference
                await self.save_preference(
                    user_id,
                    fact.key,
                    fact.value,
                    fact.confidence,
                )

                # Also store as semantic memory
                await self.add_memory(
                    user_id,
                    f"User prefers {fact.key}: {fact.value}",
                    category=fact.category,
                    metadata={"confidence": fact.confidence},
                )

            if facts:
                logger.debug(f"Extracted {len(facts)} facts for user {user_id}")

        except Exception as e:
            logger.warning(f"Extraction pipeline failed: {e}")

    # ---- Cleanup ----

    async def cleanup_old_memories(self, days: int = 90) -> int:
        """Clean up old memories with low confidence.

        Args:
            days: Days threshold

        Returns:
            Number of memories deleted
        """
        # This would integrate with Mem0's cleanup API
        # For now, placeholder
        logger.info(f"Cleanup triggered for memories older than {days} days")
        return 0


# ============== Singleton ==============

_memory_service: Optional[MemoryService] = None


def get_memory_service() -> MemoryService:
    """Get MemoryService singleton."""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
    return _memory_service


async def initialize_memory_service() -> MemoryService:
    """Initialize memory service asynchronously."""
    service = get_memory_service()
    await service.initialize()
    return service
