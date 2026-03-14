"""
utils/resume_parser.py
Extracts clean text from PDF and DOCX resume files.
"""

import io
import fitz          # PyMuPDF
import docx


def parse_resume(file_bytes: bytes, filename: str) -> str:
    """Extract plain text from a resume file (PDF or DOCX)."""
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        return _parse_pdf(file_bytes)
    elif ext in ("doc", "docx"):
        return _parse_docx(file_bytes)
    else:
        return file_bytes.decode("utf-8", errors="ignore")


def _parse_pdf(file_bytes: bytes) -> str:
    text_blocks = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_blocks.append(page.get_text("text"))
    return "\n".join(text_blocks).strip()


def _parse_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()
