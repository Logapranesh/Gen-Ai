from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import os

CHROMA_PATH = "storage/chroma_db"

def get_vector_store():
    os.makedirs(CHROMA_PATH, exist_ok=True)

    embedding = OllamaEmbeddings(model="nomic-embed-text")

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )
    return db


def add_documents(chunks):
    db = get_vector_store()
    db.add_documents(chunks)
    db.persist()