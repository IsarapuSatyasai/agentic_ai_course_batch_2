import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from config import LLM_CONFIG   # or define it inline

load_dotenv()

# ---------- Tools ----------
@tool
def add_numbers(a: int, b: int) -> str:
    """Add two numbers together."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def multiply_numbers(a: int, b: int) -> str:
    """Multiply two numbers."""
    return f"The product of {a} and {b} is {a * b}"

@tool
def search_web(query: str) -> str:
    """Search the web for latest information."""
    return f"Search results for '{query}': Latest AI agent trends include LangGraph, multi-agent systems, and production guardrails."

@tool
def explore_dead_letters(queue_name: str) -> str:
    """Explore dead letter messages in a queue."""
    return f"Explored '{queue_name}': Found 12 dead letters (timeouts, invalid cards, insufficient funds). Recommended: retry with backoff + notify users."

# ---------- Agent Logic ----------
def run_agent(query: str):
    llm = ChatOpenAI(**LLM_CONFIG)
    tools = [add_numbers, multiply_numbers, search_web, explore_dead_letters]
    llm_with_tools = llm.bind_tools(tools)

    messages = [HumanMessage(content=query)]
    steps = []

    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        tool_names = [tc["name"] for tc in response.tool_calls]
        steps.append(("tools", f"→ Tools called: {tool_names}"))
        messages.append(response)

        for tool_call in response.tool_calls:
            selected_tool = next(t for t in tools if t.name == tool_call["name"])
            result = selected_tool.invoke(tool_call["args"])
            steps.append(("result", f"{tool_call['name']} Result:\n{result}"))
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

        final = llm_with_tools.invoke(messages)
        steps.append(("final", f"Final Answer:\n{final.content}"))
    else:
        steps.append(("direct", f"Direct Answer:\n{response.content}"))

    return steps

# ---------- Website UI ----------
st.set_page_config(page_title="Tool Management System", page_icon="🛠️", layout="wide")
st.title("Tool Management System with LangChain & OpenAI")

query = st.text_input("Enter your query:", placeholder="Calculate 45 + 78")
sample = st.selectbox("Or pick a sample:", [
    "Calculate 45 + 78",
    "Search for latest AI agent trends",
    "Explore dead letters in payment_queue",
    "What is 12 * 8?"
])

if st.button("Run Agent", type="primary") or query:
    q = query or sample
    with st.spinner("Running agent..."):
        for kind, text in run_agent(q):
            if kind == "tools":
                st.info(text)
            elif kind == "result":
                st.code(text)
            else:
                st.success(text)