import os
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ====================== CONFIG ======================
HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Two Models: One from HF, One from OpenAI
models = {
    "qwen-2.5-7b": {
        "provider": "hf",
        "model_id": "Qwen/Qwen2.5-7B-Instruct"
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "model_id": "gpt-4o-mini"
    }
}

tasks = [
    {
        "category": "Reasoning",
        "prompt": "If a plane crashes on the border of India and Pakistan, where do you bury the survivors?"
    },
    {
        "category": "Coding",
        "prompt": "Write a modular Python class for a database connection using the singleton pattern."
    },
    {
        "category": "Agentic Theory",
        "prompt": "Explain the difference between a Zero-Shot Agent and a ReAct Agent in one paragraph."
    }
]

def run_inference(prompt, model_key):
    model_info = models[model_key]
    start_time = time.time()
    
    try:
        if model_info["provider"] == "hf":
            from huggingface_hub import InferenceClient
            client = InferenceClient(token=HF_TOKEN, timeout=180)
            response = client.chat.completions.create(
                model=model_info["model_id"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
        else:  # openai
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=model_info["model_id"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
        
        latency = time.time() - start_time
        output = response.choices[0].message.content.strip()
        tps = len(output.split()) / latency if latency > 0 else 0
        
        return {
            "model": model_key,
            "latency": round(latency, 2),
            "tps": round(tps, 2),
            "response_preview": output[:150] + "..." if len(output) > 150 else output,
            "status": "success"
        }
    except Exception as e:
        return {
            "model": model_key,
            "status": "failed",
            "error": str(e)[:120]
        }


eval_results = []

print("Evaluation Tasks Loaded")
for i, task in enumerate(tasks, 1):
    print(f"Task {i} [{task['category']}]: {task['prompt']}")
print("-" * 40)

for task in tasks:
    print(f"\nEvaluating Category: {task['category']}")
    for m_key in models.keys():
        print(f"[{m_key}] ", end="")
        result = run_inference(task['prompt'], m_key)
        
        if result["status"] == "success":
            print("Success")
            print(f"Response: {result['response_preview']}")
            score = input(f"Rate {m_key} quality (1-10): ") or "7"
            result["quality_score"] = int(score)
            result["category"] = task["category"]
            eval_results.append(result)
        else:
            print("Error")

# Final Summary
df = pd.DataFrame(eval_results)

if not df.empty:
    summary = df.groupby("model").agg({
        "latency": "mean",
        "tps": "mean",
        "quality_score": "mean"
    }).round(2)
    
    print("\nFINAL BENCHMARK SUMMARY")
    print(summary)
    
    df.to_csv("llm_benchmark_hf_openai.csv", index=False)
    print("Results saved to llm_benchmark_hf_openai.csv")