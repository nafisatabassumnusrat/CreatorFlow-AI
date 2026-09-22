import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from backend.models.schemas import CreatorState, DashboardMetrics
from backend.config import PROJECTS_DIR

class ProjectStorage:
    def __init__(self):
        self._projects: Dict[str, CreatorState] = {}
        self._load_all_from_disk()

    def _load_all_from_disk(self):
        if not PROJECTS_DIR.exists():
            return
        for file in PROJECTS_DIR.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    state = CreatorState(**data)
                    self._projects[state.project_id] = state
            except Exception as e:
                print(f"Error loading project {file}: {e}")

    def save(self, state: CreatorState) -> CreatorState:
        state.updated_at = datetime.utcnow().isoformat()
        self._projects[state.project_id] = state
        file_path = PROJECTS_DIR / f"{state.project_id}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(state.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error persisting project {state.project_id}: {e}")
        return state

    def get(self, project_id: str) -> Optional[CreatorState]:
        return self._projects.get(project_id)

    def list_all(self) -> List[CreatorState]:
        # Return sorted by updated_at desc
        return sorted(self._projects.values(), key=lambda p: p.updated_at, reverse=True)

    def delete(self, project_id: str) -> bool:
        if project_id in self._projects:
            del self._projects[project_id]
            file_path = PROJECTS_DIR / f"{project_id}.json"
            if file_path.exists():
                file_path.unlink()
            return True
        return False

    def get_metrics(self) -> DashboardMetrics:
        total = len(self._projects)
        completed = sum(1 for p in self._projects.values() if p.current_stage == "completed")
        in_prod = sum(1 for p in self._projects.values() if p.current_stage not in ["completed", "idle", "failed"])
        assets = sum(
            len(p.storyboard) + (1 if p.selected_thumbnail else 0) + (1 if p.rendered_video_url else 0)
            for p in self._projects.values()
        )
        return DashboardMetrics(
            videos_created=total,
            in_production=in_prod,
            completed=completed,
            assets_generated=assets
        )

# Global singleton storage
storage = ProjectStorage()
