from typing import List, Dict
import numpy as np, faiss, pickle, os
from config import MODEL, INDEX_PATH, CHUNK_PATH
from tools.pdf_tool import extract_pdf_chunks

def build_faiss_index(pdf_dir: str = "uploaded_pdfs") -> Dict:
    """
    Builds or loads FAISS index and chunks.
    Returns {"index": idx, "chunks": chunk_list}
    """
    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNK_PATH):
        idx = faiss.read_index(INDEX_PATH)
        with open(CHUNK_PATH, "rb") as f:
            chks = pickle.load(f)
        return {"index": idx, "chunks": chks}

    all_chunks = []
    for file in os.listdir(pdf_dir):
        if file.endswith(".pdf"):
            all_chunks.extend(extract_pdf_chunks(os.path.join(pdf_dir, file)))

    texts = [c["text"] for c in all_chunks]
    embeddings = MODEL.encode(texts)
    idx = faiss.IndexFlatL2(embeddings.shape[1])
    idx.add(np.array(embeddings))

    faiss.write_index(idx, INDEX_PATH)
    with open(CHUNK_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    return {"index": idx, "chunks": all_chunks}
