import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


def _require_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "FFmpeg is not installed. Install it from https://ffmpeg.org or use Docker."
        )


def _run_ffmpeg(cmd: list[str], error_label: str = "FFmpeg"):
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"{error_label} failed: {result.stderr.decode()[-500:]}")
    return result


class AudioConverter(BaseConverter):
    category = "audio"

    supported_input_formats = [
        "mp3", "wav", "flac", "aac", "ogg", "wma", "m4a",
        "aiff", "aif", "opus", "amr", "ac3", "dts", "ape",
        "wv", "mka", "ra", "mid", "midi",
        # video formats — ffmpeg strips video via -vn and keeps the audio track
        "mp4", "mkv", "mov", "avi", "webm", "flv", "m4v", "3gp",
    ]

    supported_output_formats = [
        "mp3", "wav", "flac", "aac", "ogg", "m4a",
        "aiff", "opus", "ac3", "wma",
    ]

    async def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str,
        output_format: str,
        progress_callback: Optional[Callable[[int], Any]] = None,
    ) -> Path:
        _require_ffmpeg()

        if progress_callback:
            await progress_callback(10)

        out = output_format.lower()
        codec_map = {
            "mp3": "libmp3lame", "aac": "aac", "ogg": "libvorbis",
            "flac": "flac", "opus": "libopus", "wav": "pcm_s16le",
            "m4a": "aac", "aiff": "pcm_s16be", "ac3": "ac3",
            "wma": "wmav2",
        }
        codec = codec_map.get(out, "copy")

        cmd = [
            "ffmpeg", "-i", str(input_path),
            "-vn",  # no video
            "-acodec", codec,
            "-y",  # overwrite
            str(output_path),
        ]

        # Add quality settings
        if out == "mp3":
            cmd.insert(-1, "-q:a")
            cmd.insert(-1, "2")
        elif out in ("aac", "m4a"):
            cmd.insert(-1, "-b:a")
            cmd.insert(-1, "192k")

        await asyncio.to_thread(_run_ffmpeg, cmd, "FFmpeg audio conversion")

        if progress_callback:
            await progress_callback(100)

        return output_path


class VideoConverter(BaseConverter):
    category = "video"

    supported_input_formats = [
        "mp4", "avi", "mkv", "mov", "wmv", "flv", "webm",
        "mpeg", "mpg", "3gp", "m4v", "vob", "ts", "mts",
        "m2ts", "ogv", "f4v", "asf", "rm", "rmvb", "divx",
    ]

    supported_output_formats = [
        "mp4", "avi", "mkv", "mov", "webm", "gif",
        "mpeg", "3gp", "m4v", "ts", "flv", "ogv",
    ]

    async def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str,
        output_format: str,
        progress_callback: Optional[Callable[[int], Any]] = None,
    ) -> Path:
        _require_ffmpeg()

        if progress_callback:
            await progress_callback(5)

        out = output_format.lower()

        # Special case: video to GIF
        if out == "gif":
            return await self._convert_to_gif(input_path, output_path, progress_callback)

        codec_map = {
            "mp4": ("libx264", "aac"),
            "avi": ("mpeg4", "mp3"),
            "mkv": ("libx264", "aac"),
            "mov": ("libx264", "aac"),
            "webm": ("libvpx-vp9", "libopus"),
            "mpeg": ("mpeg2video", "mp2"),
            "3gp": ("libx264", "aac"),
            "m4v": ("libx264", "aac"),
            "ts": ("libx264", "aac"),
            "flv": ("libx264", "aac"),
            "ogv": ("libtheora", "libvorbis"),
        }

        vcodec, acodec = codec_map.get(out, ("libx264", "aac"))

        cmd = [
            "ffmpeg", "-i", str(input_path),
            "-c:v", vcodec,
            "-c:a", acodec,
            "-y",
            str(output_path),
        ]

        await asyncio.to_thread(_run_ffmpeg, cmd, "FFmpeg video conversion")

        if progress_callback:
            await progress_callback(100)

        return output_path

    async def _convert_to_gif(
        self, input_path: Path, output_path: Path,
        progress_callback: Optional[Callable[[int], Any]] = None,
    ) -> Path:
        # Two-pass GIF: generate palette then use it
        palette_path = output_path.parent / f"{output_path.stem}_palette.png"

        # Pass 1: Generate palette
        cmd1 = [
            "ffmpeg", "-i", str(input_path),
            "-vf", "fps=15,scale=480:-1:flags=lanczos,palettegen",
            "-y", str(palette_path),
        ]
        await asyncio.to_thread(_run_ffmpeg, cmd1, "FFmpeg palette generation")

        if progress_callback:
            await progress_callback(50)

        # Pass 2: Use palette
        cmd2 = [
            "ffmpeg", "-i", str(input_path), "-i", str(palette_path),
            "-lavfi", "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse",
            "-y", str(output_path),
        ]

        try:
            await asyncio.to_thread(_run_ffmpeg, cmd2, "FFmpeg GIF conversion")
        finally:
            palette_path.unlink(missing_ok=True)

        if progress_callback:
            await progress_callback(100)

        return output_path
