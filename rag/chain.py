from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from rag.retriever import get_retriever
from rag.prompts import CAREER_ADVICE_PROMPT, ROADMAP_PROMPT
import os


class CareerCopilotChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.retriever = get_retriever()

    def run(self, user_profile: dict) -> dict:
        """
        Run the full RAG pipeline for a given user profile.
        Returns career advice, roadmap, and source documents.
        """
        query = self._build_query(user_profile)

        # Retrieve relevant context
        docs = self.retriever.get_relevant_documents(query)

        # Build augmented context
        context = "\n\n".join([doc.page_content for doc in docs])

        # Generate career advice
        advice_prompt = CAREER_ADVICE_PROMPT.format(
            context=context,
            goal=user_profile["goal"],
            experience=user_profile["experience"],
            skills=user_profile["skills"],
            interests=user_profile["interests"]
        )
        career_advice = self.llm.predict(advice_prompt)

        # Generate roadmap
        roadmap_prompt = ROADMAP_PROMPT.format(
            context=context,
            goal=user_profile["goal"],
            skills=user_profile["skills"]
        )
        roadmap = self.llm.predict(roadmap_prompt)

        return {
            "career_advice": career_advice,
            "roadmap": roadmap,
            "source_documents": docs
        }

    def _build_query(self, profile: dict) -> str:
        return (
            f"Career path for someone targeting {profile['goal']} "
            f"with {profile['experience']} experience, "
            f"skills in {profile['skills']}, "
            f"interested in {profile['interests']}"
        )
