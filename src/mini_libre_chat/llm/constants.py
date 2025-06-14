"""
This file contains constant values used inside the LLM module
"""

__all__ = [
    "DEFAULT_TEMPERATURE",
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_TOP_P",
    "DEFAULT_API_VERSION",
    "AZURE_ENDPOINT",
    "DEFAULT_DEPLOYMENT",
]

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TOP_P = 1.0

DEFAULT_API_VERSION = "2024-12-01-preview"
AZURE_ENDPOINT = "https://frank-mbwikz8i-swedencentral.openai.azure.com/"
DEFAULT_DEPLOYMENT = "gpt-4o-mini"
