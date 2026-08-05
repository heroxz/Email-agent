import json
import os
from typing import Any
from urllib import error, request

from mcp import ClientSession

from prompt_templates import (
    ARCHIVE_PROMPT_TEMPLATE,
    CLASSIFY_PROMPT_TEMPLATE,
    REPLY_PROMPT_TEMPLATE,
    SUMMARY_PROMPT_TEMPLATE,
)
from settings import settings


def classify_intent(text: str) -> str:
    normalized_text = text.lower()
    if "summary" in normalized_text or "outline" in normalized_text:
        return "summarizer"
    if "archive" in normalized_text:
        return "archiver"
    if "reply" in normalized_text:
        return "reply_generator"
    if "classify" in normalized_text:
        return "classifier"
    return "mail_parser"


def build_tool_arguments(intent: str, text: str) -> dict[str, object]:
    if intent == "mail_parser":
        return {"input": {"raw_text": text}}
    return {"input": {"text": text}}


def build_prompt(intent: str, text: str, assist: str = '') -> str:
    if intent == "summarizer":
        return SUMMARY_PROMPT_TEMPLATE.format(content=text) + assist
    if intent == "classifier":
        return CLASSIFY_PROMPT_TEMPLATE.format(content=text) + assist
    if intent == "reply_generator":
        return REPLY_PROMPT_TEMPLATE.format(content=text) + assist
    if intent == "archiver":
        return ARCHIVE_PROMPT_TEMPLATE.format(content=text) + assist
    return text + assist


async def generate_with_model(prompt: str, intent: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY") or getattr(settings, "DeepSeek_api_key", None)
    if not api_key:
        return ""

    base_url = os.getenv("DEEPSEEK_BASE_URL") or getattr(settings, "DeepSeek_base_url", "https://api.deepseek.com")
    model_name = os.getenv("DEEPSEEK_MODEL") or getattr(settings, "DeepSeek_model", "deepseek-v4-flash")
    endpoint = base_url.rstrip("/") + "/chat/completions"

    print(f"Calling model {model_name} at {base_url} for intent {intent} with prompt: {prompt}")

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 400,
    }

    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            body = json.load(response)
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:  # pragma: no cover - network path
        print(f"Model call failed for {intent}: {exc}")
        return ""

    choices = body.get("choices", [])
    if not choices:
        return ""

    message = choices[0].get("message", {})
    if isinstance(message, dict):
        content = message.get("content", "")
        if isinstance(content, list):
            return "".join(part.get("text", "") for part in content if isinstance(part, dict))
        return str(content).strip()

    return ""


async def route_message(session: ClientSession, text: str) -> str:
    intent = classify_intent(text)
    print(f"Classified intent: {intent}")

    response = await session.call_tool(
        intent,
        arguments=build_tool_arguments(intent, text),
    )
    assist = ''
    if response.content:
        first_content = response.content[0]
        response_content = getattr(first_content, "text", str(first_content))
        assist = json.dumps(first_content.dict(), ensure_ascii=False, indent=2)
    
    prompt = build_prompt(intent, text, assist=assist)
    model_reply = await generate_with_model(prompt, intent)
    if model_reply:
        return model_reply

    # response = await session.call_tool(
    #     intent,
    #     arguments=build_tool_arguments(intent, text),
    # )

    # if response.content:
    #     first_content = response.content[0]
    #     return getattr(first_content, "text", str(first_content))

    return ""

