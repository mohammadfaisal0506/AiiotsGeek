def get_resources(topic: str):
    """
    Generate YouTube and documentation references for a topic.
    """

    query = topic.replace(" ", "+")

    youtube_links = [
        f"https://www.youtube.com/results?search_query={query}+tutorial",
        f"https://www.youtube.com/results?search_query={query}+full+course"
    ]

    documentation_links = [
        f"https://www.google.com/search?q={query}+official+documentation",
        f"https://www.google.com/search?q={query}+study+notes+pdf"
    ]

    return {
        "youtube": youtube_links,
        "documentation": documentation_links
    }
