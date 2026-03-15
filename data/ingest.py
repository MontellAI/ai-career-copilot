"""
Ingest career knowledge base documents into FAISS vector store.

Run this once before starting the app:
    python data/ingest.py
"""

import os
from pathlib import Path
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_BASE_DIR = Path(__file__).parent / "knowledge_base"
FAISS_INDEX_DIR = Path(__file__).parent / "faiss_index"


def ingest():
    print("Loading documents...")
    loader = DirectoryLoader(
        str(KNOWLEDGE_BASE_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and building FAISS index...")
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(chunks, embeddings)

    FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(FAISS_INDEX_DIR))
    print(f"Index saved to {FAISS_INDEX_DIR}")


if __name__ == "__main__":
    ingest()
