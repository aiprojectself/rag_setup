# parsers/text_extractor.py

import os
from .pdf_parser import extract_text_from_pdf
from .doc_parser import extract_text_from_doc


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path.lower())[1]
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".doc", ".docx"]:
        return extract_text_from_doc(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
