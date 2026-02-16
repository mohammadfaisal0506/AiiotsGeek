import re

def clean_text(text):
    if isinstance(text, list):
        text = " ".join(text)

    if not isinstance(text, str):
        return ""

    return text.replace("\x00", " ").strip()

