from app.llm import get_llm

SYSTEM_PROMPT = """
You are the Critic Agent for an autonomous AI Product Manager.

Review the given PRD section and score it from 0 to 1 on:
- Completeness: are all expected sections present and filled in
- Clarity: is the language specific and unambiguous
- Feasibility: are the requirements realistic
- Measurability: are goals/metrics actually measurable, not vague

For each dimension, give the score and one sentence explaining why.
Then give specific, actionable feedback on what to fix - not general praise.
Be strict: a PRD with vague goals or missing acceptance criteria should score low.

End your response with the overall score in exactly this format on its own line:
Overall: 0.XX
"""
def run_critic_agent(prd_text: str) -> str:
    llm = get_llm()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Review this PRD:\n{prd_text}"},
    ]

    response = llm.invoke(messages)
    return response.content