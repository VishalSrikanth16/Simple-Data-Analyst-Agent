import os
import pandas as pd
from docx import Document
import fitz  # PyMuPDF
import easyocr

reader = easyocr.Reader(['en'])  

def detect_file_type(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".csv"]:
        return "csv"
    elif ext in [".xlsx", ".xls"]:
        return "excel"
    elif ext == ".pdf":
        return "pdf"
    elif ext == ".docx":
        return "docx"
    elif ext == ".txt":
        return "txt"
    elif ext in [".jpg", ".jpeg", ".png"]:
        return "image"
    else:
        return "unsupported"

def extract_table(filepath):
    try:
        if filepath.endswith(".csv"):
            return pd.read_csv(filepath)
        elif filepath.endswith(".xlsx") or filepath.endswith(".xls"):
            return pd.read_excel(filepath)
    except Exception as e:
        return f"Error reading table: {e}"
    return None

def extract_text_from_pdf(filepath):
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

def extract_text_from_docx(filepath):
    try:
        doc = Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text_from_txt(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading TXT: {e}"

def extract_text_from_image(filepath):
    try:
        result = reader.readtext(filepath, detail=0)  # detail=0 gives plain text
        return "\n".join(result)
    except Exception as e:
        return f"Error reading Image: {e}"
