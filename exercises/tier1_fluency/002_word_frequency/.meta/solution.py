def word_freq(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    freq = word_freq(text)
    # Sort by count DESC, then word ASC.
    # Negate the count so default asc sort gives desc order for count.
    items = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return items[:n]
