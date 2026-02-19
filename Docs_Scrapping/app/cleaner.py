import re
import unicodedata

def clean_text(text):
    if isinstance(text, list):
        text = " ".join(text)

    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
