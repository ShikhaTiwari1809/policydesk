from typing import List

try:
    import tiktoken
    _enc = tiktoken.encoding_for_model("gpt-4o")
except Exception:
    _enc = None

CHUNK_SIZE = 6_000


def count_tokens(text: str) -> int:
    if _enc:
        return len(_enc.encode(text))
    return len(text) // 4  # rough fallback


def chunk_text(text: str, max_tokens: int = CHUNK_SIZE) -> List[str]:
    if count_tokens(text) <= max_tokens:
        return [text]

    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for para in paragraphs:
        n = count_tokens(para)

        if n > max_tokens:
            for sub in _split_sentences(para, max_tokens):
                chunks.append(sub)
            continue

        if current_len + n > max_tokens:
            if current:
                chunks.append("\n\n".join(current))
            current = [para]
            current_len = n
        else:
            current.append(para)
            current_len += n

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _split_sentences(text: str, max_tokens: int) -> List[str]:
    sentences = text.replace(". ", ".\n").split("\n")
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for s in sentences:
        n = count_tokens(s)
        if current_len + n > max_tokens:
            if current:
                chunks.append(" ".join(current))
            current = [s]
            current_len = n
        else:
            current.append(s)
            current_len += n

    if current:
        chunks.append(" ".join(current))

    return chunks
