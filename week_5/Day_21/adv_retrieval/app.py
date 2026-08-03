# app.py
import streamlit as st
from dotenv import load_dotenv
from config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from retrieval import load_sample_text, create_chunks, enrich_chunks
from vector_db import get_vectorstore
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

load_dotenv()

st.set_page_config(page_title="Session 3 Demo", layout="centered")
st.title("🚀 Advanced Retrieval Techniques")
st.markdown("**Hybrid Search • Metadata Filter • Reranking**")

# Sidebar
with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("Chunk Size", 200, 600, DEFAULT_CHUNK_SIZE)
    chunk_overlap = st.slider("Chunk Overlap", 0, 150, DEFAULT_CHUNK_OVERLAP)
    k_results = st.slider("Number of Results", 3, 10, 5)

# Load document
raw_text = load_sample_text()

tab1, tab2, tab3 = st.tabs(["📄 Document", "💾 Store Data", "🔍 Advanced Retrieval"])

with tab1:
    st.subheader("Sample Document")
    st.text_area("Content", raw_text, height=300)

with tab2:
    st.subheader("Store Enriched Chunks")
    if st.button("Store in Chroma Vector DB", type="primary"):
        with st.spinner("Processing..."):
            chunks = create_chunks(raw_text)
            enriched_chunks = enrich_chunks(chunks)
            vectorstore = get_vectorstore(enriched_chunks)
            
            st.session_state.vectorstore = vectorstore
            st.session_state.chunks = enriched_chunks
            st.success(f"✅ {len(enriched_chunks)} chunks stored successfully!")

with tab3:
    st.subheader("Advanced Retrieval Demo")
    query = st.text_input("Enter your query:", "AI research in Hyderabad by Satyasai")

    if st.button("Run Hybrid Search"):
        if "vectorstore" not in st.session_state or "chunks" not in st.session_state:
            st.error("Please store data first!")
        else:
            with st.spinner("Running Hybrid Search (Vector + BM25)..."):
                # Vector Retriever
                vector_retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 6})
                
                # BM25 Retriever
                bm25_retriever = BM25Retriever.from_documents(st.session_state.chunks)
                bm25_retriever.k = 6
                
                # Ensemble (Hybrid) Retriever
                ensemble_retriever = EnsembleRetriever(
                    retrievers=[vector_retriever, bm25_retriever],
                    weights=[0.7, 0.3]
                )
                
                results = ensemble_retriever.invoke(query)
                
                st.success("Hybrid Search Results (Vector + BM25)")
                for i, doc in enumerate(results[:k_results]):
                    st.write(f"**Result {i+1}**")
                    st.write(doc.page_content)
                    st.caption(f"Metadata: {doc.metadata}")