import os
import uuid
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field

from configs.settings import settings
from src.agent.pipeline import HiverSupportAgent
from src.agent.schemas import AgentRunRequest, AgentResult
from src.evaluation.harness import EvaluationHarness
from src.retrieval.index import FAISSIndexStore
from src.retrieval.retriever import CaseRetriever

app = FastAPI(
    title="HiverSupport Agent API",
    version="1.0.0",
    description="Evidence-Grounded Customer Support Agent API"
)

# In-memory storage for agent runs, evaluations, and experiments
agent_runs_db: Dict[str, AgentResult] = {}
evaluations_db: Dict[str, Dict[str, Any]] = {}
experiments_db: Dict[str, Dict[str, Any]] = {}

# Lazy loaded agent instance
_agent_instance: Optional[HiverSupportAgent] = None

def get_agent() -> HiverSupportAgent:
    global _agent_instance
    if _agent_instance is None:
        store = FAISSIndexStore()
        if not store.load() or store.index.ntotal == 0:
            from src.data.loader import load_dataset
            from src.data.cleaner import preprocess_dataset
            from src.data.conversation_builder import reconstruct_conversations
            from src.retrieval.case_builder import build_historical_cases
            
            raw_df = load_dataset()
            clean_df = preprocess_dataset(raw_df)
            convs = reconstruct_conversations(clean_df)
            cases = build_historical_cases(convs)
            store.build_index(cases)
            store.save()
            
        retriever = CaseRetriever(store)
        _agent_instance = HiverSupportAgent(retriever=retriever)
    return _agent_instance

# Request/Response Models
class ExperimentCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    dataset_version: str = "v1"
    intent_taxonomy_version: str = "v1"
    golden_set_version: str = "v1"
    config: Dict[str, Any] = Field(default_factory=dict)

class EvaluationRunRequest(BaseModel):
    experiment_id: Optional[str] = None
    golden_set_version: str = "v1"
    system_name: str = "hiver-support-agent"

# Endpoints
@app.get("/api/v1/health")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "hiver-support-agent",
        "version": "1.0.0",
        "mode": settings.APP_MODE
    }


@app.get("/api/v1/brands")
def list_brands():
    return {
        "items": [
            {
                "brand_id": "brand_001",
                "brand_name": settings.SELECTED_BRAND,
                "is_active": True
            }
        ],
        "count": 1
    }

@app.get("/api/v1/brands/{brand_id}")
def get_brand(brand_id: str):
    if brand_id in ["brand_001", settings.SELECTED_BRAND, "AppleSupport"]:
        return {
            "brand_id": "brand_001",
            "brand_name": settings.SELECTED_BRAND,
            "is_active": True
        }
    raise HTTPException(status_code=404, detail=f"Brand '{brand_id}' not found.")

@app.post("/api/v1/conversations/analyze", response_model=AgentResult)
def analyze_conversation(request: AgentRunRequest):
    if not request.customer_message or not request.customer_message.strip():
        raise HTTPException(status_code=400, detail="customer_message must not be empty.")

    agent = get_agent()
    result = agent.process_conversation(
        customer_message=request.customer_message,
        conversation_id=request.conversation_id,
        brand=request.brand_id
    )

    agent_runs_db[result.run_id] = result
    return result

@app.get("/api/v1/agent-runs/{run_id}", response_model=AgentResult)
def get_agent_run(run_id: str):
    if run_id not in agent_runs_db:
        raise HTTPException(status_code=404, detail=f"Agent run '{run_id}' not found.")
    return agent_runs_db[run_id]

@app.get("/api/v1/agent-runs/{run_id}/evidence")
def get_agent_run_evidence(run_id: str):
    if run_id not in agent_runs_db:
        raise HTTPException(status_code=404, detail=f"Agent run '{run_id}' not found.")
    
    run = agent_runs_db[run_id]
    return {
        "run_id": run_id,
        "items": [c.model_dump() for c in run.retrieved_cases],
        "evidence_sufficient": run.evidence.sufficient
    }

@app.post("/api/v1/evaluations/run")
def run_evaluation(request: EvaluationRunRequest, background_tasks: BackgroundTasks):
    eval_id = f"eval_{uuid.uuid4().hex[:8]}"
    
    evaluations_db[eval_id] = {
        "evaluation_run_id": eval_id,
        "status": "running",
        "system_name": request.system_name,
        "golden_set_version": request.golden_set_version,
        "metrics": None
    }

    def execute_eval():
        try:
            harness = EvaluationHarness()
            report = harness.run_evaluation(run_judge=False)
            evaluations_db[eval_id]["status"] = "completed"
            evaluations_db[eval_id]["metrics"] = report
        except Exception as e:
            evaluations_db[eval_id]["status"] = "failed"
            evaluations_db[eval_id]["error"] = str(e)

    background_tasks.add_task(execute_eval)

    return {
        "evaluation_run_id": eval_id,
        "status": "accepted",
        "message": "Evaluation job launched in background."
    }

@app.get("/api/v1/evaluations/{run_id}")
def get_evaluation(run_id: str):
    if run_id not in evaluations_db:
        raise HTTPException(status_code=404, detail=f"Evaluation run '{run_id}' not found.")
    return evaluations_db[run_id]

@app.get("/api/v1/experiments")
def list_experiments():
    return {
        "items": list(experiments_db.values()),
        "count": len(experiments_db)
    }

@app.post("/api/v1/experiments")
def create_experiment(request: ExperimentCreateRequest):
    exp_id = f"exp_{uuid.uuid4().hex[:8]}"
    record = {
        "experiment_id": exp_id,
        "name": request.name,
        "description": request.description,
        "dataset_version": request.dataset_version,
        "intent_taxonomy_version": request.intent_taxonomy_version,
        "golden_set_version": request.golden_set_version,
        "config": request.config
    }
    experiments_db[exp_id] = record
    return record

@app.get("/api/v1/experiments/{experiment_id}")
def get_experiment(experiment_id: str):
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment_id}' not found.")
    return experiments_db[experiment_id]

# Mount UI static files if directory exists
UI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "static")
if os.path.exists(UI_DIR):
    app.mount("/static", StaticFiles(directory=UI_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    html_path = os.path.join(UI_DIR, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return HTMLResponse("<h2>HiverSupport Agent API is running. UI loading...</h2>")
