from utils.chunker import count_tokens
from utils.gpt_client import call_gpt

SYSTEM_PROMPT = """You are a healthcare policy compliance analyst.

Compare the two policy versions below (A = older, B = newer) and identify every meaningful change.

Return valid JSON only:
{
  "summary": "2-3 sentence overview of what changed",
  "total_changes": <int>,
  "changes": [
    {
      "section": "section or topic name",
      "change_type": "Added | Removed | Modified",
      "impact": "High | Medium | Low",
      "description": "what changed and its clinical or billing impact",
      "version_a_text": "excerpt from Version A, or null",
      "version_b_text": "excerpt from Version B, or null"
    }
  ],
  "high_impact_count": <int>,
  "medium_impact_count": <int>,
  "low_impact_count": <int>
}

Impact guide:
- High: affects coverage eligibility, CPT codes, or reimbursement
- Medium: changes documentation rules, prior auth, or clinical criteria
- Low: editorial fixes, formatting, or clarifications with no clinical effect"""


def _trim(text: str, max_tokens: int = 4000) -> str:
    if count_tokens(text) <= max_tokens:
        return text
    ratio = max_tokens / count_tokens(text)
    cutoff = int(len(text) * ratio)
    return text[:cutoff] + "\n\n[truncated]"


def run(policy_a_text: str, policy_b_text: str) -> dict:
    a = _trim(policy_a_text)
    b = _trim(policy_b_text)

    prompt = f"""VERSION A (Older):
{a}

VERSION B (Newer):
{b}

List all changes as JSON."""

    return call_gpt(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        json_mode=True,
        temperature=0.1,
        max_tokens=4096,
    )
