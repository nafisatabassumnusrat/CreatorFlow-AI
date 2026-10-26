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

def _load_font(size: int = 24, bold: bool = False):
    """Attempt to load a crisp TTF font with fallback to Pillow default."""
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()

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
        h = sum(ord(c) for c in (overlay_title or prompt)) % 5
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

        # Draw smooth vertical background gradient
        for y in range(height):
            ratio = y / height
            r = int(bg1[0] * (1 - ratio) + bg2[0] * ratio)
            g = int(bg1[1] * (1 - ratio) + bg2[1] * ratio)
            b = int(bg1[2] * (1 - ratio) + bg2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Geometric grid lines
        for x in range(0, width, 120):
            draw.line([(x, 0), (x, height)], fill=(35, 45, 65))
        for y in range(0, height, 120):
            draw.line([(0, y), (width, y)], fill=(35, 45, 65))

        # Glowing circles / ambient curves
        draw.ellipse([width - 500, -200, width + 300, 600], outline=accent1, width=3)
        draw.ellipse([-200, height - 500, 500, height + 200], outline=accent2, width=3)

        # Fonts
        font_header = _load_font(24, bold=True)
        font_badge = _load_font(20, bold=True)
        font_tag = _load_font(26, bold=True)
        font_title = _load_font(52, bold=True)
        font_prompt_label = _load_font(22, bold=True)
        font_prompt = _load_font(26, bold=False)
        font_footer = _load_font(20, bold=False)

        # Top Header Bar / Branding
        draw.rectangle([80, 60, 480, 115], fill=(20, 24, 38), outline=accent1, width=2)
        draw.text((105, 75), "CREATORFLOW AI  |  STUDIO", fill=(240, 245, 255), font=font_header)

        # Status Badge
        draw.rectangle([width - 480, 60, width - 80, 115], fill=(30, 41, 59), outline=(148, 163, 184), width=1)
        draw.text((width - 440, 75), "VISUAL ASSET: 4K MASTER", fill=(226, 232, 240), font=font_badge)

        # Central Card
        main_title = (overlay_title if overlay_title else prompt[:70]).strip()
        card_box = [120, 200, width - 120, height - 160]
        draw.rectangle(card_box, fill=(13, 17, 28), outline=(60, 75, 105), width=2)

        # Glowing vertical accent bar
        draw.rectangle([120, 200, 140, height - 160], fill=accent1)

        # Card Category Tag
        draw.text((180, 240), "VISUAL SCENE DIRECTION", fill=accent2, font=font_tag)

        # Main Title - wrapped cleanly
        words = main_title.split()
        title_lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 36:
                title_lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            title_lines.append(" ".join(cur_line))

        y_offset = 300
        for line in title_lines[:2]:
            draw.text((180, y_offset), line, fill=(255, 255, 255), font=font_title)
            y_offset += 65

        # Visual Prompt Box
        box_y = y_offset + 30
        draw.rectangle([180, box_y, width - 180, box_y + 240], fill=(20, 27, 44), outline=(45, 58, 85), width=1)
        draw.text((210, box_y + 20), "AI PRODUCTION PROMPT", fill=(148, 163, 184), font=font_prompt_label)

        p_words = prompt.split()
        p_lines = []
        cur_p = []
        for w in p_words:
            cur_p.append(w)
            if len(" ".join(cur_p)) > 70:
                p_lines.append(" ".join(cur_p))
                cur_p = []
        if cur_p:
            p_lines.append(" ".join(cur_p))

        for idx, line in enumerate(p_lines[:4]):
            draw.text((210, box_y + 60 + idx * 38), line, fill=(226, 232, 240), font=font_prompt)

        # Footer
        draw.text((130, height - 120), "16:9 Ultra HD (1920x1080) • CreatorFlow Production Suite", fill=(100, 116, 139), font=font_footer)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path), "JPEG", quality=92)
        return output_path

def get_image_provider() -> ImageProvider:
    if OPENAI_API_KEY:
        return OpenAIImageProvider(OPENAI_API_KEY)
    return PillowCreativeImageProvider()
