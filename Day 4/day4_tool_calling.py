# ----------------------------------------
# Imports
# ----------------------------------------
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os
import json

# Bonus (ReAct)
from langgraph.prebuilt import create_react_agent

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------
load_dotenv()

# ----------------------------------------
# LLM Setup
# ----------------------------------------
llm = ChatOllama(model="llama3.2:3b")

# ----------------------------------------
# Exercise 1 — Tool Definitions
# ----------------------------------------

@tool
def web_search(query: str) -> str:
    """Fetch real-time web results using Tavily"""
    api_key = os.getenv("TAVILY_API_KEY")
    search = TavilySearch(tavily_api_key=api_key)
    result = search.invoke(query)

    if "results" in result:
        return " ".join([r["content"] for r in result["results"][:3]])

    return str(result)


@tool
def summarize(text: str) -> str:
    """Summarize text into a short paragraph"""
    response = llm.invoke(f"Summarize in 2 lines:\n{text}")
    return response.content


@tool
def notes(text: str) -> str:
    """Convert text into notes with title and content"""
    response = llm.invoke(f"Convert into notes with Title and Content:\n{text}")
    return response.content


# ----------------------------------------
# Exercise 1 — Standalone Testing
# ----------------------------------------
def test_tools():
    print("\n--- Testing Tools Standalone ---")

    print("\nWeb Search Test:")
    print(web_search.invoke({"query": "latest AI news"}))

    print("\nSummarize Test:")
    print(summarize.invoke({"text": "AI is transforming industries by automation"}))

    print("\nNotes Test:")
    print(notes.invoke({"text": "AI improves efficiency and decision making"}))


# ----------------------------------------
# Tool Mapping
# ----------------------------------------
TOOLS = {
    "web_search": web_search,
    "summarize": summarize,
    "notes": notes
}

# ----------------------------------------
# JSON Parser
# ----------------------------------------
def safe_json_parse(output):
    try:
        output = output.strip()
        output = output[output.find("{"): output.rfind("}") + 1]
        return json.loads(output)
    except:
        return None


# ----------------------------------------
# Exercise 2 — Manual Agent Loop
# ----------------------------------------
def run_agent(query):
    print("\nUser Query:", query)

    system_prompt = """
You are an AI agent.

Tools:
- web_search(query)
- summarize(text)
- notes(text)

Rules:
- Respond ONLY in JSON
- ALWAYS use args
- After tool result, return final_answer

Format:
{"tool": "tool_name", "args": {"param": "value"}}
{"final_answer": "text"}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    for step in range(6):
        response = llm.invoke(messages)
        output = response.content.strip()

        print("\nLLM Output:", output)

        parsed = safe_json_parse(output)

        if not parsed:
            print("Invalid JSON, retrying...")
            messages.append({"role": "user", "content": "Respond in valid JSON"})
            continue

        # Final Answer
        if "final_answer" in parsed:
            print("\nFinal Answer:", parsed["final_answer"])
            return

        # Tool Selection
        tool_name = parsed.get("tool")
        args = parsed.get("args", {})

        print("Tool Selected:", tool_name)

        # Fix missing args
        if not args:
            if tool_name == "summarize" and "text" in parsed:
                args = {"text": parsed["text"]}
            elif tool_name == "web_search" and "query" in parsed:
                args = {"query": parsed["query"]}

        tool_func = TOOLS.get(tool_name)

        if tool_func:
            result = tool_func.invoke(args)
            print("Tool Result:", result)

            messages.append({"role": "assistant", "content": output})
            messages.append({
                "role": "user",
                "content": f"Tool result:\n{result}\nNow give final_answer in JSON"
            })
        else:
            print("Tool not found")
            return


# ----------------------------------------
# Exercise 4 — ReAct Agent (Bonus)
# ----------------------------------------
def run_react_agent(query):
    print("\n--- ReAct Agent ---")

    tools = [web_search, summarize, notes]
    agent = create_react_agent(llm, tools)

    response = agent.invoke({"messages": [("user", query)]})

    print("ReAct Output:", response)


# ----------------------------------------
# Exercise 3 — Test Queries
# ----------------------------------------
if __name__ == "__main__":

    # Exercise 1
    test_tools()

    # Exercise 3
    run_agent("What is the latest news on OpenAI?")

    run_agent("Summarize this paragraph: Artificial Intelligence is transforming industries by automating tasks and improving efficiency.")

    run_agent("Find the latest news on AI agents and summarize it")

    # Exercise 4 (Bonus)
    run_react_agent("Find latest news on AI agents and summarize it")