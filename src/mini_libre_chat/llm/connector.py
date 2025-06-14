"""
This file defines a connector to connect with LLM models from different providers
"""

from typing import Generator
from mini_libre_chat.llm.constants import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_API_VERSION,
    AZURE_ENDPOINT,
    DEFAULT_DEPLOYMENT,
    DEFAULT_TOP_P,
)
from openai import AzureOpenAI


class AzureConnector:
    def __init__(
        self,
        api_key: str,
        api_version: str = DEFAULT_API_VERSION,
        endpoint: str = AZURE_ENDPOINT,
        deployment: str = DEFAULT_DEPLOYMENT,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_p: float = DEFAULT_TOP_P,
    ):
        """
        Initialize the Azure OpenAI connector.

        Args:
            api_key: Azure OpenAI API key.
            endpoint: Full endpoint URL, e.g., https://your-resource-name.openai.azure.com/
        """
        self.client = AzureOpenAI(
            api_version=api_version, azure_endpoint=endpoint, api_key=api_key
        )

        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.deployment = deployment

    def chat(self, message: dict[str, str]) -> Generator[str, None, None]:
        """
        Streaming chat generator with Azure OpenAI, safe from empty chunks.
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                message,
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            model=self.deployment,
            stream=True,
        )

        for chunk in response:
            # Safety check
            if not chunk.choices or not hasattr(chunk.choices[0], "delta"):
                continue  # Skip malformed or empty chunks

            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content
