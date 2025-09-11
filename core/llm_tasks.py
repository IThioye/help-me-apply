# core/llm_tasks.py
import json
from core.llm_interface import LLMInterface

# Global cache so we only init once
_llm_instance = None

def get_llm(language="en", model="llama2"):
    """
    Load LLMInterface once and reuse it.
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMInterface(model=model, language=language)
    return _llm_instance


class AnalyzerRecommender:
    def __init__(self, llm):
        self.llm = llm

    def run(self, cv_data: dict, job_text: str) -> str:
        user_msg = (
            f"CV:\n{json.dumps(cv_data, indent=2)}\n\n"
            f"JOB OFFER:\n{job_text}\n\n"
            "### Analyze the match and suggest actionable recommendations."
        )
        return self.llm.run(task="analyzer", user_message=user_msg)


class Generator:
    def __init__(self, llm):
        self.llm = llm

    def rewrite_profile(self, profile: str, recommendations: str):
        return self.llm.run(
            task="generator",
            user_message=f"PROFILE:\n{profile}\n\nRECOMMENDATIONS:\n{recommendations}"
        )

    def rewrite_experience(self, exp: dict, recommendations: str):
        return self.llm.run(
            task="generator",
            user_message=f"EXPERIENCE:\n{exp}\n\nRECOMMENDATIONS:\n{recommendations}"
        )

    def rewrite_education(self, edu: dict, recommendations: str):
        return self.llm.run(
            task="generator",
            user_message=f"EDUCATION:\n{edu}\n\nRECOMMENDATIONS:\n{recommendations}"
        )

    def rewrite_skills(self, skills: str, recommendations: str):
        return self.llm.run(
            task="generator",
            user_message=f"SKILLS:\n{skills}\n\nRECOMMENDATIONS:\n{recommendations}"
        )
