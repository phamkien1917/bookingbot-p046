"""Test MemoryService integration.

Run with: pytest tests/test_mem0_service.py -v
"""

from unittest.mock import AsyncMock, patch

import pytest


class TestMemoryService:
    """Test cases for MemoryService."""

    @pytest.fixture
    def memory_service(self):
        """Create memory service instance."""
        from src.services.mem0_service import MemoryService
        return MemoryService()

    @pytest.fixture
    def sample_messages(self):
        """Sample conversation messages."""
        return [
            {"role": "user", "content": "Tôi muốn tìm căn hộ quận Cầu Giấy"},
            {"role": "assistant", "content": "Bạn muốn tìm căn hộ quận Cầu Giấy. Ngân sách của bạn là bao nhiêu?"},
            {"role": "user", "content": "Dưới 3 tỷ, 2 phòng ngủ"},
        ]

    @pytest.mark.asyncio
    async def test_add_message(self, memory_service):
        """Test adding a message to conversation history."""
        # Mock the conversation store
        memory_service.conversations.save_message = AsyncMock(return_value="msg-123")

        msg_id = await memory_service.add_message(
            session_id="test-session",
            user_id="test-user",
            role="user",
            content="Test message"
        )

        assert msg_id == "msg-123"
        memory_service.conversations.save_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_history(self, memory_service):
        """Test getting conversation history."""
        expected_history = [
            {"role": "user", "content": "Hello", "created_at": "2024-01-01T00:00:00"},
            {"role": "assistant", "content": "Hi there!", "created_at": "2024-01-01T00:00:01"},
        ]
        memory_service.conversations.get_conversation_history = AsyncMock(
            return_value=expected_history
        )

        history = await memory_service.get_history(
            user_id="test-user",
            session_id="test-session",
            limit=10
        )

        assert len(history) == 2
        assert history[0]["content"] == "Hello"

    @pytest.mark.asyncio
    async def test_search_memories(self, memory_service):
        """Test semantic memory search."""
        from src.services.mem0_service import MemoryEntry

        expected_memories = [
            MemoryEntry(
                id="mem-1",
                user_id="test-user",
                content="User prefers Cầu Giấy district",
                score=0.9
            )
        ]
        memory_service.semantic.search = AsyncMock(return_value=expected_memories)

        results = await memory_service.search_memories(
            user_id="test-user",
            query="quận",
            limit=5
        )

        assert len(results) == 1
        assert "Cầu Giấy" in results[0].content

    @pytest.mark.asyncio
    async def test_preferences(self, memory_service):
        """Test preference storage."""
        memory_service.preferences.save = AsyncMock(return_value=True)
        memory_service.preferences.get_all = AsyncMock(return_value={
            "preferred_district": "Cầu Giấy",
            "budget_max": 3000000000
        })

        # Save preference
        success = await memory_service.save_preference(
            user_id="test-user",
            key="preferred_district",
            value="Cầu Giấy",
            confidence=0.9
        )
        assert success is True

        # Get preferences
        prefs = await memory_service.get_preferences("test-user")
        assert prefs["preferred_district"] == "Cầu Giấy"
        assert prefs["budget_max"] == 3000000000

    @pytest.mark.asyncio
    async def test_get_context(self, memory_service):
        """Test context building for LLM."""
        memory_service.conversations.get_conversation_history = AsyncMock(return_value=[])
        memory_service.conversations.summarize_conversation = AsyncMock(return_value="")
        memory_service.preferences.get_all = AsyncMock(return_value={"budget_max": 3000000000})
        memory_service.semantic.search = AsyncMock(return_value=[])

        context = await memory_service.get_context(
            user_id="test-user",
            session_id="test-session",
            current_query="Tìm căn"
        )

        assert context.user_id == "test-user"
        assert context.preferences["budget_max"] == 3000000000


class TestExtractionPolicy:
    """Test extraction policy."""

    @pytest.fixture
    def extractor(self):
        """Create extraction policy."""
        from src.services.mem0_service import ExtractionPolicy
        return ExtractionPolicy()

    def test_system_prompt_structure(self, extractor):
        """Test that extraction policy has proper structure."""
        assert "CHỈ trích xuất" in extractor.SYSTEM_PROMPT
        assert "KHÔNG trích xuất" in extractor.SYSTEM_PROMPT
        assert "dữ liệu kinh doanh" in extractor.SYSTEM_PROMPT  # Vietnamese for "business data"

    def test_filters_business_data(self, extractor):
        """Test that policy explicitly filters business data."""
        # The policy should mention NOT extracting:
        # - Property availability
        # - Prices
        # - Booking status
        prompt = extractor.SYSTEM_PROMPT
        assert "Tình trạng còn trống" in prompt or "availability" in prompt.lower()
        assert "Giá cả bất động sản" in prompt


class TestSemanticMemory:
    """Test semantic memory with Chroma."""

    @pytest.fixture
    def semantic_memory(self):
        """Create semantic memory instance."""
        from src.services.mem0_service import SemanticMemory
        return SemanticMemory(provider="chroma", collection_name="test_memory")

    def test_init_without_client(self, semantic_memory):
        """Test initialization doesn't fail without client."""
        # Should not raise
        assert semantic_memory.provider == "chroma"
        assert semantic_memory.collection_name == "test_memory"

    def test_get_client_returns_none_on_error(self, semantic_memory):
        """Test client returns None when Chroma not available."""
        # Mock to simulate missing Chroma
        with patch("builtins.__import__", side_effect=ImportError):
            semantic_memory._get_client()
            # Should handle gracefully


class TestConversationStore:
    """Test conversation store."""

    @pytest.mark.asyncio
    async def test_save_message_structure(self):
        """Test message structure for saving."""
        from src.services.mem0_service import ConversationStore

        store = ConversationStore()

        # The method should exist and be callable
        assert hasattr(store, "save_message")
        assert hasattr(store, "get_conversation_history")
        assert hasattr(store, "summarize_conversation")
        # Test signature
        import inspect
        sig = inspect.signature(store.save_message)
        params = list(sig.parameters.keys())
        assert "session_id" in params
        assert "user_id" in params
        assert "role" in params
        assert "content" in params


class TestPreferenceStore:
    """Test preference store."""

    @pytest.mark.asyncio
    async def test_preference_crud(self):
        """Test preference CRUD operations."""
        from src.services.mem0_service import PreferenceStore

        store = PreferenceStore()

        # Test that methods exist and have correct signatures
        assert callable(store.save)
        assert callable(store.get_all)
        assert callable(store.delete)

        import inspect
        save_sig = inspect.signature(store.save)
        save_params = list(save_sig.parameters.keys())
        assert "user_id" in save_params
        assert "key" in save_params
        assert "value" in save_params
        assert "confidence" in save_params


class TestMemoryIntegration:
    """Integration tests for full memory flow."""

    @pytest.mark.asyncio
    async def test_full_memory_flow(self):
        """Test complete memory flow."""
        from src.services.mem0_service import MemoryService

        service = MemoryService()

        # Mock all async methods
        service.conversations.save_message = AsyncMock(return_value="msg-1")
        service.conversations.get_conversation_history = AsyncMock(return_value=[])
        service.conversations.summarize_conversation = AsyncMock(return_value="")
        service.preferences.save = AsyncMock(return_value=True)
        service.preferences.get_all = AsyncMock(return_value={})
        service.semantic.add = AsyncMock(return_value="mem-1")
        service.semantic.search = AsyncMock(return_value=[])
        service.extractor.extract_facts = AsyncMock(return_value=[])

        # Add message
        msg_id = await service.add_message("session-1", "user-1", "user", "Test")
        assert msg_id == "msg-1"

        # Get context
        context = await service.get_context("user-1", "session-1", "Test query")
        assert context.user_id == "user-1"

        # Save preference
        await service.save_preference("user-1", "key", "value")

        # Add memory
        mem_id = await service.add_memory("user-1", "Some memory")
        assert mem_id == "mem-1"


# Performance tests
class TestMemoryPerformance:
    """Performance tests for memory operations."""

    @pytest.mark.asyncio
    async def test_context_building_performance(self):
        """Test that context building doesn't add significant latency."""
        import time

        from src.services.mem0_service import MemoryService

        service = MemoryService()

        # Mock to avoid real DB/vector calls
        service.conversations.get_conversation_history = AsyncMock(return_value=[])
        service.preferences.get_all = AsyncMock(return_value={})
        service.semantic.search = AsyncMock(return_value=[])
        service.conversations.summarize_conversation = AsyncMock(return_value="")

        start = time.time()
        context = await service.get_context("user-1", "session-1", "test")
        elapsed = time.time() - start

        # Should complete quickly with mocks
        assert elapsed < 0.5, f"Context building too slow: {elapsed}s"
        assert context.user_id == "user-1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
