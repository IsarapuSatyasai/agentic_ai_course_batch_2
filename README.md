# Production-Grade Agentic AI Engineer Course

## 🚀 Project Overview
**Ayaanex Technologies** presents the **Production-Grade Agentic AI Engineer (9-Week Intensive)** — a fast-paced, hands-on course designed to take learners from foundational Python skills to production-level AI engineering expertise.

The primary aim is to transform participants into capable **Agentic AI Engineers** who can confidently **design, build, and deploy** reliable, production-grade agentic AI systems. Starting from core programming foundations and progressing through advanced RAG pipelines, single and multi-agent orchestration, memory engineering, guardrails, and deployment, this program covers the complete journey needed to create real-world agentic solutions.

Whether you are an automation testing engineer, Python developer, or AI enthusiast, by the end of these 9 weeks you will have the skills to build intelligent, observable, and trustworthy agentic systems ready for professional or portfolio use.

It compresses essential industry knowledge into a practical 9-week format, merging foundational topics with high-impact agentic skills and culminating in **one integrated capstone project** that combines RAG pipelines, multi-agent orchestration, guardrails, and deployment.

---

## 🛠️ Tools & Technologies

### Core Programming & Engineering
- **Python** (async/await, decorators, *args/**kwargs, type hints, generators, concurrency)
- **FastAPI** (REST APIs, async endpoints, error handling)
- **Pydantic** (data validation, settings, tool/function schemas)
- **asyncio**

### AI Frameworks
- **LangChain** & **LangGraph** (chains, agents, multi-agent workflows, state management)

### Retrieval & Vector
- Embeddings models
- Vector databases (Chroma, FAISS, Pinecone)
- Hybrid retrieval (vector + BM25 + graph)
- Reranking & context optimization

### Production & Reliability
- **Guardrails** (input/output/action safety, prompt injection defense, PII redaction)
- **Observability**: LangSmith
- **Deployment**: Docker, FastAPI + Streamlit, local/cloud hosting (Vercel/AWS adaptable)
- Git, Jupyter Notebooks

---

## 📈 9-Week Course Structure & Milestones

### Week 1: Python + Async Foundations
**Focus:** Build strong Python engineering skills essential for agent frameworks.  
**Key Topics:** Core Python (variables, control flow, functions, *args/**kwargs, decorators, comprehensions, generators, type hints), asyncio, concurrent tasks, timeouts, FastAPI basics, parallel LLM calls with error handling.  
**Assignment:** Build an async FastAPI endpoint that calls multiple LLMs in parallel, times out slow responses, and returns results without blocking.  
**End State:** Solid foundation so later agent code doesn’t break mysteriously.

### Week 2: LLM Mental Model + Prompt Engineering Basics
**Focus:** Understand LLMs deeply and move from casual prompting to engineering.  
**Key Topics:** LLM fundamentals (knowledge cutoffs, probabilistic generation, hallucinations), system prompts, few-shot, Chain-of-Thought, caching for cost optimization.  
**Assignment:** Create reliable, cost-optimized prompts and explain LLM behavior to non-technical stakeholders.  
**End State:** Systematic prompt improvement and API control.

### Week 3: Ingestion Pipeline + Basic RAG
**Focus:** Connect private data to LLMs.  
**Key Topics:** Document loading, chunking strategies (fixed-size, semantic, parent-child), embeddings, vector stores (Chroma), naive RAG pipeline, PDF/text ingestion.  
**Assignment:** Build a simple PDF-based RAG chatbot.  
**End State:** Functional retrieval-augmented system.

### Week 4: Advanced RAG + Evaluation
**Focus:** Make RAG production-viable.  
**Key Topics:** Hybrid retrieval (vector + BM25 + graph), reranking, context management, RAG Triad, Precision/Recall, faithfulness metrics, golden datasets, failure modes.  
**Assignment:** Improve RAG system with measurable performance gains and evaluation harness.  
**End State:** Ability to measure and fix RAG issues with data, not intuition.

### Week 5: Tools, Function Calling & Single Agents
**Focus:** Give agents real capabilities.  
**Key Topics:** Tool schemas (Pydantic/JSON Schema), function calling, ReAct pattern, error handling, integrating external tools (web search, databases, custom functions).  
**Assignment:** Build a single agent that uses multiple tools reliably and gracefully handles failures.  
**End State:** Agents that can act in the world, not just chat.

### Week 6: Memory & Context Engineering
**Focus:** Solve “forgetting” and context problems.  
**Key Topics:** Short-term vs long-term memory, context window management, token budgeting, lost-in-the-middle, recency bias, conversation summarization.  
**Assignment:** Implement memory patterns so agents maintain coherent long conversations.  
**End State:** High-leverage skill for reliable agent behavior.

### Week 7: Multi-Agent Orchestration
**Focus:** Scale to complex workflows.  
**Key Topics:** When (and when not) to use multi-agent systems, LangGraph workflows, planner-executor patterns, conditional routing, state management, specialized agent roles (e.g., NL-to-SQL or analysis workflows).  
**Assignment:** Build a multi-agent system with orchestration and retry logic.  
**End State:** Design and implement collaborative agent teams.

### Week 8: Guardrails + LLMOps
**Focus:** Production safety and observability.  
**Key Topics:** Three-layer guardrails (Input deterministic, Output LLM-judge, Action tool-level), prompt injection defense, PII redaction, faithfulness checks, LangSmith observability, evaluation harnesses, monitoring.  
**Assignment:** Add comprehensive guardrails and monitoring to previous agents.  
**End State:** Ship agents with confidence and measurable reliability.

### Week 9: Capstone Project
**Focus:** Integrate everything into one production-grade system.  
**Project:** **Intelligent Enterprise Knowledge Assistant**  
- Document ingestion (PDFs, semantic chunking, hybrid retrieval)  
- Multi-agent orchestration (Planner, Retriever, Validator, Explainer/Analyzer)  
- Guardrails (input/output/action) + faithfulness with citations  
- Evaluation harness + observability  
- FastAPI backend + simple chat UI  
- Basic deployment + README for portfolio  

**Domains:** Company policy Q&A, document analytics, or domain-specific (e.g., testing/automation reports).  
**Outcomes:** Complete working system, live demo, presentation, and portfolio-ready repository.

---

## 🎯 Key Learning Outcomes
By the end of the course, students will be able to:

- Design, build, evaluate, and deploy reliable **multi-agent RAG systems**
- Master advanced Python engineering patterns required for agent frameworks
- Build production-grade RAG pipelines with hybrid retrieval, reranking, and evaluation
- Orchestrate single and multi-agent systems using LangGraph
- Implement memory systems and context engineering for long-running agents
- Add robust **guardrails** and **observability** (LangSmith)
- Deploy agentic systems with FastAPI, Docker, and simple UIs
- Deliver a complete, portfolio-ready production system

---

## 📚 Additional Course Elements
- **Teaching Style:** Hands-on with Jupyter notebooks, live coding demos, student-friendly explanations, and real project focus
- **Weekly Resources:** Notebooks, code templates, reading lists, assignment rubrics
- **Assessment:** Weekly assignments + capstone milestones + final presentation
- **Out-of-Scope:** Fine-tuning, voice agents, deep ML math (focus remains on prompt/tool/RAG/agent engineering)
- **Certification:** Completion certificate + portfolio project

---

## Prerequisites
- Basic Python (variables, control flow, functions, lists/dicts, basic OOP)
- Python 3.10+ environment + pip
- Git basics (recommended)
- LLM API access (OpenAI / Groq / Anthropic / Gemini)
- Willingness to commit 8–12 hours/week
