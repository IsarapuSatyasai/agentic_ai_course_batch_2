# app.py
import streamlit as st
from evaluation import run_full_evaluation, GOLDEN_DATASET
from config import GENERATION_MODEL, JUDGE_MODEL, TEMPERATURE
import pandas as pd

st.set_page_config(
    page_title="RAG Evaluation Mini Project",
    page_icon="",
    layout="wide"
)

st.title("RAG Evaluation Mini Project")
st.markdown("**Generation LLM + Judge LLM | Real RAG Triad Metrics**")

# ====================== SIDEBAR - PARAMETERS ======================
st.sidebar.header("Parameters")

generation_model = st.sidebar.selectbox(
    "Generation Model",
    options=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
    index=0
)

judge_model = st.sidebar.selectbox(
    "Judge Model",
    options=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
    index=0
)

temperature = st.sidebar.slider(
    "Generation Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.1,
    step=0.05
)

st.sidebar.markdown("---")
st.sidebar.info("Using OpenAI models for both Generation and Judging.")

# ====================== MAIN TABS ======================
tab1, tab2, tab3 = st.tabs(["Golden Dataset", "Run Evaluation", "About"])

# ---------- TAB 1: Golden Dataset ----------
with tab1:
    st.subheader("Golden Dataset")
    st.write("These are the test cases used for evaluation.")

    for i, item in enumerate(GOLDEN_DATASET, 1):
        with st.expander(f"Test Case {i}: {item['question']}"):
            st.markdown(f"**Question:** {item['question']}")
            st.markdown(f"**Context:** {item['context']}")
            st.markdown(f"**Ground Truth:** {item['ground_truth']}")

# ---------- TAB 2: Run Evaluation ----------
with tab2:
    st.subheader("Run RAG Evaluation")

    if st.button("Start Evaluation", type="primary", use_container_width=True):
        with st.spinner("Generating answers + Judging with LLMs... Please wait..."):
            results = run_full_evaluation(
                generation_model=generation_model,
                judge_model=judge_model,
                temperature=temperature
            )

            st.session_state["results"] = results
            st.success("Evaluation Completed!")

    if "results" in st.session_state:
        results = st.session_state["results"]

        # Overall Summary
        st.markdown("### Overall Scores")
        avg_faithfulness = sum(r["faithfulness"] for r in results) / len(results)
        avg_relevancy = sum(r["answer_relevancy"] for r in results) / len(results)
        avg_context = sum(r["context_relevancy"] for r in results) / len(results)
        avg_overall = sum(r["overall_score"] for r in results) / len(results)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Faithfulness", f"{avg_faithfulness:.3f}")
        col2.metric("Answer Relevancy", f"{avg_relevancy:.3f}")
        col3.metric("Context Relevancy", f"{avg_context:.3f}")
        col4.metric("Overall Score", f"{avg_overall:.3f}")

        st.markdown("---")

        # Detailed Results
        st.markdown("### Detailed Results")

        for i, r in enumerate(results, 1):
            with st.expander(f"Test Case {i}: {r['question']}", expanded=False):
                st.markdown(f"**Question:** {r['question']}")
                st.markdown(f"**Context:** {r['context']}")
                st.markdown(f"**Generated Answer:** {r['generated_answer']}")
                st.markdown(f"**Ground Truth:** {r['ground_truth']}")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Faithfulness", f"{r['faithfulness']:.3f}")
                c2.metric("Answer Relevancy", f"{r['answer_relevancy']:.3f}")
                c3.metric("Context Relevancy", f"{r['context_relevancy']:.3f}")
                c4.metric("Overall", f"{r['overall_score']:.3f}")

        # Table View
        st.markdown("### Scores Table")
        df = pd.DataFrame(results)[
            ["question", "faithfulness", "answer_relevancy", "context_relevancy", "overall_score"]
        ]
        st.dataframe(df, use_container_width=True)

# ---------- TAB 3: About ----------
with tab3:
    st.subheader("About this Project")
    st.markdown("""
    This is a **RAG Evaluation Mini Project** built for teaching purposes.

    ### What it does:
    1. Uses one LLM to **generate** answers from context (simulates RAG)
    2. Uses another LLM to **judge** the quality of those answers
    3. Calculates the **RAG Triad** metrics:
       - **Faithfulness** → Is the answer grounded in the context?
       - **Answer Relevancy** → Does the answer address the question?
       - **Context Relevancy** → Is the retrieved context relevant?

    ### Tech Stack:
    - Streamlit (UI)
    - OpenAI (Generation + Judge models)
    - Pure Python (no heavy evaluation frameworks)
    """)