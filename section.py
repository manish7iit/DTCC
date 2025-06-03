import fitz
import re

def extract_text(docu):
    doc = fitz.open(docu)
    start_page = 2
    words = []
    for page_num in range(start_page, len(doc)):
        content = doc[page_num].get_text()
        content = re.sub(r'\[\d+\]|\(\d+\)|[A-Z][a-z]+ et al\.,? \d{4}', '', content)
        content = re.sub(r'\s{2,}', ' ', content)
        for word in content.strip().split():
            words.append((word, page_num))
    return words

def chunk_words(words, max_words=300, overlap=50):
    chunks = []
    i = 0
    while i < len(words):
        chunk_slice = words[i:i + max_words]
        if not chunk_slice:
            break
        chunk_words_only = [w for w, _ in chunk_slice]
        pages = [p for _, p in chunk_slice]
        chunks.append({
            'id': f"{len(chunks) + 1}",
            'start_page': min(pages),
            'end_page': max(pages),
            'word_count': len(chunk_words_only),
            'content': ' '.join(chunk_words_only)
        })
        if i + max_words >= len(words):
            break
        i += max_words - overlap
    return chunks

def chunk_pdf(doc, max_words=500, overlap=100):
    words = extract_text(doc)
    return chunk_words(words, max_words=max_words, overlap=overlap)

if __name__ == "__main__":
    doc = "example.pdf"
    chunks = chunk_pdf(doc)

    for chunk in chunks:
        print(f"\nChunk ID: {chunk['id']}")
        print(f"Pages: {chunk['start_page']}–{chunk['end_page']}")
        print(f"Words: {chunk['word_count']}")
        print(f"{chunk['content'][:300]}")