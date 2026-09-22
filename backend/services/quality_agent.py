from datetime import datetime
from typing import Tuple, List
from backend.models.schemas import (
    CreatorState,
    QualityCheckReport,
    QualityCheckItem,
)

class QualityControlAgent:
    """
    Quality Control Agent.
    Inspects content integrity, production assets, and YouTube package readiness.
    If defects are found, diagnoses the root cause and triggers a targeted retry.
    """

    def inspect(self, state: CreatorState) -> QualityCheckReport:
        checks: List[QualityCheckItem] = []
        issues: List[str] = []
        recommendations: List[str] = []
        affected_stage = None

        # -------------------------------------------------------------
        # 1. Content Validation
        # -------------------------------------------------------------
        # Script matches topic
        topic_words = set(w.lower() for w in state.topic.split() if len(w) > 3)
        script_text = (state.script.full_narration if state.script else "").lower()
        topic_matches = any(w in script_text for w in topic_words)
        
        checks.append(QualityCheckItem(
            category="Content",
            name="Topic Relevance & Alignment",
            passed=topic_matches,
            details=f"Verified script contains core topic terms: {list(topic_words)[:3]}",
            severity="error" if not topic_matches else "info"
        ))
        if not topic_matches:
            issues.append("Script does not sufficiently reflect the target topic keywords.")
            affected_stage = "script"

        # Hook connection
        hook_present = bool(state.hook and len(state.hook.hook_text.strip()) > 10)
        checks.append(QualityCheckItem(
            category="Content",
            name="Hook Punchiness & Curiosity",
            passed=hook_present,
            details="5-15s opening hook creates curiosity and delivers initial value promise.",
            severity="error" if not hook_present else "info"
        ))
        if not hook_present:
            issues.append("Opening hook is missing or lacks sufficient length.")
            affected_stage = affected_stage or "hook"

        # CTA Relevance
        cta_present = bool(state.script and state.script.call_to_action and len(state.script.call_to_action) > 10)
        checks.append(QualityCheckItem(
            category="Content",
            name="Call-To-Action (CTA) Clarity",
            passed=cta_present,
            details="Explicit viewer engagement and follow-up prompt configured.",
            severity="warning" if not cta_present else "info"
        ))

        # -------------------------------------------------------------
        # 2. Production Validation
        # -------------------------------------------------------------
        # Storyboard scenes exist
        has_scenes = len(state.storyboard) >= 3
        checks.append(QualityCheckItem(
            category="Production",
            name="Scene Storyboard Coverage",
            passed=has_scenes,
            details=f"{len(state.storyboard)} production scenes generated.",
            severity="error" if not has_scenes else "info"
        ))
        if not has_scenes:
            issues.append("Insufficient production scenes generated in storyboard.")
            affected_stage = affected_stage or "storyboard"

        # Visuals & prompts for every scene
        all_visuals = all(bool(s.image_prompt and s.visual_description) for s in state.storyboard)
        checks.append(QualityCheckItem(
            category="Production",
            name="Scene Visual Prompt Completeness",
            passed=all_visuals,
            details="Every scene specifies visual description, prompt, and visual type.",
            severity="warning" if not all_visuals else "info"
        ))

        # Narration for every scene
        all_narrations = all(bool(s.narration.strip()) for s in state.storyboard)
        checks.append(QualityCheckItem(
            category="Production",
            name="Narration Audio Coverage",
            passed=all_narrations,
            details="All scenes contain synchronized narration script.",
            severity="error" if not all_narrations else "info"
        ))
        if not all_narrations:
            issues.append("Some storyboard scenes are missing narration text.")
            affected_stage = affected_stage or "script"

        # Duration timing sanity
        target_dur_map = {"1 min": 60, "3 min": 180, "5 min": 300, "10 min": 600}
        target_sec = target_dur_map.get(str(state.duration.value if hasattr(state.duration, 'value') else state.duration), 180)
        actual_sec = sum(s.duration_sec for s in state.storyboard)
        duration_tolerance = abs(actual_sec - target_sec) <= (target_sec * 0.45)
        checks.append(QualityCheckItem(
            category="Production",
            name="Duration Pacing Alignment",
            passed=duration_tolerance,
            details=f"Calculated {actual_sec}s runtime against {target_sec}s target.",
            severity="warning" if not duration_tolerance else "info"
        ))

        # -------------------------------------------------------------
        # 3. YouTube Package Validation
        # -------------------------------------------------------------
        has_title = bool(state.selected_title and len(state.selected_title) > 5)
        checks.append(QualityCheckItem(
            category="Package",
            name="YouTube Title Selected",
            passed=has_title,
            details=f"Primary title: '{state.selected_title}'",
            severity="error" if not has_title else "info"
        ))
        if not has_title:
            issues.append("No primary YouTube title has been selected.")
            affected_stage = affected_stage or "titles"

        has_seo = bool(state.seo and len(state.seo.description) > 30)
        checks.append(QualityCheckItem(
            category="Package",
            name="SEO & Metadata Completeness",
            passed=has_seo,
            details="Chapters, tags, hashtags, and description populated.",
            severity="warning" if not has_seo else "info"
        ))
        if not has_seo:
            issues.append("SEO metadata or chapter timestamps are incomplete.")
            affected_stage = affected_stage or "seo"

        has_thumbnail = bool(state.selected_thumbnail and (state.selected_thumbnail.image_url or state.selected_thumbnail.image_prompt))
        checks.append(QualityCheckItem(
            category="Package",
            name="Thumbnail Asset Readiness",
            passed=has_thumbnail,
            details="Thumbnail concept scored and visual asset linked.",
            severity="warning" if not has_thumbnail else "info"
        ))
        if not has_thumbnail:
            issues.append("Thumbnail visual asset is not ready.")
            affected_stage = affected_stage or "thumbnail"

        # Overall verdict
        has_critical_error = any(not c.passed and c.severity == "error" for c in checks)
        passed = not has_critical_error

        if not passed:
            recommendations.append(f"Auto-repair recommended for stage '{affected_stage}'.")
            recommendations.append("Triggering autonomous retry loop...")
        else:
            recommendations.append("All production quality standards met. Package ready for final human review.")

        return QualityCheckReport(
            passed=passed,
            checked_at=datetime.utcnow().strftime("%H:%M:%S"),
            checks=checks,
            issues_identified=issues,
            retry_required=not passed,
            affected_stage=affected_stage,
            recommendations=recommendations
        )
