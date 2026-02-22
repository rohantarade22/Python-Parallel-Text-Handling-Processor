import re
from concurrent.futures import ThreadPoolExecutor
import os


#Clean text using regex
def clean_text(chunk):
    return re.sub(r'[^a-zA-Z\s]', '', chunk)


#Split text into chunks
def split_text(text):
    chunks = text.split("\n")
    return [chunk for chunk in chunks if chunk.strip() != ""]


#Parallel processing using ThreadPoolExecutor
def parallel_process(text):
    chunks = split_text(text)

    max_workers = os.cpu_count()  # number of threads

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        cleaned_chunks = list(executor.map(clean_text, chunks))

    return cleaned_chunks