from PyPDF2 import PdfReader

def extract_text_from_file(path: str):
    if path.endswith(".pdf"):
        reader = PdfReader(path)
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
        return "pdf", text
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return "text", f.read()
