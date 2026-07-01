import os


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return _from_pdf(file_path)
    elif ext == ".txt":
        return _from_txt(file_path)
    raise ValueError(f"Unsupported file type: {ext}")


def _from_pdf(path: str) -> str:
    try:
        import fitz
    except ImportError:
        raise ImportError("PyMuPDF not installed — run: pip install pymupdf")
    with fitz.open(path) as doc:
        return "\n".join(page.get_text() for page in doc)


def _from_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_upload(uploaded_file) -> str:
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        try:
            import fitz
        except ImportError:
            raise ImportError("PyMuPDF not installed — run: pip install pymupdf")
        raw = uploaded_file.read()
        with fitz.open(stream=raw, filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)

    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    raise ValueError(f"Unsupported file: {uploaded_file.name}")
