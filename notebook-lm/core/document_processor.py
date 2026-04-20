from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
import os


def process_pdf(file_path):
    try:
        # 📄 Load PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # ✂️ Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        # 🏷️ Add metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["filename"] = os.path.basename(file_path)
            chunk.metadata["page_number"] = chunk.metadata.get("page", i)
            chunk.metadata["upload_date"] = str(datetime.now())

        return chunks

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []