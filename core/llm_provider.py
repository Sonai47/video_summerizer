import os

from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama


def get_llm():
    provider = os.getenv("LLM_PROVIDER", "mistral").strip().lower()

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b"),
            temperature=0.3,
        )

    if provider == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY is missing from .env")
        return ChatMistralAI(
            model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
            mistral_api_key=api_key,
            temperature=0.3,
            max_retries=0,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER={provider!r}. Use 'ollama' or 'mistral'."
    )
