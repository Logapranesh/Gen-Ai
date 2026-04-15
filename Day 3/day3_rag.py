# ==============================
# day3_rag.py (Final Improved)
# ==============================

# ----------- IMPORTS -----------
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

# ----------- STEP 1: CHUNKS -----------
# Improved and diverse chunks

chunks = [
    "Graph theory is used in network security to detect anomalies.",
    "Intrusion Detection Systems monitor network traffic for suspicious activity.",
    "Deep learning models help classify cyber attacks effectively.",
    "RAG stands for Retrieval-Augmented Generation and combines retrieval with text generation.",
    "Vector databases store embeddings for semantic search.",
    "Machine learning is a subset of AI that learns from data.",
    "Chunk size in RAG affects retrieval accuracy and context understanding.",
    "Graph Neural Networks improve intrusion detection accuracy."
]

documents = [Document(page_content=chunk) for chunk in chunks]

# ----------- STEP 2: EMBEDDINGS -----------
print("\nCreating embeddings...")
embedding = OllamaEmbeddings(model="nomic-embed-text")

# ----------- STEP 3: VECTOR STORE -----------
print("Storing data in ChromaDB...")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding,
    persist_directory="./chroma_db"
)

print("Vector DB ready.")

# ----------- STEP 4: RETRIEVER -----------
print("\nCreating semantic retriever...")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("Retriever ready.")

# ----------- STEP 5: LLM -----------
print("\nLoading LLM...")
llm = ChatOllama(model="qwen2.5:1.5b")
print("LLM loaded.")

# ----------- STEP 6: PROMPT TEMPLATE -----------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an AI assistant. Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""
)

# ----------- STEP 7: RAG FUNCTION -----------
def rag_chain(question):
    docs = retriever.invoke(question)

    # Remove duplicate chunks
    unique_docs = []
    seen = set()

    for doc in docs:
        if doc.page_content not in seen:
            unique_docs.append(doc)
            seen.add(doc.page_content)

    # Combine context
    context = "\n".join([doc.page_content for doc in unique_docs])

    # Format prompt
    final_prompt = prompt.format(context=context, question=question)

    # Generate response
    response = llm.invoke(final_prompt)

    return unique_docs, response.content


# ----------- STEP 8: TEST QUESTIONS -----------
print("\nRunning test queries...")

questions = [
    "What is the impact of chunk size in RAG?",
    "How can AI improve cyber threat classification?",
    "What is Retrieval-Augmented Generation (RAG)?"
]

# ----------- STEP 9: EXECUTION -----------
for i, question in enumerate(questions, 1):
    print("\n" + "=" * 50)
    print(f"Question {i}: {question}")

    docs, answer = rag_chain(question)

    print("\nRetrieved Chunks:")
    for doc in docs:
        print("-", doc.page_content)

    print("\nGenerated Answer:")
    print(answer)

print("\nAll tasks completed successfully.")