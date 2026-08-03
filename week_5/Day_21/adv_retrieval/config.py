# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEFAULT_CHUNK_SIZE = 400
DEFAULT_CHUNK_OVERLAP = 80
COLLECTION_NAME = "advanced_retrieval_collection"
PERSIST_DIRECTORY = "./chroma_db"
BM25_RETRIEVER_K = 5