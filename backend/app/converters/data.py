import asyncio
import json
import csv
import io
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


class DataConverter(BaseConverter):
    category = "data"

    supported_input_formats = [
        "json", "yaml", "yml", "toml", "xml", "csv", "tsv", "ini",
    ]

    supported_output_formats = [
        "json", "yaml", "yml", "toml", "xml", "csv", "tsv", "ini",
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

        inp = input_format.lower()
        out = output_format.lower()

        def _do():
            # Step 1: Parse input to Python object
            data = self._parse(input_path, inp)

            # Step 2: Serialize to output
            self._serialize(data, output_path, out)

            return output_path

        result = await asyncio.to_thread(_do)

        if progress_callback:
            await progress_callback(100)

        return result

    def _parse(self, path: Path, fmt: str):
        content = path.read_text(encoding="utf-8", errors="replace")

        if fmt == "json":
            return json.loads(content)
        elif fmt in ("yaml", "yml"):
            import yaml
            return yaml.safe_load(content)
        elif fmt == "toml":
            import toml
            return toml.loads(content)
        elif fmt == "xml":
            import xmltodict
            return xmltodict.parse(content)
        elif fmt in ("csv", "tsv"):
            delimiter = "\t" if fmt == "tsv" else ","
            reader = csv.DictReader(io.StringIO(content), delimiter=delimiter)
            return list(reader)
        elif fmt == "ini":
            import configparser
            parser = configparser.ConfigParser()
            parser.read_string(content)
            return {s: dict(parser[s]) for s in parser.sections()}
        else:
            raise RuntimeError(f"Cannot parse format: {fmt}")

    def _serialize(self, data, path: Path, fmt: str):
        if fmt == "json":
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        elif fmt in ("yaml", "yml"):
            import yaml
            path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")
        elif fmt == "toml":
            import toml
            path.write_text(toml.dumps(data), encoding="utf-8")
        elif fmt == "xml":
            from dicttoxml import dicttoxml
            xml_bytes = dicttoxml(data, custom_root="root", attr_type=False)
            path.write_bytes(xml_bytes)
        elif fmt in ("csv", "tsv"):
            if not isinstance(data, list):
                raise RuntimeError("Data must be a list of objects to convert to CSV/TSV")
            delimiter = "\t" if fmt == "tsv" else ","
            if data:
                keys = list(data[0].keys()) if isinstance(data[0], dict) else []
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=keys, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
                path.write_text(output.getvalue(), encoding="utf-8")
            else:
                path.write_text("", encoding="utf-8")
        elif fmt == "ini":
            import configparser
            parser = configparser.ConfigParser()
            if isinstance(data, dict):
                for section, values in data.items():
                    if isinstance(values, dict):
                        parser[section] = {k: str(v) for k, v in values.items()}
            with open(path, "w", encoding="utf-8") as f:
                parser.write(f)
        else:
            raise RuntimeError(f"Cannot serialize to format: {fmt}")
