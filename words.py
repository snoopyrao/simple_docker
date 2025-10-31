def split_words(text: str) -> list[str]:
    """
    Very simple demo "business logic": split on any whitespace
    and filter out empties.
    """
    return [w for w in text.split() if w]
