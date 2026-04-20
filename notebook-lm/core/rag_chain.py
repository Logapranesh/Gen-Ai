from langchain_ollama import OllamaLLM
from core.vector_store import get_vector_store

def ask_rag(question):
    db = get_vector_store()

    results = db.similarity_search(question, k=4)

    if not results:
        return "No relevant information found in the document."

    context = "\n\n".join([doc.page_content for doc in results])

    llm = OllamaLLM(model="llama3.2:3b")

    prompt = f"""
You are an AI assistant. Answer ONLY using the given context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    # Sources
    sources = []
    for doc in results:
        meta = doc.metadata
        sources.append(f"{meta.get('filename')} - Page {meta.get('page_number')}")

    return response + "\n\nSources:\n" + "\n".join(set(sources))