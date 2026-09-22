import os
import httpx
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import math
from backend.providers.base import ImageProvider
from backend.config import OPENAI_API_KEY, REPLICATE_API_TOKEN

class OpenAIImageProvider(ImageProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://api.openai.com/v1/images/generations"

    @property
    def provider_name(self) -> str:
        return "OpenAI DALL-E 3"

    @property
    def is_real_api(self) -> bool:
        return True

    async def generate_image(self, prompt: str, aspect_ratio: str, output_path: Path, overlay_title: Optional[str] = None) -> Path:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        size = "1792x1024" if "16:9" in aspect_ratio else "1024x1024"
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": size,
            "quality": "standard",
            "n": 1
        }
        async with httpx.AsyncClient(timeout=90.0) as client:
            resp = await client.post(self.endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            image_url = resp.json()["data"][0]["url"]
            # Download image
            img_resp = await client.get(image_url)
            with open(output_path, "wb") as f:
                f.write(img_resp.content)
            return output_path

class PillowCreativeImageProvider(ImageProvider):
    """
    High-fidelity Local Visual Card Generator.
    Generates beautiful 1920x1080 graphic cards with modern gradients, grid geometry,
    scene context, typography, and clear labeling.
    Clearly marks assets as 'LOCAL CREATIVE ENGINE / PLACEHOLDER'.
    """
    @property
    def provider_name(self) -> str:
        return "CreatorFlow Visual Engine (Local)"

    @property
    def is_real_api(self) -> bool:
        return False

    async def generate_image(self, prompt: str, aspect_ratio: str, output_path: Path, overlay_title: Optional[str] = None) -> Path:
        width = 1920
        height = 1080

        # Select color palette based on prompt hash
        h = sum(ord(c) for c in prompt) % 5
        palettes = [
            ((15, 23, 42), (30, 41, 59), (99, 102, 241), (168, 85, 247)),    # Slate / Indigo / Purple
            ((10, 15, 29), (20, 30, 55), (14, 165, 233), (56, 189, 248)),    # Deep Blue / Cyan
            ((24, 24, 27), (39, 39, 42), (244, 63, 94), (251, 146, 60)),     # Zinc / Rose / Amber
            ((15, 23, 42), (23, 37, 84), (16, 185, 129), (52, 211, 153)),    # Emerald / Tech
            ((18, 18, 20), (38, 38, 45), (139, 92, 246), (236, 72, 153)),    # Cyber Violet / Pink
        ]
        bg1, bg2, accent1, accent2 = palettes[h]

        img = Image.new("RGB", (width, height), bg1)
        draw = ImageDraw.Draw(img)

        # Draw smooth vertical & radial background gradient
        for y in range(height):
            ratio = y / height
            r = int(bg1[0] * (1 - ratio) + bg2[0] * ratio)
            g = int(bg1[1] * (1 - ratio) + bg2[1] * ratio)
            b = int(bg1[2] * (1 - ratio) + bg2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Add geometric tech grid lines
        grid_color = (255, 255, 255, 15)
        for x in range(0, width, 120):
            draw.line([(x, 0), (x, height)], fill=(40, 50, 70))
        for y in range(0, height, 120):
            draw.line([(0, y), (width, y)], fill=(40, 50, 70))

        # Subtle glowing circles
        draw.ellipse([width - 500, -200, width + 300, 600], outline=accent1, width=3)
        draw.ellipse([-200, height - 500, 500, height + 200], outline=accent2, width=3)

        # Draw Header Bar / Branding
        draw.rectangle([80, 70, 460, 120], fill=(20, 24, 38), outline=accent1, width=2)
        draw.text((105, 84), "CREATORFLOW AI  |  STUDIO", fill=(220, 225, 245))

        # Clear Status Badge
        draw.rectangle([width - 450, 70, width - 80, 120], fill=(30, 41, 59), outline=(148, 163, 184), width=1)
        draw.text((width - 425, 84), "VISUAL ASSET: PLACEHOLDER", fill=(203, 213, 225))

        # Central Title / Overlay
        main_title = overlay_title if overlay_title else prompt[:70]
        # Draw central dark card
        card_box = [140, 260, width - 140, height - 240]
        draw.rectangle(card_box, fill=(13, 17, 28), outline=(60, 70, 95), width=2)

        # Glowing accent bar on left of card
        draw.rectangle([140, 260, 156, height - 240], fill=accent1)

        # Title text inside card
        draw.text((200, 320), "SCENE VISUAL DIRECTION", fill=accent2)
        draw.text((200, 380), main_title[:60], fill=(255, 255, 255))
        if len(main_title) > 60:
            draw.text((200, 440), main_title[60:130], fill=(255, 255, 255))

        # Prompt description
        draw.text((200, 530), "AI GENERATION PROMPT:", fill=(148, 163, 184))
        # Word wrap prompt roughly
        words = prompt.split()
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 75:
                lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))

        for idx, line in enumerate(lines[:4]):
            draw.text((200, 570 + idx * 36), line, fill=(203, 213, 225))

        # Footer Note
        draw.text((140, height - 140), "16:9 Ultra HD (1920x1080) • Dynamic Storyboard Frame • Production Ready", fill=(100, 116, 139))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path), "JPEG", quality=92)
        return output_path

def get_image_provider() -> ImageProvider:
    if OPENAI_API_KEY:
        return OpenAIImageProvider(OPENAI_API_KEY)
    return PillowCreativeImageProvider()
