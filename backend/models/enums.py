from enum import Enum

class PipelineStage(str, Enum):
    IDLE = "idle"
    STRATEGY = "strategy"
    TITLES = "titles"
    HOOK = "hook"
    SCRIPT = "script"
    APPROVAL_SCRIPT = "approval_script"
    STORYBOARD = "storyboard"
    VOICE = "voice"
    VISUALS = "visuals"
    IMAGE_GEN = "image_gen"
    VIDEO_GEN = "video_gen"
    THUMBNAIL = "thumbnail"
    SEO = "seo"
    QUALITY_CHECK = "quality_check"
    APPROVAL_PRODUCTION = "approval_production"
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"

class StageStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    WAITING_FOR_APPROVAL = "WAITING FOR APPROVAL"

class VisualType(str, Enum):
    AI_VIDEO = "AI Video"
    MOTION_GRAPHIC = "Motion Graphic"
    AI_IMAGE = "AI Image"
    SCREEN_RECORDING = "Screen Recording"
    STOCK_FOOTAGE = "Stock Footage"
    TEXT_ANIMATION = "Text Animation"

class AssetStatus(str, Enum):
    GENERATED = "GENERATED"
    PLACEHOLDER = "PLACEHOLDER"
    WAITING_FOR_API = "WAITING FOR API"
    FAILED = "FAILED"

class VoiceGender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NEUTRAL = "Neutral"

class VideoDuration(str, Enum):
    DUR_1 = "1 min"
    DUR_3 = "3 min"
    DUR_5 = "5 min"
    DUR_10 = "10 min"

class VideoStyle(str, Enum):
    EDUCATIONAL = "Educational"
    CINEMATIC = "Cinematic"
    FAST_PACED = "Fast-paced"
    DOCUMENTARY = "Documentary"
    STORYTELLING = "Storytelling"
    NEWS_STYLE = "News-style"
