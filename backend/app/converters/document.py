import asyncio
import os
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Optional, Callable, Any
from app.converters.base import BaseConverter


def _find_weasyprint() -> Optional[str]:
    # Prefer weasyprint in the same bin dir as the running Python (venv).
    # Falls back to PATH lookup when installed system-wide.
    here = Path(sys.executable).parent
    for name in ("weasyprint", "weasyprint.exe"):
        cand = here / name
        if cand.exists():
            return str(cand)
    return shutil.which("weasyprint")


class DocumentConverter(BaseConverter):
    category = "document"

    supported_input_formats = [
        "pdf", "docx", "doc", "xlsx", "xls", "pptx", "ppt",
        "odt", "ods", "odp", "rtf", "txt", "html", "htm",
        "md", "markdown", "csv", "tsv", "tex", "latex",
        "epub", "xml",
    ]

    supported_output_formats = [
        "pdf", "docx", "xlsx", "pptx", "odt", "ods", "odp",
        "rtf", "txt", "html", "csv", "md", "epub", "tex",
    ]

    async def convert(
        self,
        input_path: Path,
        output_path: Path,
        input_format: str,
        output_format: str,
        progress_callback: Optional[Callable[[int], Any]] = None,
    ) -> Path:
        inp = input_format.lower()
        out = output_format.lower()

        if progress_callback:
            await progress_callback(10)

        # Markdown to other formats via Pandoc
        pandoc_formats = {"md", "markdown", "tex", "latex", "epub", "rst"}
        if inp in pandoc_formats or out in pandoc_formats:
            result = await self._convert_with_pandoc(input_path, output_path, inp, out)
        # PDF input — use dedicated handlers (text extraction) before LibreOffice
        elif inp == "pdf":
            result = await self._convert_pdf(input_path, output_path, inp, out)
        # Office docs via LibreOffice
        elif inp in ("docx", "doc", "xlsx", "xls", "pptx", "ppt", "odt", "ods", "odp", "rtf") or \
             out in ("docx", "xlsx", "pptx", "odt", "ods", "odp", "rtf"):
            result = await self._convert_with_libreoffice(input_path, output_path, inp, out)
        # Other PDF output
        elif out == "pdf":
            result = await self._convert_pdf(input_path, output_path, inp, out)
        # Plain text/HTML/CSV
        else:
            result = await self._convert_text(input_path, output_path, inp, out)

        if progress_callback:
            await progress_callback(100)
        return result

    async def _convert_with_pandoc(
        self, input_path: Path, output_path: Path, inp: str, out: str
    ) -> Path:
        if not shutil.which("pandoc"):
            raise RuntimeError(
                "Pandoc is not installed. Install it from https://pandoc.org or use Docker."
            )
        format_map = {
            "md": "markdown", "markdown": "markdown", "tex": "latex",
            "latex": "latex", "htm": "html", "txt": "plain",
            "docx": "docx", "epub": "epub", "rst": "rst",
            "odt": "odt", "rtf": "rtf", "pdf": "pdf",
        }
        in_fmt = format_map.get(inp, inp)
        out_fmt = format_map.get(out, out)

        cmd = ["pandoc", str(input_path), "-f", in_fmt, "-t", out_fmt, "-o", str(output_path)]

        if out == "pdf":
            # pandoc locates pdf-engine via PATH, so fall back to an absolute
            # path when weasyprint is only installed inside the Python venv.
            weasy = _find_weasyprint()
            cmd.extend([f"--pdf-engine={weasy or 'weasyprint'}"])
            # weasyprint requires a non-empty <title>; supply a default so the
            # conversion doesn't fail when the source has no title metadata
            cmd.extend(["--metadata", f"title={input_path.stem}"])

        def _run():
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                raise RuntimeError(f"Pandoc conversion failed: {result.stderr.decode()}")

        await asyncio.to_thread(_run)

        return output_path

    async def _convert_with_libreoffice(
        self, input_path: Path, output_path: Path, inp: str, out: str
    ) -> Path:
        # LibreOffice needs explicit filter names for reliable conversion.
        # Format is "extension:filter_name" for --convert-to.
        lo_filter_map = {
            "pdf": "pdf:writer_pdf_Export",
            "docx": "docx:MS Word 2007 XML",
            "doc": "doc:MS Word 97",
            "odt": "odt:writer8",
            "rtf": "rtf:Rich Text Format",
            "txt": "txt:Text",
            "html": "html:HTML (StarWriter)",
            "xlsx": "xlsx:Calc MS Excel 2007 XML",
            "xls": "xls:MS Excel 97",
            "ods": "ods:calc8",
            "csv": "csv:Text - txt - csv (StarCalc)",
            "pptx": "pptx:Impress MS PowerPoint 2007 XML",
            "ppt": "ppt:MS PowerPoint 97",
            "odp": "odp:impress8",
        }
        lo_out = lo_filter_map.get(out, out)
        # The plain extension is needed for renaming the output file
        lo_ext = out
        outdir = output_path.parent

        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            # Check common install paths on Windows
            for p in [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]:
                if os.path.isfile(p):
                    soffice = p
                    break
        if not soffice:
            raise RuntimeError(
                "LibreOffice is not installed. Install it from https://www.libreoffice.org or use Docker."
            )

        cmd = [soffice, "--headless"]
        # PDFs open as Draw by default; force Writer import so text export filters work
        if inp == "pdf":
            cmd.extend(["--infilter=writer_pdf_import"])
        cmd.extend(["--convert-to", lo_out, "--outdir", str(outdir), str(input_path)])

        def _run():
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                raise RuntimeError(f"LibreOffice conversion failed: {result.stderr.decode()}")

        await asyncio.to_thread(_run)

        # LibreOffice outputs to outdir with the input filename but new extension
        expected = outdir / f"{input_path.stem}.{lo_ext}"
        if expected.exists() and expected != output_path:
            shutil.move(str(expected), str(output_path))

        return output_path

    def _extract_pdf_text(self, input_path: Path) -> list[str]:
        """Extract text from PDF as a list of paragraphs using PyMuPDF blocks."""
        import fitz
        doc = fitz.open(str(input_path))
        paragraphs = []
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] != 0:  # skip image blocks
                    continue
                lines = block.get("lines", [])
                if not lines:
                    continue
                # Merge all lines in a block — they belong to the same paragraph
                line_texts = []
                for line in lines:
                    span_text = "".join(span["text"] for span in line["spans"])
                    stripped = span_text.strip()
                    if stripped:
                        line_texts.append(stripped)
                full_text = " ".join(line_texts)
                if full_text:
                    paragraphs.append(full_text)
        doc.close()
        return paragraphs

    async def _convert_pdf(
        self, input_path: Path, output_path: Path, inp: str, out: str
    ) -> Path:
        if inp == "pdf" and out == "txt":
            def _extract():
                paragraphs = self._extract_pdf_text(input_path)
                output_path.write_text("\n\n".join(paragraphs), encoding="utf-8")
                return output_path
            return await asyncio.to_thread(_extract)

        if inp == "pdf" and out == "docx":
            def _to_docx():
                from pdf2docx import Converter
                cv = Converter(str(input_path))
                cv.convert(str(output_path))
                cv.close()
                return output_path
            return await asyncio.to_thread(_to_docx)

        if inp == "pdf" and out == "html":
            def _to_html():
                paragraphs = self._extract_pdf_text(input_path)
                body = "\n".join(f"<p>{p}</p>" for p in paragraphs)
                html = f"<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"></head>\n<body>\n{body}\n</body></html>"
                output_path.write_text(html, encoding="utf-8")
                return output_path
            return await asyncio.to_thread(_to_html)

        if inp == "pdf" and out == "odt":
            def _to_odt():
                import zipfile
                paragraphs = self._extract_pdf_text(input_path)
                # Build ODT (ZIP with XML content)
                content_paras = "\n".join(
                    f'<text:p text:style-name="Standard">{p}</text:p>'
                    for p in paragraphs
                )
                content_xml = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"'
                    ' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"'
                    ' office:version="1.2">'
                    '<office:body><office:text>'
                    f'{content_paras}'
                    '</office:text></office:body>'
                    '</office:document-content>'
                )
                manifest_xml = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">'
                    '<manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>'
                    '<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>'
                    '</manifest:manifest>'
                )
                with zipfile.ZipFile(str(output_path), 'w', zipfile.ZIP_DEFLATED) as z:
                    # mimetype must be first and uncompressed
                    z.writestr('mimetype', 'application/vnd.oasis.opendocument.text', compress_type=zipfile.ZIP_STORED)
                    z.writestr('content.xml', content_xml)
                    z.writestr('META-INF/manifest.xml', manifest_xml)
                return output_path
            return await asyncio.to_thread(_to_odt)

        if inp == "pdf" and out == "rtf":
            return await self._convert_with_libreoffice(input_path, output_path, inp, out)

        if out == "pdf":
            return await self._convert_with_libreoffice(input_path, output_path, inp, out)

        raise RuntimeError(f"Unsupported PDF conversion: {inp} -> {out}")

    async def _convert_text(
        self, input_path: Path, output_path: Path, inp: str, out: str
    ) -> Path:
        def _do():
            content = input_path.read_text(encoding="utf-8", errors="replace")

            if inp == "html" and out == "txt":
                import re
                text = re.sub(r"<[^>]+>", "", content)
                output_path.write_text(text, encoding="utf-8")
            elif inp == "csv" and out == "tsv":
                output_path.write_text(content.replace(",", "\t"), encoding="utf-8")
            elif inp == "tsv" and out == "csv":
                output_path.write_text(content.replace("\t", ","), encoding="utf-8")
            elif inp == "txt" and out == "html":
                html = f"<html><body><pre>{content}</pre></body></html>"
                output_path.write_text(html, encoding="utf-8")
            else:
                output_path.write_text(content, encoding="utf-8")

            return output_path

        return await asyncio.to_thread(_do)
