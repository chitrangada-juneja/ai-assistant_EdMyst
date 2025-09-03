import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss, pickle, numpy as np
from openai import OpenAI

load_dotenv()

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INDEX_PATH = os.path.join(STORAGE_DIR, "index.faiss")
CHUNK_PATH = os.path.join(STORAGE_DIR, "chunks.pkl")
