import os
from langchain.vectorstores import FAISS, Pinecone
from langchain.embeddings import OpenAIEmbeddings
import pinecone


def get_retriever(use_pinecone: bool = False):
    """
    Returns a retriever backed by either FAISS (local) or Pinecone (hosted).
    Defaults to FAISS for local development.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    if use_pinecone:
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV")
        )
        vectorstore = Pinecone.from_existing_index(
            index_name="career-copilot",
            embedding=embeddings
        )
    else:
        # Load local FAISS index (built during ingestion)
        index_path = os.path.join(os.path.dirname(__file__), "../data/faiss_index")
        vectorstore = FAISS.load_local(index_path, embeddings)

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
