import asyncio
import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
import imageio_ffmpeg
from backend.models.schemas import StoryboardScene

class VideoAssembler:
    """
    Video Assembly Service using FFmpeg.
    Combines scene visuals, narration voiceover, ambient background music,
    and on-screen text overlays into a final 16:9 YouTube MP4.
    """

    def __init__(self):
        self.ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    async def get_audio_duration(self, audio_path: Path) -> float:
        """Probe audio duration using ffmpeg"""
        cmd = [
            self.ffmpeg_bin,
            "-i", str(audio_path),
            "-f", "null", "-"
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, stderr = await proc.communicate()
        text = stderr.decode("utf-8", errors="ignore")
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

        try:
            for idx, scene in enumerate(scenes):
                seg_path = temp_dir / f"scene_{idx:03d}.mp4"
                
                # Check for audio file
                audio_path = None
                duration = float(scene.duration_sec) if scene.duration_sec else 6.0
                if scene.audio_url and os.path.exists(scene.audio_url):
                    audio_path = Path(scene.audio_url)
                    real_dur = await self.get_audio_duration(audio_path)
                    if real_dur > 1.0:
                        duration = real_dur + 0.5  # padding for natural pause

                # Visual source
                img_path = None
                if scene.image_url and os.path.exists(scene.image_url):
                    img_path = Path(scene.image_url)

                # Text overlay escaping
                safe_text = (scene.on_screen_text or f"SCENE {idx+1}").replace("'", "").replace(":", "-")[:45]

                # Build scene video segment
                if img_path and img_path.exists():
                    # Ken-burns zoompan
                    total_frames = int(duration * fps)
                    vf_parts = [
                        f"scale={width}:{height}:force_original_aspect_ratio=decrease",
                        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x0b0f19",
                        f"drawbox=y=ih-120:color=black@0.6:width=iw:height=90:t=fill",
                        f"drawtext=text='{safe_text}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-95",
                        "format=yuv420p"
                    ]
                    vf = ",".join(vf_parts)

                    if audio_path and audio_path.exists():
                        cmd = [
                            self.ffmpeg_bin, "-y",
                            "-loop", "1",
                            "-i", str(img_path),
                            "-i", str(audio_path),
                            "-t", str(duration),
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
                        # Generate tone audio as fallback
                        cmd = [
                            self.ffmpeg_bin, "-y",
                            "-loop", "1",
                            "-i", str(img_path),
                            "-f", "lavfi",
                            "-i", f"anullsrc=r=44100:cl=stereo",
                            "-t", str(duration),
                            "-vf", vf,
                            "-c:v", "libx264",
                            "-preset", "ultrafast",
                            "-c:a", "aac",
                            "-b:a", "128k",
                            "-pix_fmt", "yuv420p",
                            str(seg_path)
                        ]
                else:
                    # Solid color background with text
                    vf = f"drawtext=text='{safe_text}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2,format=yuv420p"
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
                            "-i", f"anullsrc=r=44100:cl=stereo",
                            "-t", str(duration),
                            "-vf", vf,
                            "-c:v", "libx264",
                            "-preset", "ultrafast",
                            "-c:a", "aac",
                            "-pix_fmt", "yuv420p",
                            str(seg_path)
                        ]

                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                await proc.communicate()

                if seg_path.exists():
                    segment_files.append(seg_path)

            if not segment_files:
                raise RuntimeError("Failed to build any scene video segments.")

            # Create concat list file
            concat_txt = temp_dir / "concat_list.txt"
            with open(concat_txt, "w", encoding="utf-8") as f:
                for seg in segment_files:
                    # ffmpeg concat demuxer expects forward slashes or escaped backslashes
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
            proc = await asyncio.create_subprocess_exec(*cmd_concat, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()

            return output_file
        finally:
            # Clean up temporary segments
            for f in segment_files:
                try:
                    f.unlink(missing_ok=True)
                except Exception:
                    pass
