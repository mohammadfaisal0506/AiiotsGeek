import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove weird characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Trim
    return text.strip()
