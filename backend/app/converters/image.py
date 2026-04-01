import asyncio
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


class ImageConverter(BaseConverter):
    category = "image"

    supported_input_formats = [
        "png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif", "webp",
        "ico", "psd", "pcx", "tga", "ppm", "pgm", "pbm", "heic",
        "heif", "avif", "svg", "eps", "raw", "cr2", "nef", "arw",
        "dng", "orf", "rw2",
    ]

    supported_output_formats = [
        "png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif", "webp",
        "ico", "pdf", "eps", "pcx", "tga", "ppm",
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

        # Use ImageMagick (via Wand) for complex formats like SVG, EPS, PSD, RAW
        complex_inputs = {"svg", "eps", "psd", "raw", "cr2", "nef", "arw", "dng", "orf", "rw2", "heic", "heif", "avif"}

        if inp in complex_inputs:
            result = await self._convert_with_imagemagick(input_path, output_path, inp, out)
        else:
            result = await self._convert_with_pillow(input_path, output_path, inp, out)

        if progress_callback:
            await progress_callback(100)

        return result

    async def _convert_with_pillow(
        self, input_path: Path, output_path: Path, inp: str, out: str
    ) -> Path:
        def _do_convert():
            from PIL import Image

            img = Image.open(input_path)

            # Handle RGBA to RGB for formats that don't support alpha
            if out in ("jpg", "jpeg", "bmp", "eps", "pcx") and img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                img = background

            # Handle ICO output
            if out == "ico":
                sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
                img.save(output_path, format="ICO", sizes=sizes)
            elif out == "pdf":
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(output_path, format="PDF")
            else:
                format_map = {
                    "jpg": "JPEG", "jpeg": "JPEG", "tif": "TIFF", "tiff": "TIFF",
                }
                save_format = format_map.get(out, out.upper())
                save_kwargs = {}
                if out in ("jpg", "jpeg"):
                    save_kwargs["quality"] = 95
                elif out == "webp":
                    save_kwargs["quality"] = 90
                elif out == "png":
                    save_kwargs["optimize"] = True
                img.save(output_path, format=save_format, **save_kwargs)

            return output_path

        return await asyncio.to_thread(_do_convert)

    async def _convert_with_imagemagick(
        self, input_path: Path, output_path: Path, inp: str, out: str
    ) -> Path:
        def _do_convert():
            try:
                from wand.image import Image
            except ImportError:
                raise RuntimeError(
                    "ImageMagick is not installed. Install it from https://imagemagick.org or use Docker."
                )

            with Image(filename=str(input_path)) as img:
                if out in ("jpg", "jpeg") and img.alpha_channel:
                    img.background_color = "white"
                    img.alpha_channel = "remove"
                img.format = out if out not in ("jpg",) else "jpeg"
                img.save(filename=str(output_path))

            return output_path

        return await asyncio.to_thread(_do_convert)
