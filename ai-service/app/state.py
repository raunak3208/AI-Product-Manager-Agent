from typing import TypedDict

class PMState(TypedDict):
    idea: str
    features: str
    research: str
    prd: str
    critic_feedback: str
    critic_score: float
    revision_count: int