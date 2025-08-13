from pypdf import PdfReader
from pathlib import Path

def load_pdfs_text(pdf_paths: list[str]) -> dict[str, str]:
    all_text: dict[str, str] = {}
    for pdf in pdf_paths:
        p = Path(pdf)
        if not p.exists():
            continue
        reader = PdfReader(str(p))
        text = "".join(page.extract_text() or "" for page in reader.pages)
        if text:
            all_text[p.name] = text
    return all_text

def load_summary(summary_path: str) -> str:
    p = Path(summary_path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")
