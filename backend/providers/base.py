from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

class LLMProvider(ABC):
    @abstractmethod
    async def generate_json(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate structured JSON using LLM"""
        pass

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        """Generate text using LLM"""
        pass

class VoiceProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, voice_gender: str, language: str, output_path: Path) -> Path:
        """Synthesize spoken narration audio from text"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_real_api(self) -> bool:
        pass

class ImageProvider(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str, aspect_ratio: str, output_path: Path, overlay_title: Optional[str] = None) -> Path:
        """Generate an image or production visual asset"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_real_api(self) -> bool:
        pass

class VideoProvider(ABC):
    @abstractmethod
    async def generate_clip(self, prompt: str, duration_sec: int, output_path: Path, image_source: Optional[Path] = None) -> Path:
        """Generate a short video clip or dynamic motion scene"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_real_api(self) -> bool:
        pass
