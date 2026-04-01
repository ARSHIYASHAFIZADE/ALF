import asyncio
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


class FontConverter(BaseConverter):
    category = "font"

    supported_input_formats = [
        "ttf", "otf", "woff", "woff2", "eot", "svg",
    ]

    supported_output_formats = [
        "ttf", "otf", "woff", "woff2",
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
            await progress_callback(20)

        out = output_format.lower()

        def _do():
            from fontTools.ttLib import TTFont

            font = TTFont(str(input_path))

            if out == "woff":
                font.flavor = "woff"
            elif out == "woff2":
                font.flavor = "woff2"
            elif out in ("ttf", "otf"):
                font.flavor = None

            font.save(str(output_path))
            return output_path

        result = await asyncio.to_thread(_do)

        if progress_callback:
            await progress_callback(100)

        return result
