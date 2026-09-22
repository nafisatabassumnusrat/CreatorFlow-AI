import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
PROJECTS_DIR = STORAGE_DIR / "projects"
MEDIA_DIR = STORAGE_DIR / "media"
FONTS_DIR = BASE_DIR / "assets" / "fonts"

# Ensure directories exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# API Keys (optional; fallback to high-fidelity local providers if unset)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
