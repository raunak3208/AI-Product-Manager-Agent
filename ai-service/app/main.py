from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_graph

app = FastAPI()
graph = build_graph()

class RunRequest(BaseModel):
    idea: str
    features: str

@app.post("/runs")
def start_run(request: RunRequest):
    initial_state = {
        "idea": request.idea,
        "features": request.features,
        "revision_count": 0,
    }
    result = graph.invoke(initial_state)
    return result