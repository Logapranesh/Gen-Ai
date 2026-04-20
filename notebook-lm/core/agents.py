from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.llms import Ollama

def create_agent(rag_chain, enable_web):

    tools = []

    tools.append(
        Tool(
            name="Document Search",
            func=rag_chain.run,
            description="Search in uploaded PDFs"
        )
    )

    if enable_web:
        search = TavilySearchAPIWrapper()
        tools.append(
            Tool(
                name="Web Search",
                func=search.run,
                description="Search the internet"
            )
        )

    llm = Ollama(model="llama3.2:3b")

    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True
    )

    return agent