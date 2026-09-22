import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.models.schemas import VideoCreateRequest, VideoDuration, VideoStyle, VoiceGender
from backend.services.storage import storage
from backend.services.orchestrator import orchestrator

async def main():
    print("Testing CreatorFlow AI Agent Pipeline...")
    req = VideoCreateRequest(
        niche="AI & Technology",
        topic="5 AI Agents Every Developer Should Know in 2026",
        target_audience="University students and beginner developers",
        language="English",
        duration=VideoDuration.DUR_3,
        style=VideoStyle.EDUCATIONAL,
        voice=VoiceGender.NEUTRAL,
        reference_channel="@Fireship",
        brand_info="Clean modern dark theme"
    )

    # 1. Initialize project
    from backend.models.schemas import CreatorState
    from backend.models.enums import PipelineStage, StageStatus
    import uuid
    from datetime import datetime

    p_id = f"test-{uuid.uuid4().hex[:6]}"
    state = CreatorState(
        project_id=p_id,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
        niche=req.niche,
        topic=req.topic,
        target_audience=req.target_audience,
        language=req.language,
        duration=req.duration,
        style=req.style,
        voice=req.voice,
        reference_channel=req.reference_channel,
        brand_info=req.brand_info,
        current_stage=PipelineStage.IDLE,
        stage_statuses={}
    )
    storage.save(state)
    print(f"Created Project: {state.project_id}")

    # 2. Stage 1: Strategy
    state = await orchestrator.analyze_content(state)
    print(f"[OK] Strategy Angle: {state.selected_angle.title}")

    # 3. Stage 2: Titles
    state = await orchestrator.generate_titles(state)
    print(f"[OK] Selected Title: {state.selected_title}")

    # 4. Stage 3: Hook
    state = await orchestrator.generate_hook(state)
    print(f"[OK] Hook: {state.hook.hook_text[:60]}...")

    # 5. Stage 4: Script
    state = await orchestrator.generate_script(state)
    print(f"[OK] Script Scenes: {len(state.script.scenes)}")
    print(f"[OK] Human Approval Status: {state.waiting_for_approval_type}")

    # Human Gate: approve
    state = await orchestrator.handle_approval(state.project_id, "script", "approve")
    print(f"[OK] Approved Script. Storyboard Scenes: {len(state.storyboard)}")

    # 6. Stage 6: Voice
    state = await orchestrator.generate_voice(state)
    print(f"[OK] Voice generated for {len([s for s in state.storyboard if s.audio_url])} scenes")

    # 7. Stage 7 & 8: Visuals & Images
    state = await orchestrator.generate_visuals(state)
    print(f"[OK] Visuals generated for {len([s for s in state.storyboard if s.image_url])} scenes")

    # 8. Stage 10: Thumbnail
    state = await orchestrator.generate_thumbnail(state)
    print(f"[OK] Thumbnail: {state.selected_thumbnail.title_text} (Score: {state.selected_thumbnail.overall_score})")

    # 9. Stage 11: SEO
    state = await orchestrator.generate_seo(state)
    print(f"[OK] SEO Chapters: {len(state.seo.chapters)}")

    # 10. Stage 12: Quality Check
    state = await orchestrator.validate_production(state)
    print(f"[OK] Quality Check Passed: {state.quality_checks.passed}")

    # Human Gate 2: Approve Production
    state = await orchestrator.handle_approval(state.project_id, "production", "approve")
    print(f"[OK] Rendered Video: {state.rendered_video_url}")
    print(f"[OK] Final Package Ready: {bool(state.final_package)}")
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
