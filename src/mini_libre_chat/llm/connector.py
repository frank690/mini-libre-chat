"""
This file defines a connector to connect with LLM models from different providers
"""

from openai import OpenAIError, RateLimitError, APIConnectionError, AuthenticationError
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

    def chat(self, messages: list[dict]) -> str:
        """
        Streaming chat generator with Azure OpenAI, safe from empty chunks.
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                model=self.deployment,
                stream=False,
            )

            choice = response.choices[0]
            if not choice.message or not choice.message.content:
                return "No content received from the model."

            return choice.message.content

        except RateLimitError:
            return "⚠️ Rate limit exceeded. Please try again later."
        except AuthenticationError:
            return "❌ Authentication failed. Contact the system administrator."
        except APIConnectionError:
            return "🌐 Unable to connect to the model server. Try again soon."
        except OpenAIError as e:
            return f"❗ An unexpected error occurred: {e}"
        except Exception as e:
            return f"❓ Unknown error: {e}"
