import os
import json
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not set in .env")
        _client = OpenAI(api_key=api_key)
    return _client


def call_gpt(
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0.2,
    json_mode: bool = False,
    max_tokens: int = 4096,
) -> Any:
    client = _get_client()

    kwargs: dict = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    content = response.choices[0].message.content

    if json_mode:
        return json.loads(content)
    return content


def call_gpt_chunked(
    system_prompt: str,
    chunks: list[str],
    merge_instruction: str = "Combine the following partial results into one final answer:",
    model: str = "gpt-4o",
    temperature: float = 0.2,
    json_mode: bool = False,
    max_tokens: int = 4096,
) -> Any:
    partials = []

    for i, chunk in enumerate(chunks):
        result = call_gpt(
            system_prompt=system_prompt,
            user_prompt=f"[Part {i+1} of {len(chunks)}]\n\n{chunk}",
            model=model,
            temperature=temperature,
            json_mode=False,
            max_tokens=max_tokens,
        )
        partials.append(result)

    if len(partials) == 1:
        return json.loads(partials[0]) if json_mode else partials[0]

    combined = "\n\n---\n\n".join(f"[Part {i+1}]\n{r}" for i, r in enumerate(partials))

    return call_gpt(
        system_prompt=(
            "Merge the partial analysis results below into a single, coherent, "
            "deduplicated response."
        ),
        user_prompt=f"{merge_instruction}\n\n{combined}",
        model=model,
        temperature=0.1,
        json_mode=json_mode,
        max_tokens=max_tokens,
    )
