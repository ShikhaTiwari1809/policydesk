from utils.chunker import chunk_text, count_tokens
from utils.gpt_client import call_gpt, call_gpt_chunked

SYSTEM_PROMPT = """You are a healthcare policy analyst. Read the policy document below and extract a structured summary.

Return valid JSON only, using this structure:
{
  "policy_name": "string",
  "policy_id": "string or null",
  "effective_date": "string or null",
  "purpose": "1-2 sentences on what this policy covers",
  "covered_services": ["..."],
  "cpt_codes": [{"code": "XXXXX", "description": "..."}],
  "coverage_criteria": ["each clinical/admin requirement for coverage"],
  "documentation_requirements": ["each doc item needed for the claim"],
  "exclusions": ["each explicitly excluded condition or situation"],
  "key_notes": ["frequency limits, special rules, caveats"]
}

Use exact language from the document. Return empty lists for sections not mentioned."""


def run(policy_text: str) -> dict:
    if count_tokens(policy_text) <= 6000:
        return call_gpt(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=f"Summarize this policy:\n\n{policy_text}",
            json_mode=True,
            temperature=0.1,
        )

    chunks = chunk_text(policy_text)
    return call_gpt_chunked(
        system_prompt=SYSTEM_PROMPT,
        chunks=chunks,
        merge_instruction=(
            "Merge these partial summaries into one complete JSON object. "
            "Combine all CPT codes, criteria, and exclusions — no duplicates."
        ),
        json_mode=True,
        temperature=0.1,
    )
