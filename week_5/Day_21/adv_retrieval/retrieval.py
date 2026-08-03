# retrieval.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from langchain_classic.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

def load_sample_text():
    with open("sample_document.txt", "r", encoding="utf-8") as f:
        return f.read()

def create_chunks(text):
    """Split document into chunks"""
    docs = [Document(page_content=text)]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )
    return splitter.split_documents(docs)

def enrich_chunks(chunks):
    """Add metadata to chunks"""
    for chunk in chunks:
        chunk.metadata = {
            "source": "sample_document.txt",
            "date": "2025-05-20",
            "category": "ai_research",
            "entities": ["Satyasai Esarapu", "Hyderabad", "xAI Solutions", "Bangalore", "Pune"],
            "summary": "Advanced RAG retrieval techniques discussion.",
            "has_pii": False
        }
    return chunks