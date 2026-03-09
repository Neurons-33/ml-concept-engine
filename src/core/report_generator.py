import os
from typing import Optional

from google import genai
from core.prompt_template import build_report_prompt


DEFAULT_MODEL = "gemini-2.5-flash-lite"

# memory cache (避免重複呼叫 API)
cache: dict[str, str] = {}


def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


def make_cache_key(context: str, question: str, model: str) -> str:
    context = normalize_text(context)
    question = normalize_text(question)

    # 避免 cache key 過長
    short_context = context[:500]

    return f"{model}|||{short_context}|||{question}"


def get_gemini_client(api_key: Optional[str] = None) -> genai.Client:
    api_key = api_key or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Please set it in environment or .env file."
        )

    return genai.Client(api_key=api_key)


def generate_report(
    context: str,
    question: str,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> str:

    # normalize input
    context = normalize_text(context)
    question = normalize_text(question)

    if not question:
        raise ValueError("Question is empty.")

    # cache key
    cache_key = make_cache_key(context, question, model)

    # 如果同一問題 + context 已經算過，直接回傳
    if cache_key in cache:
        return cache[cache_key]

    client = get_gemini_client(api_key=api_key)

    prompt = build_report_prompt(
        context=context,
        question=question,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API request failed: {e}")

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    text = text.strip()

    # save to cache
    cache[cache_key] = text

    return text