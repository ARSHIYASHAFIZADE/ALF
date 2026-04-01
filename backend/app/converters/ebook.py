import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


class EbookConverter(BaseConverter):
    category = "ebook"

    supported_input_formats = [
        "epub", "mobi", "azw3", "azw", "fb2", "lit", "pdb",
        "lrf", "tcr", "snb", "cbz", "cbr",
    ]

    supported_output_formats = [
        "epub", "mobi", "azw3", "fb2", "pdf", "txt", "html",
        "docx", "rtf",
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

        # Use Calibre's ebook-convert CLI
        ebook_convert = shutil.which("ebook-convert")
        if not ebook_convert:
            raise RuntimeError(
                "Calibre's ebook-convert not found. Please install Calibre: https://calibre-ebook.com"
            )

        cmd = [ebook_convert, str(input_path), str(output_path)]

        def _run():
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                raise RuntimeError(f"Calibre conversion failed: {result.stderr.decode()[-500:]}")

        await asyncio.to_thread(_run)

        if progress_callback:
            await progress_callback(90)

        if progress_callback:
            await progress_callback(100)

        return output_path
