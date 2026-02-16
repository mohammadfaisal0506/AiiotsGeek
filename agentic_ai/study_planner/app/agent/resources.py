import urllib.parse

def get_heading_documentation(topic: str):

    encoded = urllib.parse.quote_plus(topic)

    return [
        f"https://www.google.com/search?q={encoded}+academic+notes+pdf",
        f"https://www.google.com/search?q={encoded}+textbook+chapter",
        f"https://www.google.com/search?q={encoded}+university+lecture+notes"
    ]
