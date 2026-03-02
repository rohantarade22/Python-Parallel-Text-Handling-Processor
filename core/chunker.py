def split_into_chunks(text, chunk_size=200):
    """
    Split text into fixed-size character chunks.
    """
    chunks = []
    text = text.strip()

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks