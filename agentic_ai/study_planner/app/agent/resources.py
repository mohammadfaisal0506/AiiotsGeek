import urllib.parse


def get_resource_for_subtopic(subtopic: str):
    """
    Generate ONE focused resource per subtopic.
    """

    encoded = urllib.parse.quote_plus(subtopic)

    documentation = (
        f"https://www.google.com/search?q={encoded}+official+documentation+guide"
    )

    youtube = (
        f"https://www.youtube.com/results?search_query={encoded}+tutorial"
    )

    return {
        "documentation": documentation,
        "youtube": youtube
    }
