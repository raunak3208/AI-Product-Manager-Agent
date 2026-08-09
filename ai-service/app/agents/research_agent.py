from langchain_core.tools import tool
from tavily import TavilyClient
from app.llm import get_llm
from app.config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

SYSTEM_PROMPT = """
You are the Research Agent for an autonomous AI Product Manager.

Given a product idea, do the following:
1. Find at least 5 existing competitors or similar solutions.
2. Identify user pain points from reddit threads and discussions.
3. Note any recent market trends relevant to this space (last 6 months if possible).
4. Roughly estimate market size or growth if data is available.

Use the web_search and reddit_search tools as many times as needed to gather this.
Do not guess or make up information - only report what the tools return.

Structure your final answer with these headings:
- Competitors
- User Pain Points
- Market Trends
- Sources

Always list the source URL next to each claim.
"""

@tool
def web_search(query: str) -> str:
    """Search the web for a query and return top results."""
    results = tavily.search(query=query, max_results=5)
    return str(results["results"])

@tool
def reddit_search(query: str) -> str:
    """Search reddit discussions for a query."""
    results = tavily.search(query=f"site:reddit.com {query}", max_results=5)
    return str(results["results"])

TOOLS = [web_search, reddit_search]
TOOLS_MAP = {t.name: t for t in TOOLS}

def run_research_agent(product_idea: str) -> str:
    llm = get_llm().bind_tools(TOOLS)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": product_idea},
    ]

    response = llm.invoke(messages)
    messages.append(response)

    # if model asked to call tools, run them and feed results back
    while response.tool_calls:
        for call in response.tool_calls:
            tool_fn = TOOLS_MAP[call["name"]]
            result = tool_fn.invoke(call["args"])
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_call_id": call["id"],
            })
        response = llm.invoke(messages)
        messages.append(response)

    return response.content