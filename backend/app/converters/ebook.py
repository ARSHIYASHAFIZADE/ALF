import asyncio
import os
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

        # Calibre's shebang resolves `env python3` through PATH, so if a
        # pyenv/venv shim sits ahead of /usr/bin the wrong interpreter runs
        # (and Calibre's C-extension deps like msgpack go missing). Put
        # system python first, and force a UTF-8 locale so the translation
        # layer finds its message catalogs.
        system_path = "/usr/local/bin:/usr/bin:/bin"
        existing = os.environ.get("PATH", "")
        env = {
            **os.environ,
            "PATH": f"{system_path}:{existing}" if existing else system_path,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
        }

        def _run():
            result = subprocess.run(cmd, capture_output=True, env=env)
            if result.returncode != 0:
                raise RuntimeError(f"Calibre conversion failed: {result.stderr.decode()[-500:]}")

        await asyncio.to_thread(_run)

        if progress_callback:
            await progress_callback(90)

        if progress_callback:
            await progress_callback(100)

        return output_path
