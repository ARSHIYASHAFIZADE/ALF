import asyncio
import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


class ArchiveConverter(BaseConverter):
    category = "archive"

    supported_input_formats = [
        "zip", "tar", "gz", "tgz", "bz2", "tbz2", "xz", "txz", "7z", "rar",
    ]

    supported_output_formats = [
        "zip", "tar", "gz", "tgz", "bz2", "xz", "7z",
    ]

    async def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str,
        output_format: str,
        progress_callback: Optional[Callable[[int], Any]] = None,
    ) -> Path:
        if progress_callback:
            await progress_callback(10)

        inp = input_format.lower()
        out = output_format.lower()

        # Step 1: Extract to temp dir
        extract_dir = output_path.parent / f"_extract_{output_path.stem}"
        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            await self._extract(input_path, extract_dir, inp)

            if progress_callback:
                await progress_callback(50)

            # Step 2: Repackage
            await self._compress(extract_dir, output_path, out)
        finally:
            shutil.rmtree(extract_dir, ignore_errors=True)

        if progress_callback:
            await progress_callback(100)

        return output_path

    async def _extract(self, input_path: Path, extract_dir: Path, fmt: str):
        def _do():
            if fmt == "zip":
                with zipfile.ZipFile(input_path, "r") as zf:
                    zf.extractall(extract_dir)
            elif fmt in ("tar", "gz", "tgz", "bz2", "tbz2", "xz", "txz"):
                mode_map = {
                    "tar": "r:", "gz": "r:gz", "tgz": "r:gz",
                    "bz2": "r:bz2", "tbz2": "r:bz2", "xz": "r:xz", "txz": "r:xz",
                }
                mode = mode_map.get(fmt, "r:")
                with tarfile.open(input_path, mode) as tf:
                    tf.extractall(extract_dir, filter="data")
            elif fmt == "7z":
                import py7zr
                with py7zr.SevenZipFile(input_path, "r") as sz:
                    sz.extractall(extract_dir)
            elif fmt == "rar":
                import subprocess
                subprocess.run(
                    ["unrar", "x", "-o+", str(input_path), str(extract_dir)],
                    check=True, capture_output=True,
                )
            else:
                raise RuntimeError(f"Cannot extract format: {fmt}")

        await asyncio.to_thread(_do)

    async def _compress(self, source_dir: Path, output_path: Path, fmt: str):
        def _do():
            files = list(source_dir.rglob("*"))
            files = [f for f in files if f.is_file()]

            if fmt == "zip":
                with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for f in files:
                        zf.write(f, f.relative_to(source_dir))
            elif fmt in ("tar", "gz", "tgz", "bz2", "xz"):
                mode_map = {
                    "tar": "w:", "gz": "w:gz", "tgz": "w:gz",
                    "bz2": "w:bz2", "xz": "w:xz",
                }
                mode = mode_map.get(fmt, "w:")
                with tarfile.open(output_path, mode) as tf:
                    for f in files:
                        tf.add(f, f.relative_to(source_dir))
            elif fmt == "7z":
                import py7zr
                with py7zr.SevenZipFile(output_path, "w") as sz:
                    for f in files:
                        sz.write(f, f.relative_to(source_dir))
            else:
                raise RuntimeError(f"Cannot compress to format: {fmt}")

        await asyncio.to_thread(_do)
