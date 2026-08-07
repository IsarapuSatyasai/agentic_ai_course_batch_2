# evaluation.py
from openai import OpenAI
from config import OPENAI_API_KEY, GENERATION_MODEL, JUDGE_MODEL, TEMPERATURE, MAX_TOKENS
import json

client = OpenAI(api_key=OPENAI_API_KEY)

# ====================== GOLDEN DATASET ======================
GOLDEN_DATASET = [
    {
        "question": "What is Graph RAG?",
        "context": "Graph RAG combines knowledge graphs with vector search. It enables multi-hop reasoning by connecting related entities across documents.",
        "ground_truth": "Graph RAG is a technique that combines knowledge graphs with vector search to enable multi-hop reasoning."
    },
    {
        "question": "When should we use Hybrid Search?",
        "context": "Hybrid search combines vector embeddings and BM25 keyword search. It is useful when both semantic similarity and exact keyword matching are needed.",
        "ground_truth": "Hybrid search should be used when we need both semantic similarity and keyword precision."
    },
    {
        "question": "What are the benefits of reranking?",
        "context": "Reranking uses stronger cross-encoder models to re-score the top retrieved documents. This significantly improves the quality of final results.",
        "ground_truth": "Reranking improves the quality of top-k results using more powerful cross-encoder models."
    }
]


# ====================== GENERATION LLM ======================
def generate_answer(question: str, context: str, model: str = GENERATION_MODEL, temperature: float = TEMPERATURE) -> str:
    """Generate answer using context (simulates RAG generation)"""
    
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the provided context.
If the context does not contain enough information, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=MAX_TOKENS
    )
    return response.choices[0].message.content.strip()


# ====================== JUDGE LLM (RAG TRIAD) ======================
def judge_faithfulness(question: str,
                       answer: str,
                       context: str,
                       model: str = JUDGE_MODEL) -> float:
    
    """Score how faithful the answer is to the context (0 to 1)"""
    
    prompt = f"""You are an expert evaluator. Score the faithfulness of the answer based on the context.
    
    Faithfulness means: Does the answer only contain information that can be found in the context? (No hallucinations)
    
    Question: {question}
    Context: {context}
    Answer: {answer}
    
    Return ONLY a number between 0 and 1.
    - 1.0 = Fully faithful
    - 0.0 = Completely hallucinated
    
    Score:"""

    response = client.chat.completions.create(
             model=model,
             messages=[{'role': 'user', 'content': prompt}],
             temperature=0.0,
             max_tokens = 10
    )
    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.5
         

def judge_answer_relevancy(question: str, answer: str, model: str = JUDGE_MODEL) -> float:
    """Score how relevant the answer is to the question (0 to 1)"""
    
    prompt = f"""You are an expert evaluator. Score how relevant the answer is to the question.

Question: {question}
Answer: {answer}

Return ONLY a number between 0 and 1.
- 1.0 = Perfectly answers the question
- 0.0 = Completely irrelevant

Score:"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=10
    )
    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.5


def judge_context_relevancy(question: str, context: str, model: str = JUDGE_MODEL) -> float:
    """Score how relevant the context is to the question (0 to 1)"""
    
    prompt = f"""You are an expert evaluator. Score how relevant the retrieved context is to the question.

Question: {question}
Context: {context}

Return ONLY a number between 0 and 1.
- 1.0 = Context is highly relevant
- 0.0 = Context is completely irrelevant

Score:"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=10
    )
    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.5


# ====================== MAIN EVALUATION FUNCTION ======================
def run_full_evaluation(generation_model: str, judge_model: str, temperature: float):
    """Run complete RAG evaluation on the golden dataset"""
    
    results = []

    for item in GOLDEN_DATASET:
        question = item["question"]
        context = item["context"]
        ground_truth = item["ground_truth"]

        # 1. Generate Answer
        generated_answer = generate_answer(
            question=question,
            context=context,
            model=generation_model,
            temperature=temperature
        )

        # 2. Judge the Answer (RAG Triad)
        faithfulness = judge_faithfulness(question, generated_answer, context, judge_model)
        answer_relevancy = judge_answer_relevancy(question, generated_answer, judge_model)
        context_relevancy = judge_context_relevancy(question, context, judge_model)

        overall = (faithfulness + answer_relevancy + context_relevancy) / 3

        results.append({
            "question": question,
            "context": context,
            "ground_truth": ground_truth,
            "generated_answer": generated_answer,
            "faithfulness": round(faithfulness, 3),
            "answer_relevancy": round(answer_relevancy, 3),
            "context_relevancy": round(context_relevancy, 3),
            "overall_score": round(overall, 3)
        })

    return results