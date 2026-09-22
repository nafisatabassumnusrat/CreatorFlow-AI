import os
import asyncio
import httpx
from pathlib import Path
from backend.providers.base import VoiceProvider
from backend.config import ELEVENLABS_API_KEY, OPENAI_API_KEY

class ElevenLabsProvider(VoiceProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Default voice ID: Adam or Rachel
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"
        self.endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"

    @property
    def provider_name(self) -> str:
        return "ElevenLabs TTS"

    @property
    def is_real_api(self) -> bool:
        return True

    async def synthesize(self, text: str, voice_gender: str, language: str, output_path: Path) -> Path:
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(self.endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(resp.content)
            return output_path

class OpenAITTSProvider(VoiceProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/audio/speech"

    @property
    def provider_name(self) -> str:
        return "OpenAI TTS"

    @property
    def is_real_api(self) -> bool:
        return True

    async def synthesize(self, text: str, voice_gender: str, language: str, output_path: Path) -> Path:
        voice = "alloy" if voice_gender == "Neutral" else ("onyx" if voice_gender == "Male" else "nova")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "tts-1",
            "input": text,
            "voice": voice
        }
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(self.endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(resp.content)
            return output_path

class GoogleTTSProvider(VoiceProvider):
    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    @property
    def provider_name(self) -> str:
        return "Google Cloud TTS"

    @property
    def is_real_api(self) -> bool:
        return bool(self.api_key)

    async def synthesize(self, text: str, voice_gender: str, language: str, output_path: Path) -> Path:
        raise NotImplementedError("Google Cloud TTS requires service credentials.")

class EdgeTTSProvider(VoiceProvider):
    """
    High-fidelity neural voice provider using Edge-TTS.
    Provides realistic, natural-sounding audio in English, Bengali, Hindi, etc.
    """
    @property
    def provider_name(self) -> str:
        return "Neural Voice Engine (Edge-TTS)"

    @property
    def is_real_api(self) -> bool:
        return True

    async def synthesize(self, text: str, voice_gender: str, language: str, output_path: Path) -> Path:
        import edge_tts
        # Select voice based on language and gender
        lang_lower = language.lower()
        if "bangla" in lang_lower or "bengali" in lang_lower:
            voice = "bn-BD-PradeepNeural" if voice_gender == "Male" else "bn-BD-NabanitaNeural"
        elif "hindi" in lang_lower:
            voice = "hi-IN-MadhurNeural" if voice_gender == "Male" else "hi-IN-SwaraNeural"
        else:
            voice = "en-US-ChristopherNeural" if voice_gender == "Male" else ("en-US-JennyNeural" if voice_gender == "Female" else "en-US-GuyNeural")

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))
        return output_path

class MockTTSProvider(VoiceProvider):
    """
    Clearly labeled Mock Voice Provider.
    Used when offline or as a fallback. Produces a valid audio file with tone tones.
    """
    @property
    def provider_name(self) -> str:
        return "Mock TTS (Demo Fallback)"

    @property
    def is_real_api(self) -> bool:
        return False

    async def synthesize(self, text: str, voice_gender: str, language: str, output_path: Path) -> Path:
        # Generates a clean subtle audio tone / silence placeholder mp3 using ffmpeg
        import imageio_ffmpeg
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        duration = max(3, len(text.split()) // 3)
        cmd = [
            ffmpeg_bin, "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency=440:duration={duration}",
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            str(output_path)
        ]
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()
        return output_path

def get_voice_provider() -> VoiceProvider:
    if ELEVENLABS_API_KEY:
        return ElevenLabsProvider(ELEVENLABS_API_KEY)
    elif OPENAI_API_KEY:
        return OpenAITTSProvider(OPENAI_API_KEY)
    
    # Try Edge-TTS as the primary high-fidelity provider
    try:
        import edge_tts
        return EdgeTTSProvider()
    except Exception:
        return MockTTSProvider()
