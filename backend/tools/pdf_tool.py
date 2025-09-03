from typing import List, Dict
import fitz, os

def extract_pdf_chunks(file_path: str, chunk_size: int = 50) -> List[Dict]:
    """
    Extracts chunks of text from a PDF.
    Returns a list of chunks with 'text', 'source', 'page'.
    """
    doc = fitz.open(file_path)
    chunks = []
    for page_number, page in enumerate(doc):
        text = page.get_text()
        sentences = text.split('. ')
        current_chunk = ''
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + '.'
            else:
                chunks.append({
                    "text": current_chunk.strip(),
                    "source": os.path.basename(file_path),
                    "page": page_number + 1
                })
                current_chunk = sentence + '. '
        if current_chunk:
            chunks.append({
                "text": current_chunk.strip(),
                "source": os.path.basename(file_path),
                "page": page_number + 1
            })
    return chunks
