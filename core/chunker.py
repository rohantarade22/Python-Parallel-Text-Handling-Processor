import re

def split_into_chunks(text):
    # Split by sentences instead of characters
    sentences = re.split(r'[.!?]+', text)

    # Clean empty sentences
    chunks = [s.strip() for s in sentences if s.strip()]

    return chunks