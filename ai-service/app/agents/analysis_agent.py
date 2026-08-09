from app.llm import get_llm

SYSTEM_PROMPT = """
You are the Analysis Agent for an autonomous AI Product Manager.

Given a list of features, score each on:
- Reach (1-10): how many users this affects
- Impact (1-10): how much it helps them
- Confidence (1-10): how sure you are about the above
- Effort (1-10): how much work to build (higher = more effort)

RICE Score = (Reach * Impact * Confidence) / Effort

For each feature, briefly justify the scores in one line before showing the numbers.
Return a table with columns: Feature, Reach, Impact, Confidence, Effort, RICE Score.
Sort the table by RICE Score, highest first.
After the table, list the top 3 features as the recommended MVP set.
"""

def run_analysis_agent(features: list[str]) -> str:
    llm = get_llm()

    feature_list = "\n".join(f"- {f}" for f in features)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Score these features:\n{feature_list}"},
    ]

    response = llm.invoke(messages)
    return response.content