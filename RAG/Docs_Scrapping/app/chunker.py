def chunk_text(text: str, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = words[i:i + chunk_size]
        if len(chunk) < 50:
            continue
        chunks.append(" ".join(chunk))

    return chunks
