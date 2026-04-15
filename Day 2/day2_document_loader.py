from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


# Load PDFs
def load_pdfs(files):
    docs = []
    for f in files:
        loader = PyPDFLoader(f)
        docs.extend(loader.load())
    return docs


# Split into chunks
def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)


# Add metadata
def add_metadata(chunks):
    for c in chunks:
        filename = c.metadata.get("source", "unknown").split("\\")[-1]

        c.metadata["filename"] = filename
        c.metadata["page_number"] = c.metadata.get("page", 0)
        c.metadata["upload_date"] = datetime.now().strftime("%Y-%m-%d")

        if "book" in filename:
            c.metadata["source_type"] = "textbook"
        else:
            c.metadata["source_type"] = "notes"

    return chunks


# Filter function
def filter_chunks(chunks, source_type):
    return [c for c in chunks if c.metadata["source_type"] == source_type]


# MAIN
if __name__ == "__main__":

    files = ["book1.pdf", "notes1.pdf"]

    docs = load_pdfs(files)
    print(f"Loaded documents: {len(docs)}")

    chunks = split_docs(docs)
    print(f"Total chunks: {len(chunks)}")

    chunks = add_metadata(chunks)

    print("\n--- TESTING ---")

    book_chunks = filter_chunks(chunks, "textbook")
    notes_chunks = filter_chunks(chunks, "notes")

    print(f"Book chunks: {len(book_chunks)}")
    print(f"Notes chunks: {len(notes_chunks)}")

    print("\nSample metadata:")
    print(chunks[0].metadata)