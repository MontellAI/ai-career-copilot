from typing import Dict

# Skill requirements by role (simplified scoring)
ROLE_SKILL_REQUIREMENTS = {
    "AI/ML Engineer": {
        "Python": 90,
        "LangChain / LLMs": 80,
        "RAG Systems": 75,
        "Vector Databases": 70,
        "AWS / Cloud": 65,
        "AI Agents": 60,
    },
    "LLM Engineer": {
        "Python": 90,
        "LangChain / LLMs": 90,
        "RAG Systems": 85,
        "Fine-Tuning": 70,
        "Vector Databases": 75,
        "Prompt Engineering": 80,
    },
    "ML Engineer": {
        "Python": 90,
        "PyTorch / TensorFlow": 85,
        "MLOps": 75,
        "AWS / Cloud": 70,
        "Data Engineering": 65,
        "Model Evaluation": 70,
    }
}

# Rough keyword-to-skill mapping for parsing free-text input
SKILL_KEYWORDS = {
    "Python": ["python", "py"],
    "LangChain / LLMs": ["langchain", "llm", "openai", "gpt", "llms"],
    "RAG Systems": ["rag", "retrieval", "retrieval-augmented"],
    "Vector Databases": ["faiss", "pinecone", "chroma", "vector db", "vector database"],
    "AWS / Cloud": ["aws", "gcp", "azure", "cloud", "ec2", "lambda"],
    "AI Agents": ["agents", "agent", "agentic", "tool use", "function calling"],
    "Fine-Tuning": ["fine-tuning", "lora", "peft", "finetuning", "qlora"],
    "Prompt Engineering": ["prompt", "prompting", "chain of thought", "cot"],
    "Data Engineering": ["etl", "pipeline", "spark", "airflow", "dbt"],
}


class SkillAnalyzer:
    def analyze(self, current_skills_text: str, target_role: str) -> Dict[str, int]:
        """
        Scores current skills against target role requirements.
        Returns a dict of skill -> estimated proficiency (0-100).
        """
        skills_lower = current_skills_text.lower()

        # Determine which role template to use
        role_key = self._match_role(target_role)
        requirements = ROLE_SKILL_REQUIREMENTS.get(role_key, ROLE_SKILL_REQUIREMENTS["AI/ML Engineer"])

        scores = {}
        for skill, required_level in requirements.items():
            keywords = SKILL_KEYWORDS.get(skill, [skill.lower()])
            mentioned = any(kw in skills_lower for kw in keywords)

            if mentioned:
                # Give partial credit — they have it, but gap from required
                scores[skill] = min(required_level, 75 + (required_level - 75) // 2)
            else:
                scores[skill] = max(10, required_level - 50)

        return scores

    def _match_role(self, role_text: str) -> str:
        role_lower = role_text.lower()
        if "llm" in role_lower:
            return "LLM Engineer"
        if "ml" in role_lower or "machine learning" in role_lower:
            return "ML Engineer"
        return "AI/ML Engineer"
