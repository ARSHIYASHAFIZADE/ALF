from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Callable, Any


class BaseConverter(ABC):
    """Base class for all file converters."""

    @property
    @abstractmethod
    def supported_input_formats(self) -> list[str]:
        """List of supported input format extensions (without dot)."""
        ...

    @property
    @abstractmethod
    def supported_output_formats(self) -> list[str]:
        """List of supported output format extensions (without dot)."""
        ...

    @property
    @abstractmethod
    def category(self) -> str:
        """Category name: image, document, audio, video, archive, data, ebook, font, vector"""
        ...

    def can_convert(self, input_format: str, output_format: str) -> bool:
        return (
            input_format.lower() in self.supported_input_formats
            and output_format.lower() in self.supported_output_formats
        )

    @abstractmethod
    async def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str,
        output_format: str,
        progress_callback: Optional[Callable[[int], Any]] = None,
    ) -> Path:
        """
        Convert a file from input_format to output_format.
        Returns the path to the converted file.
        The progress_callback may be async — always await it.
        """
        ...
