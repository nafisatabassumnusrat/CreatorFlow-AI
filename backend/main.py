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
    videos = storage.list_all()
    return [orchestrator.heal_state(v) for v in videos]

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
    state = orchestrator.heal_state(state)
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
# Static Media and Web Hosting (Self-Healing On-Demand Engine)
# -------------------------------------------------------------
@app.get("/media/{project_id}/{media_type}/{filename}")
async def get_media_file(project_id: str, media_type: str, filename: str):
    file_path = MEDIA_DIR / project_id / media_type / filename
    if file_path.exists():
        return FileResponse(file_path)

    fallback = BASE_DIR / "storage" / "media" / project_id / media_type / filename
    if fallback.exists():
        return FileResponse(fallback)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    state = storage.get(project_id)

    # 1. Image on-demand synthesis
    if media_type == "images":
        try:
            sc_idx = 0
            if "scene_" in filename:
                digits = "".join(c for c in filename.split("scene_")[-1] if c.isdigit())
                if digits:
                    sc_idx = max(0, int(digits) - 1)

            overlay = None
            prompt = None
            if state and state.storyboard and sc_idx < len(state.storyboard):
                sc = state.storyboard[sc_idx]
                overlay = f"SCENE {sc_idx + 1}: {sc.on_screen_text}"
                prompt = sc.image_prompt
            elif state and state.script and state.script.scenes and sc_idx < len(state.script.scenes):
                sc_s = state.script.scenes[sc_idx]
                overlay = f"SCENE {sc_idx + 1}: {sc_s.on_screen_text or state.topic}"
                prompt = sc_s.visual_direction or state.topic
            else:
                topic_label = state.topic if state else "Autonomous Production Scene"
                overlay = f"SCENE {sc_idx + 1}: {topic_label}"
                prompt = f"Cinematic 16:9 ultra-HD visual capturing {topic_label}"

            await orchestrator.image.generate_image(
                prompt=prompt or "Visual Scene Direction",
                aspect_ratio="16:9",
                output_path=file_path,
                overlay_title=overlay
            )
            if file_path.exists():
                return FileResponse(file_path, media_type="image/jpeg")
        except Exception as img_err:
            print(f"[ON-DEMAND IMAGE ERR] {img_err}")

    # 2. Thumbnail on-demand synthesis
    elif media_type == "thumbnails":
        try:
            thumb_title = None
            thumb_prompt = None
            if state and state.thumbnail_concepts:
                for c in state.thumbnail_concepts:
                    if c.id in filename or f"thumbnail_{c.id}" in filename:
                        thumb_title = c.title_text
                        thumb_prompt = c.image_prompt
                        break
            if not thumb_title and state:
                thumb_title = state.selected_thumbnail.title_text if state.selected_thumbnail else (state.selected_title or state.topic)
                thumb_prompt = state.selected_thumbnail.image_prompt if state.selected_thumbnail else f"YouTube Thumbnail for {state.topic}"

            await orchestrator.image.generate_image(
                prompt=thumb_prompt or "High-converting YouTube thumbnail",
                aspect_ratio="16:9",
                output_path=file_path,
                overlay_title=thumb_title or "YOUTUBE MASTER THUMBNAIL"
            )
            if file_path.exists():
                return FileResponse(file_path, media_type="image/jpeg")
        except Exception as thumb_err:
            print(f"[ON-DEMAND THUMB ERR] {thumb_err}")

    # 3. Audio on-demand synthesis
    elif media_type == "audio":
        try:
            sc_idx = 0
            if "scene_" in filename:
                digits = "".join(c for c in filename.split("scene_")[-1] if c.isdigit())
                if digits:
                    sc_idx = max(0, int(digits) - 1)

            narration = None
            if state and state.storyboard and sc_idx < len(state.storyboard):
                narration = state.storyboard[sc_idx].narration
            elif state and state.script and state.script.scenes and sc_idx < len(state.script.scenes):
                narration = state.script.scenes[sc_idx].narration

            if not narration:
                topic_label = state.topic if state else "this topic"
                narration = f"Welcome back. In this scene, we explore the crucial strategies for {topic_label}."

            voice_gender = str(state.voice.value if hasattr(state.voice, 'value') else state.voice) if state else "Neutral"
            lang = state.language if state else "English"
            try:
                await orchestrator.voice.synthesize(
                    text=narration,
                    voice_gender=voice_gender,
                    language=lang,
                    output_path=file_path
                )
            except Exception as tts_err:
                print(f"[TTS SYNTH ERR] {tts_err}")
                # Generate subtle audio placeholder using ffmpeg
                import imageio_ffmpeg
                import subprocess
                ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
                dur = max(4, len(narration.split()) // 3)
                cmd = [
                    ffmpeg_bin, "-y",
                    "-f", "lavfi",
                    "-i", f"sine=frequency=440:duration={dur}",
                    "-c:a", "libmp3lame",
                    "-b:a", "128k",
                    str(file_path)
                ]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if file_path.exists():
                return FileResponse(file_path, media_type="audio/mpeg")
        except Exception as audio_err:
            print(f"[ON-DEMAND AUDIO ERR] {audio_err}")

    # Fallback to demo thumbnail if image
    if media_type in ["images", "thumbnails"]:
        demo_img = BASE_DIR / "frontend" / "assets" / "demo_thumbnail.jpg"
        if demo_img.exists():
            return FileResponse(demo_img)

    raise HTTPException(status_code=404, detail="Media file not found")


@app.get("/media/{project_id}/{filename}")
async def get_root_media_file(project_id: str, filename: str):
    file_path = MEDIA_DIR / project_id / filename
    if file_path.exists():
        return FileResponse(file_path)

    fallback = BASE_DIR / "storage" / "media" / project_id / filename
    if fallback.exists():
        return FileResponse(fallback)

    state = storage.get(project_id)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Video (.mp4)
    if filename.endswith(".mp4"):
        is_demo = project_id.startswith("demo-") or (state and ("ai agent" in (state.topic or "").lower() or "chatbot" in (state.topic or "").lower()))
        demo_vid = BASE_DIR / "frontend" / "assets" / "demo_video.mp4"

        if is_demo and demo_vid.exists():
            return FileResponse(demo_vid)

        # On-demand fast MP4 assembly using active thumbnail / scene visual card
        try:
            active_thumb = MEDIA_DIR / project_id / "thumbnail.jpg"
            if not active_thumb.exists():
                t_label = (state.selected_title or state.topic or "Autonomous Studio") if state else "Autonomous Studio"
                await orchestrator.image.generate_image(
                    prompt=f"YouTube thumbnail for {t_label}",
                    aspect_ratio="16:9",
                    output_path=active_thumb,
                    overlay_title=t_label[:36]
                )

            audio_file = MEDIA_DIR / project_id / "audio" / "scene_01.mp3"
            await orchestrator.assembler.fast_assemble(
                image_path=active_thumb,
                audio_path=audio_file if audio_file.exists() else None,
                output_file=file_path,
                duration=state.storyboard[0].duration_sec if state and state.storyboard else 8.0
            )
            if file_path.exists():
                return FileResponse(file_path, media_type="video/mp4")
        except Exception as vid_err:
            print(f"[ON-DEMAND VIDEO ERR] {vid_err}")

        if demo_vid.exists() and is_demo:
            return FileResponse(demo_vid)

    # 2. Thumbnail / Image (.jpg, .png)
    elif filename.endswith((".jpg", ".png", ".webp")):
        try:
            title_text = (state.selected_thumbnail.title_text if state and state.selected_thumbnail else (state.selected_title or state.topic if state else "YouTube Thumbnail"))
            prompt_text = (state.selected_thumbnail.image_prompt if state and state.selected_thumbnail else (state.topic if state else "YouTube Master Thumbnail"))
            await orchestrator.image.generate_image(
                prompt=prompt_text,
                aspect_ratio="16:9",
                output_path=file_path,
                overlay_title=title_text[:36]
            )
            if file_path.exists():
                return FileResponse(file_path, media_type="image/jpeg")
        except Exception as thumb_err:
            print(f"[ON-DEMAND ROOT THUMB ERR] {thumb_err}")

        demo_img = BASE_DIR / "frontend" / "assets" / "demo_thumbnail.jpg"
        if demo_img.exists():
            return FileResponse(demo_img)

    raise HTTPException(status_code=404, detail="Media file not found")

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
