from bs4 import BeautifulSoup
import re
import trafilatura

def html_to_text(html: str) -> str:
    # Try trafilatura extraction first (gives better article text)
    try:
        extracted = trafilatura.extract(html)
        if extracted and len(extracted) > 200:
            return extracted
    except Exception:
        pass

    # Fallback to BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts, style, nav, footer
    for t in soup(["script", "style", "noscript", "header", "footer", "svg", "nav", "iframe"]):
        t.extract()

    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text
