import os
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

def extract_text_from_pdf(path: str) -> str:
    try:
        return pdf_extract_text(path)
    except Exception as e:
        print("pdf extract error:", e)
        return ""

def extract_text_from_docx(path: str) -> str:
    try:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    except Exception as e:
        print("docx extract error:", e)
        return ""

def extract_text_from_txt(path: str) -> str:
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print("txt read error:", e)
        return ""

def extract_text_from_path(path: str) -> str:
    path = str(path)
    lower = path.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif lower.endswith(".docx") or lower.endswith(".doc"):
        return extract_text_from_docx(path)
    else:
        return extract_text_from_txt(path)
