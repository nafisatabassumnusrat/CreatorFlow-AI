import os
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from backend.config import BASE_DIR, MEDIA_DIR, HOST, PORT
from backend.models.schemas import (
    VideoCreateRequest,
    CreatorState,
    HumanApprovalRequest,
    DashboardMetrics,
)
from backend.models.enums import PipelineStage, StageStatus
from backend.services.storage import storage
from backend.services.orchestrator import orchestrator

app = FastAPI(
    title="CreatorFlow AI API",
    description="Autonomous YouTube Production Studio API",
    version="1.0.0"
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# REST Endpoints
# -------------------------------------------------------------

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics():
    return storage.get_metrics()

@app.get("/api/videos", response_model=list[CreatorState])
async def list_videos():
    return storage.list_all()

@app.post("/api/videos/create", response_model=CreatorState)
async def create_video(request: VideoCreateRequest, background_tasks: BackgroundTasks):
    project_id = f"proj-{uuid.uuid4().hex[:8]}"
    state = CreatorState(
        project_id=project_id,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
        niche=request.niche,
        topic=request.topic,
        target_audience=request.target_audience,
        language=request.language,
        duration=request.duration,
        style=request.style,
        voice=request.voice,
        reference_channel=request.reference_channel or "",
        brand_info=request.brand_info or "",
        current_stage=PipelineStage.IDLE,
        stage_statuses={
            "strategy": StageStatus.PENDING,
            "titles": StageStatus.PENDING,
            "hook": StageStatus.PENDING,
            "script": StageStatus.PENDING,
            "approval_script": StageStatus.PENDING,
            "storyboard": StageStatus.PENDING,
            "voice": StageStatus.PENDING,
            "visuals": StageStatus.PENDING,
            "thumbnail": StageStatus.PENDING,
            "seo": StageStatus.PENDING,
            "quality_check": StageStatus.PENDING,
            "approval_production": StageStatus.PENDING,
            "rendering": StageStatus.PENDING,
        }
    )
    storage.save(state)
    orchestrator._log_action(state, "System", f"Initialized project for '{request.topic}'")
    return state

@app.post("/api/videos/demo", response_model=CreatorState)
async def create_demo_video():
    state = await orchestrator.seed_demo()
    return state

@app.get("/api/videos/{project_id}", response_model=CreatorState)
async def get_video(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return state

@app.delete("/api/videos/{project_id}")
async def delete_video(project_id: str):
    success = storage.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "deleted", "project_id": project_id}

# Pipeline Stage Triggers
@app.post("/api/videos/{project_id}/strategy", response_model=CreatorState)
async def trigger_strategy(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.analyze_content(state)

@app.post("/api/videos/{project_id}/titles", response_model=CreatorState)
async def trigger_titles(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.generate_titles(state)

@app.post("/api/videos/{project_id}/hook", response_model=CreatorState)
async def trigger_hook(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.generate_hook(state)

@app.post("/api/videos/{project_id}/script", response_model=CreatorState)
async def trigger_script(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.generate_script(state)

@app.post("/api/videos/{project_id}/storyboard", response_model=CreatorState)
async def trigger_storyboard(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.create_storyboard(state)

@app.post("/api/videos/{project_id}/voice", response_model=CreatorState)
async def trigger_voice(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.generate_voice(state)

@app.post("/api/videos/{project_id}/visuals", response_model=CreatorState)
async def trigger_visuals(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    state = await orchestrator.generate_visuals(state)
    return state

@app.post("/api/videos/{project_id}/thumbnail", response_model=CreatorState)
async def trigger_thumbnail(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.generate_thumbnail(state)

@app.post("/api/videos/{project_id}/select-thumbnail", response_model=CreatorState)
async def select_thumbnail_endpoint(project_id: str, payload: dict):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    thumbnail_id = payload.get("thumbnail_id")
    if not thumbnail_id:
        raise HTTPException(status_code=400, detail="thumbnail_id is required")
    return await orchestrator.select_thumbnail(state, thumbnail_id)

@app.post("/api/videos/{project_id}/seo", response_model=CreatorState)
async def trigger_seo(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.generate_seo(state)

@app.post("/api/videos/{project_id}/validate", response_model=CreatorState)
async def trigger_validate(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.validate_production(state)

@app.post("/api/videos/{project_id}/render", response_model=CreatorState)
async def trigger_render(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return await orchestrator.render_video(state)

@app.post("/api/videos/{project_id}/replan", response_model=CreatorState)
async def trigger_replan(project_id: str):
    state = storage.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    orchestrator._log_action(state, "System", "Manual replan initiated by creator. Resetting stage pipeline.", status="warning")
    state.validation_retry_count = 0
    state.quality_checks = None
    state.stage_statuses["quality_check"] = StageStatus.PENDING
    state.stage_statuses["rendering"] = StageStatus.PENDING
    state.current_stage = PipelineStage.STRATEGY
    storage.save(state)
    return await orchestrator.analyze_content(state)

@app.post("/api/videos/{project_id}/approve", response_model=CreatorState)
async def submit_human_approval(project_id: str, request: HumanApprovalRequest):
    return await orchestrator.handle_approval(
        project_id=project_id,
        approval_type=request.approval_type,
        decision=request.decision,
        edits=request.edits
    )

@app.post("/api/videos/{project_id}/run-autonomous", response_model=CreatorState)
async def run_autonomous_pipeline(project_id: str):
    return await orchestrator.run_autonomous(project_id=project_id, pause_for_approvals=True)

# -------------------------------------------------------------
# Static Media and Web Hosting
# -------------------------------------------------------------
# Media streaming endpoint for audio, image, and video
@app.get("/media/{project_id}/{media_type}/{filename}")
async def get_media_file(project_id: str, media_type: str, filename: str):
    file_path = MEDIA_DIR / project_id / media_type / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Media file not found")
    return FileResponse(file_path)

@app.get("/media/{project_id}/{filename}")
async def get_root_media_file(project_id: str, filename: str):
    file_path = MEDIA_DIR / project_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Media file not found")
    return FileResponse(file_path)

# Serve Frontend static assets
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    if (FRONTEND_DIR / "css").exists():
        app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
    if (FRONTEND_DIR / "js").exists():
        app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")
    if (FRONTEND_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

@app.get("/")
async def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "CreatorFlow AI API is running. Frontend static index not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
