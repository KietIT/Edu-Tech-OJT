"""
LLM Client for the Agentic AI system.
Provides a unified interface for Claude API calls.
"""
import os
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from package directory
PACKAGE_DIR = Path(__file__).parent
ENV_FILE = PACKAGE_DIR / ".env"
load_dotenv(ENV_FILE)

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for making LLM API calls"""

    _instance: Optional['LLMClient'] = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")

        if self.api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
                logger.info(f"LLM Client initialized with model: {self.model}")
            except ImportError:
                logger.warning("anthropic package not installed. Run: pip install anthropic")
                self._client = None
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
                self._client = None
        else:
            logger.warning("ANTHROPIC_API_KEY not found in environment")
            self._client = None

        self._initialized = True

    @property
    def is_available(self) -> bool:
        """Check if LLM is available for use"""
        return self._client is not None

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Generate text using Claude.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)

        Returns:
            Generated text or None if unavailable
        """
        if not self.is_available or self._client is None:
            logger.warning("LLM not available, returning None")
            return None

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages,
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self._client.messages.create(**kwargs) 

            if response.content and len(response.content) > 0:
                return response.content[0].text
            return None

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return None

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        Generate structured output (for lists, recommendations, etc.)
        Uses lower temperature for more consistent results.
        """
        return self.generate(prompt, system_prompt, max_tokens, temperature=0.5)


# Singleton instance
llm_client = LLMClient()


def get_llm_client() -> LLMClient:
    """Get the LLM client instance"""
    return llm_client
