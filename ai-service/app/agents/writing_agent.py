from app.llm import get_llm

SYSTEM_PROMPT = """
You are the Writing Agent for an autonomous AI Product Manager.

Given research findings and a prioritized feature list, write a PRD section with these headings:
- Problem Statement (2-3 sentences, grounded in the research given)
- Goals and Success Metrics (2-4 measurable goals, not vague statements)
- Feature Requirements (for each feature: a short description, why it matters, and one key acceptance criterion)

Only use information from the research and features given to you - do not invent competitors,
statistics, or user needs that weren't provided.
Write in clear, plain language. No fluff or filler sentences.
"""
def run_writing_agent(research: str, features: str) -> str:
    llm = get_llm()

    user_content = f"Research:\n{research}\n\nFeatures:\n{features}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    response = llm.invoke(messages)
    return response.content