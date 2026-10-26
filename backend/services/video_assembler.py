import asyncio
import os
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional
import imageio_ffmpeg
from backend.models.schemas import StoryboardScene
from backend.config import MEDIA_DIR

def _run_ffmpeg_sync(cmd: List[str]) -> subprocess.CompletedProcess:
    """Run FFmpeg command synchronously in a thread to prevent Windows asyncio subprocess NotImplementedError"""
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="ignore"
    )

class VideoAssembler:
    """
    Video Assembly Service using FFmpeg.
    Combines scene visuals, narration voiceover, ambient background music,
    and on-screen text overlays into a final 16:9 YouTube MP4.
    """

    def __init__(self):
        self.ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    async def get_audio_duration(self, audio_path: Path) -> float:
        """Probe audio duration using ffmpeg via thread"""
        cmd = [
            self.ffmpeg_bin,
            "-i", str(audio_path),
            "-f", "null", "-"
        ]
        res = await asyncio.to_thread(_run_ffmpeg_sync, cmd)
        text = res.stderr or ""
        for line in text.splitlines():
            if "Duration:" in line:
                try:
                    parts = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = parts.split(":")
                    return float(h) * 3600 + float(m) * 60 + float(s)
                except Exception:
                    pass
        return 5.0

    async def assemble(
        self,
        scenes: List[StoryboardScene],
        output_file: Path,
        background_music_mood: str = "Modern cinematic technology",
        include_captions: bool = True
    ) -> Path:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        unique_id = uuid.uuid4().hex[:8]
        temp_dir = output_file.parent / f"temp_assembly_{unique_id}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        segment_files = []
        fps = 25
        width = 1280
        height = 720

        # Check for system font on Windows
        font_file_arg = ""
        for test_font in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/segoeui.ttf"]:
            if Path(test_font).exists():
                font_file_arg = f":fontfile='{test_font}'"
                break

        try:
            for idx, scene in enumerate(scenes):
                seg_path = temp_dir / f"scene_{idx:03d}.mp4"
                
                # Check for audio file
                audio_path = None
                duration = float(scene.duration_sec) if scene.duration_sec else 6.0
                if scene.audio_url:
                    cand_audio = Path(scene.audio_url)
                    if not cand_audio.exists():
                        clean_audio = scene.audio_url.replace("/media/", "").lstrip("/").lstrip("\\")
                        cand_audio = MEDIA_DIR / clean_audio
                    if cand_audio.exists():
                        audio_path = cand_audio
                        real_dur = await self.get_audio_duration(audio_path)
                        if real_dur > 1.0:
                            duration = real_dur + 0.5  # padding for natural pause

                # Visual source
                img_path = None
                if scene.image_url:
                    cand_img = Path(scene.image_url)
                    if not cand_img.exists():
                        clean_img = scene.image_url.replace("/media/", "").lstrip("/").lstrip("\\")
                        cand_img = MEDIA_DIR / clean_img
                    if cand_img.exists():
                        img_path = cand_img

                # Text overlay escaping
                safe_text = (scene.on_screen_text or f"SCENE {idx+1}").replace("'", "").replace(":", "-").replace("\\", "/")[:40]

                # Build scene video segment
                if img_path and img_path.exists():
                    vf_with_text = (
                        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x0b0f19,"
                        f"drawbox=y=ih-120:color=black@0.6:width=iw:height=90:t=fill,"
                        f"drawtext=text='{safe_text}'{font_file_arg}:fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-95,"
                        "format=yuv420p"
                    )
                    vf_no_text = (
                        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x0b0f19,"
                        "format=yuv420p"
                    )

                    # Try with text first, fallback to no text if drawtext errors
                    for current_vf in [vf_with_text, vf_no_text]:
                        if audio_path and audio_path.exists():
                            cmd = [
                                self.ffmpeg_bin, "-y",
                                "-loop", "1",
                                "-i", str(img_path),
                                "-i", str(audio_path),
                                "-t", str(duration),
                                "-vf", current_vf,
                                "-c:v", "libx264",
                                "-preset", "ultrafast",
                                "-c:a", "aac",
                                "-b:a", "128k",
                                "-pix_fmt", "yuv420p",
                                "-shortest",
                                str(seg_path)
                            ]
                        else:
                            # Generate tone audio as fallback
                            cmd = [
                                self.ffmpeg_bin, "-y",
                                "-loop", "1",
                                "-i", str(img_path),
                                "-f", "lavfi",
                                "-i", "anullsrc=r=44100:cl=stereo",
                                "-t", str(duration),
                                "-vf", current_vf,
                                "-c:v", "libx264",
                                "-preset", "ultrafast",
                                "-c:a", "aac",
                                "-b:a", "128k",
                                "-pix_fmt", "yuv420p",
                                str(seg_path)
                            ]
                        res = await asyncio.to_thread(_run_ffmpeg_sync, cmd)
                        if seg_path.exists() and seg_path.stat().st_size > 1000:
                            break
                else:
                    # Solid color background with text
                    vf = f"drawbox=y=ih-120:color=black@0.6:width=iw:height=90:t=fill,format=yuv420p"
                    if audio_path and audio_path.exists():
                        cmd = [
                            self.ffmpeg_bin, "-y",
                            "-f", "lavfi",
                            "-i", f"color=c=0x0f172a:s={width}x{height}:d={duration}:r={fps}",
                            "-i", str(audio_path),
                            "-vf", vf,
                            "-c:v", "libx264",
                            "-preset", "ultrafast",
                            "-c:a", "aac",
                            "-b:a", "128k",
                            "-pix_fmt", "yuv420p",
                            "-shortest",
                            str(seg_path)
                        ]
                    else:
                        cmd = [
                            self.ffmpeg_bin, "-y",
                            "-f", "lavfi",
                            "-i", f"color=c=0x0f172a:s={width}x{height}:d={duration}:r={fps}",
                            "-f", "lavfi",
                            "-i", "anullsrc=r=44100:cl=stereo",
                            "-t", str(duration),
                            "-vf", vf,
                            "-c:v", "libx264",
                            "-preset", "ultrafast",
                            "-c:a", "aac",
                            "-pix_fmt", "yuv420p",
                            str(seg_path)
                        ]
                    await asyncio.to_thread(_run_ffmpeg_sync, cmd)

                if seg_path.exists() and seg_path.stat().st_size > 1000:
                    segment_files.append(seg_path)

            if not segment_files:
                raise RuntimeError("Failed to build any scene video segments.")

            # Create concat list file
            concat_txt = temp_dir / "concat_list.txt"
            with open(concat_txt, "w", encoding="utf-8") as f:
                for seg in segment_files:
                    safe_path = str(seg.resolve()).replace("\\", "/")
                    f.write(f"file '{safe_path}'\n")

            # Final concat assembly
            cmd_concat = [
                self.ffmpeg_bin, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_txt),
                "-c", "copy",
                str(output_file)
            ]
            res_concat = await asyncio.to_thread(_run_ffmpeg_sync, cmd_concat)

            if not output_file.exists() or output_file.stat().st_size < 1000:
                # If copy concat failed, re-encode concat
                cmd_reencode = [
                    self.ffmpeg_bin, "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", str(concat_txt),
                    "-c:v", "libx264",
                    "-preset", "ultrafast",
                    "-c:a", "aac",
                    str(output_file)
                ]
                await asyncio.to_thread(_run_ffmpeg_sync, cmd_reencode)

            return output_file
        finally:
            # Clean up temporary segments
            for f in segment_files:
                try:
                    f.unlink(missing_ok=True)
                except Exception:
                    pass
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass
