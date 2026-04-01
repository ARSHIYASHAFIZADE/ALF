from app.converters.base import BaseConverter
from app.converters.image import ImageConverter
from app.converters.document import DocumentConverter
from app.converters.audio_video import AudioConverter, VideoConverter
from app.converters.archive import ArchiveConverter
from app.converters.data import DataConverter
from app.converters.ebook import EbookConverter
from app.converters.font import FontConverter


class ConversionRegistry:
    """Central registry of all converters. Handles format routing."""

    def __init__(self):
        self.converters: list[BaseConverter] = [
            ImageConverter(),
            DocumentConverter(),
            AudioConverter(),
            VideoConverter(),
            ArchiveConverter(),
            DataConverter(),
            EbookConverter(),
            FontConverter(),
        ]

    def find_converter(self, input_format: str, output_format: str) -> BaseConverter | None:
        inp = input_format.lower().lstrip(".")
        out = output_format.lower().lstrip(".")
        for converter in self.converters:
            if converter.can_convert(inp, out):
                return converter
        return None

    def get_supported_formats(self) -> dict:
        """Returns all supported formats grouped by category."""
        formats = {}
        for converter in self.converters:
            cat = converter.category
            if cat not in formats:
                formats[cat] = {"input": set(), "output": set()}
            formats[cat]["input"].update(converter.supported_input_formats)
            formats[cat]["output"].update(converter.supported_output_formats)

        # Convert sets to sorted lists
        return {
            cat: {
                "input": sorted(list(fmts["input"])),
                "output": sorted(list(fmts["output"])),
            }
            for cat, fmts in formats.items()
        }

    def get_output_formats_for(self, input_format: str) -> dict[str, list[str]]:
        """Given an input format, return all possible output formats grouped by category."""
        inp = input_format.lower().lstrip(".")
        result = {}
        for converter in self.converters:
            if inp in converter.supported_input_formats:
                cat = converter.category
                if cat not in result:
                    result[cat] = []
                result[cat].extend(converter.supported_output_formats)
        # Deduplicate
        return {cat: sorted(list(set(fmts))) for cat, fmts in result.items()}

    def get_all_input_formats(self) -> list[str]:
        all_formats = set()
        for converter in self.converters:
            all_formats.update(converter.supported_input_formats)
        return sorted(list(all_formats))

    def get_all_output_formats(self) -> list[str]:
        all_formats = set()
        for converter in self.converters:
            all_formats.update(converter.supported_output_formats)
        return sorted(list(all_formats))


_registry = None


def get_registry() -> ConversionRegistry:
    global _registry
    if _registry is None:
        _registry = ConversionRegistry()
    return _registry
