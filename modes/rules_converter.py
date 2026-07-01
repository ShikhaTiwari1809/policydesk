from utils.chunker import chunk_text, count_tokens
from utils.gpt_client import call_gpt, call_gpt_chunked

JSON_PROMPT = """You are building a claims adjudication rules engine.

Extract every coverage rule from this policy and return a JSON object with this exact structure:
{
  "rules": [
    {
      "rule_id": "R001",
      "description": "short rule name",
      "condition": "precise clinical or admin condition that must be true",
      "action": "APPROVE | DENY | FLAG_FOR_REVIEW",
      "rationale": "policy basis",
      "priority": 1
    }
  ]
}

One rule per distinct condition. APPROVE = coverage met, DENY = excluded, FLAG_FOR_REVIEW = needs human judgment.
Order by priority (1 = evaluated first). The top-level key MUST be "rules"."""

PYTHON_PROMPT = """Convert this policy's coverage rules into a Python function.

Write `adjudicate_claim(claim: dict) -> dict` that:
- Takes a claim dict with patient/procedure info
- Checks each rule in priority order
- Returns {"decision": "APPROVE|DENY|FLAG_FOR_REVIEW", "reason": "...", "rule_triggered": "..."}

Include a short docstring listing the expected claim dict fields.
Return Python code only — no markdown fences."""


def run_json(policy_text: str) -> list:
    if count_tokens(policy_text) <= 6000:
        result = call_gpt(
            system_prompt=JSON_PROMPT,
            user_prompt=f"Extract rules from this policy:\n\n{policy_text}",
            json_mode=True,
            temperature=0.1,
        )
    else:
        result = call_gpt_chunked(
            system_prompt=JSON_PROMPT,
            chunks=chunk_text(policy_text),
            merge_instruction=(
                'Merge these rule lists into one JSON object: {"rules": [...]}. '
                "Renumber rule_ids from R001. Remove duplicates. "
                'The top-level key MUST be "rules".'
            ),
            json_mode=True,
            temperature=0.1,
        )

    # unwrap object → list (json_mode always returns an object, never a bare array)
    if isinstance(result, dict):
        # try known keys first
        for key in ("rules", "coverage_rules", "items", "adjudication_rules", "coverage_rules_list"):
            if key in result and isinstance(result[key], list):
                return result[key]
        # fallback: return the first list value found under any key
        for val in result.values():
            if isinstance(val, list):
                return val

    return result if isinstance(result, list) else []


def run_python(policy_text: str) -> str:
    if count_tokens(policy_text) > 5000:
        from modes.summarizer import run as summarize
        s = summarize(policy_text)
        criteria = s.get("coverage_criteria", [])
        exclusions = s.get("exclusions", [])
        source = "Coverage Criteria:\n" + "\n".join(f"- {c}" for c in criteria)
        source += "\n\nExclusions:\n" + "\n".join(f"- {e}" for e in exclusions)
    else:
        source = policy_text

    result = call_gpt(
        system_prompt=PYTHON_PROMPT,
        user_prompt=f"Write the adjudication function for this policy:\n\n{source}",
        json_mode=False,
        temperature=0.2,
        max_tokens=3000,
    )

    # strip fences if the model included them anyway
    if result.strip().startswith("```"):
        lines = result.strip().split("\n")
        result = "\n".join(l for l in lines if not l.strip().startswith("```"))

    return result
