import json
from utils.gpt_client import call_gpt

SYSTEM_PROMPT = """You are a claims adjudication assistant helping a human reviewer evaluate whether a claim meets policy requirements.

You'll receive the relevant policy text and a claim in JSON format. Evaluate the claim against every rule and return a decision.

Return valid JSON only:
{
  "decision": "PASS | FLAG | DENY",
  "confidence": "High | Medium | Low",
  "summary": "one sentence verdict",
  "reasons": [
    {
      "rule": "the policy rule being checked",
      "met": true,
      "explanation": "why this rule passes or fails for this specific claim"
    }
  ],
  "missing_documentation": ["docs the provider still needs to submit"],
  "policy_citations": ["exact text from the policy supporting the decision"],
  "recommendation": "what the reviewer should do next"
}

PASS = all criteria met. FLAG = borderline or missing docs, needs review. DENY = fails a hard exclusion rule.
You are a support tool — the reviewer makes the final call."""


def run(policy_text: str, claim: dict) -> dict:
    claim_json = json.dumps(claim, indent=2)

    from utils.chunker import count_tokens
    policy_section = policy_text[:12000] if count_tokens(policy_text) > 4000 else policy_text

    prompt = f"""POLICY:
{policy_section}

CLAIM:
{claim_json}

Evaluate this claim against the policy and return a JSON decision."""

    return call_gpt(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        json_mode=True,
        temperature=0.1,
        max_tokens=3000,
    )
