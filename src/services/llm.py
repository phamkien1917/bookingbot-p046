"""OpenRouter LLM service with automatic fallback.

Supports free tier models and fallback to paid models when credits run out.
"""

import logging

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain_core.tools import BaseTool

from src.config import get_settings
from src.services import token_usage
from src.services.models import (
    MODEL_DISPLAY_NAMES,
    MODEL_PRIORITY,
    SYSTEM_PROMPT_VI,
)

logger = logging.getLogger(__name__)


class OpenRouterLLM:
    """OpenRouter LLM with automatic model fallback.

    Attempts to use free models first, then falls back to paid models
    when credits are exhausted or errors occur.
    """

    def __init__(
        self,
        preferred_model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        """Initialize OpenRouter LLM.

        Args:
            preferred_model: Specific model to use (overrides default priority)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
        """
        self.settings = get_settings()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.current_model_index = 0
        self.current_model = preferred_model or self.settings.model_name
        self.is_direct_openai = not self.settings.openrouter_api_key and bool(self.settings.openai_api_key)

        # If user specifies a model, use only that model
        if preferred_model:
            self.models = [preferred_model]
        elif self.is_direct_openai:
            self.models = ["gpt-4o-mini", "gpt-4o"]
            self.current_model = self.models[0]
            self.current_model_index = 0
        elif self.current_model in MODEL_PRIORITY:
            # Start at the configured model and keep the rest of the list as fallbacks.
            self.models = MODEL_PRIORITY
            self.current_model_index = MODEL_PRIORITY.index(self.current_model)
        else:
            # A MODEL_NAME outside the known list is still honoured. Leaving the
            # index at 0 would quietly serve MODEL_PRIORITY[0] instead, so the
            # configured model would never run and nothing would say so.
            logger.warning(
                "MODEL_NAME %r is not in MODEL_PRIORITY. Using it first, with the "
                "known list behind it as fallbacks. Add it to models.py to silence this.",
                self.current_model,
            )
            self.models = [self.current_model, *MODEL_PRIORITY]
            self.current_model_index = 0

        logger.info(
            f"LLM initialized with model: {self.current_model} "
            f"(index: {self.current_model_index}/{len(self.models)}), direct_openai: {self.is_direct_openai}"
        )

    def _get_base_url(self) -> str | None:
        """Get the API base URL."""
        if self.is_direct_openai:
            return None
        return self.settings.openrouter_base_url

    def _get_headers(self) -> dict | None:
        """Get HTTP headers for OpenRouter API."""
        if self.is_direct_openai:
            return None
        return {
            "HTTP-Referer": self.settings.openrouter_site_url,
            "X-Title": self.settings.openrouter_site_name,
        }

    def _create_chat_model(self) -> BaseChatModel:
        """Create a ChatOpenAI instance for the current model."""
        from langchain_openai import ChatOpenAI

        if self.is_direct_openai:
            api_key = self.settings.openai_api_key
        else:
            # Ensure OpenRouter API key is provided
            api_key = self.settings.openrouter_api_key
            if not api_key:
                raise ValueError(
                    "OPENROUTER_API_KEY is missing in your .env file. "
                    "Please get a free API key from https://openrouter.ai/ and add it."
                )

        return ChatOpenAI(
            model=self.models[self.current_model_index],
            api_key=api_key,
            base_url=self._get_base_url(),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=60,
            max_retries=1,
            default_headers=self._get_headers(),
        )

    def _try_next_model(self) -> bool:
        """Try the next model in the priority list.

        Returns:
            True if another model is available, False otherwise
        """
        self.current_model_index += 1
        if self.current_model_index >= len(self.models):
            logger.error("All OpenRouter models exhausted")
            return False

        self.current_model = self.models[self.current_model_index]
        logger.warning(
            f"Switching to fallback model: {self.current_model} "
            f"(index: {self.current_model_index}/{len(self.models)})"
        )
        return True

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        *,
        tools: list[BaseTool] | None = None,
    ) -> ChatResult:
        """Invoke the LLM with automatic fallback.

        Args:
            messages: List of chat messages
            tools: Optional list of tools to bind

        Returns:
            ChatResult from the LLM
        """
        last_error: Exception | None = None

        for attempt in range(len(self.models) - self.current_model_index):
            try:
                chat_model = self._create_chat_model()

                # Bind tools if provided
                if tools:
                    chat_model = chat_model.bind_tools(tools)

                # Invoke
                result = await chat_model.ainvoke(
                    messages,
                    config={"callbacks": [token_usage.UsageCallback(self.current_model)]},
                )

                # In dòng log ra Terminal để phục vụ việc quay Video Demo cho Mentor
                base_url = self._get_base_url() or "https://api.openai.com/v1"
                api_url = f"{base_url.rstrip('/')}/chat/completions"
                logger.info(f'HTTP Request: POST {api_url} "HTTP/1.1 200 OK"')

                return result

            except Exception as e:
                last_error = e
                error_str = str(e).lower()

                # Check for credits exhaustion
                if "insufficient credits" in error_str or "quota" in error_str:
                    logger.warning(f"Model {self.current_model} exhausted: {e}")
                    if not self._try_next_model():
                        raise Exception(
                            "All OpenRouter models have insufficient credits. "
                            "Please add credits to your account or use a different API."
                        ) from last_error
                    continue

                # Check for rate limiting
                if "rate limit" in error_str or "429" in error_str:
                    logger.warning(f"Rate limited on {self.current_model}: {e}")
                    if not self._try_next_model():
                        raise
                    continue

                # Other errors - try next model
                logger.warning(f"Error with {self.current_model}: {e}")
                if not self._try_next_model():
                    raise

        raise last_error or Exception("All models failed")

    async def ainvoke_structured(self, schema: type, messages: list[BaseMessage]):
        """Structured-output call that falls back down the model list like ainvoke.

        Callers used to build the chat model themselves, which skipped every retry
        here. OpenRouter answers a struggling upstream with HTTP 200 and a body of
        just {"error": ...}; the OpenAI SDK then raises on the missing `choices`,
        and the caller saw one dead model instead of the next one in the list.
        """
        last_error: Exception | None = None

        for _ in range(len(self.models) - self.current_model_index):
            try:
                structured = self._create_chat_model().with_structured_output(
                    schema, method="json_schema", strict=True
                )
                return await structured.ainvoke(
                    messages,
                    config={"callbacks": [token_usage.UsageCallback(self.current_model)]},
                )
            except Exception as e:
                last_error = e
                logger.warning(f"Structured call failed on {self.current_model}: {e}")
                if not self._try_next_model():
                    raise

        raise last_error or Exception("All models failed")

    def bind_tools(self, tools: list[BaseTool]) -> "OpenRouterLLM":
        """Bind tools to this LLM instance.

        Returns a new OpenRouterLLM with tools bound.
        """
        # For now, return self (tools will be bound at invoke time)
        # In production, you might want to cache the bound model
        return self

    @property
    def model_name(self) -> str:
        """Get the current model name."""
        return self.current_model

    @property
    def model_display_name(self) -> str:
        """Get the display name for the current model."""
        return MODEL_DISPLAY_NAMES.get(self.current_model, self.current_model)


# Singleton instance cache
_llm_instance: OpenRouterLLM | None = None


def get_llm(
    preferred_model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> OpenRouterLLM:
    """Get or create the LLM singleton instance.

    Args:
        preferred_model: Optional specific model to use
        temperature: Sampling temperature
        max_tokens: Max tokens to generate

    Returns:
        OpenRouterLLM instance
    """
    global _llm_instance

    if _llm_instance is None or preferred_model:
        _llm_instance = OpenRouterLLM(
            preferred_model=preferred_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    return _llm_instance


def get_system_prompt() -> str:
    """Get the system prompt for the Vietnamese Real Estate Agent."""
    return SYSTEM_PROMPT_VI


def reset_llm() -> None:
    """Reset the LLM singleton (useful for testing)."""
    global _llm_instance
    _llm_instance = None
