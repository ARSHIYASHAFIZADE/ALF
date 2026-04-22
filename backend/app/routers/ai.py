"""AI-powered endpoints: per-file content summary + smart format recommendation."""
from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.converters import get_registry
from app.database import get_db
from app.models import ConversionJob
from app.services.ai import analyze, extract_preview

router = APIRouter(prefix="/api/ai", tags=["ai"])


def _category_for_input(input_format: str) -> str:
    """Find which converter category owns this input format.

    Ambiguous formats (epub is claimed by both document + ebook converters)
    resolve to the more specialised category so the right extractor runs.
    """
    ebook_formats = {
        "epub", "mobi", "azw3", "azw", "fb2", "lit", "pdb",
        "lrf", "tcr", "snb", "cbz", "cbr",
    }
    if input_format in ebook_formats:
        return "ebook"
    registry = get_registry()
    for conv in registry.converters:
        if input_format in conv.supported_input_formats:
            return conv.category
    return "document"


@router.post("/analyze/{job_id}")
async def analyze_job(job_id: str, db: AsyncSession = Depends(get_db)):
    """Summarise the uploaded file and recommend the best output format(s)."""
    result = await db.execute(select(ConversionJob).where(ConversionJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    input_path = Path(job.input_path)
    if not input_path.exists():
        raise HTTPException(status_code=410, detail="Uploaded file no longer available")

    registry = get_registry()
    outputs_by_cat = registry.get_output_formats_for(job.input_format)
    # Flatten to a single list of possible output formats for this input,
    # excluding the input format itself (same-format "conversion" is blocked).
    available: list[str] = []
    for fmts in outputs_by_cat.values():
        for f in fmts:
            if f != job.input_format and f not in available:
                available.append(f)

    if not available:
        raise HTTPException(status_code=400, detail="No output formats available for this input")

    # Content extraction + model call are both blocking — run in a thread
    def _work():
        preview = extract_preview(input_path, job.input_format, job.category)
        return preview, analyze(
            filename=job.original_filename,
            input_format=job.input_format,
            file_size=job.file_size,
            category=job.category,
            available_output_formats=available,
            preview=preview,
        )

    preview, insight = await asyncio.to_thread(_work)

    return {
        "jobId": job_id,
        "category": job.category,
        "inputFormat": job.input_format,
        "availableOutputFormats": available,
        "preview": preview[:800],  # truncate for wire
        **insight,
    }


@router.post("/analyze-upload")
async def analyze_upload(file: UploadFile = File(...)):
    """Analyze a file before it's officially uploaded — the frontend can call
    this right after file drop to get a fast AI insight, in parallel with
    the format picker loading. No DB job is created."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    input_format = Path(file.filename).suffix.lower().lstrip(".")
    if not input_format:
        raise HTTPException(status_code=400, detail="Cannot determine file format")

    registry = get_registry()
    category = _category_for_input(input_format)
    outputs_by_cat = registry.get_output_formats_for(input_format)
    available: list[str] = []
    for fmts in outputs_by_cat.values():
        for f in fmts:
            if f != input_format and f not in available:
                available.append(f)
    if not available:
        raise HTTPException(
            status_code=400,
            detail=f"No output formats available for .{input_format}",
        )

    # Stream to a temp file so extractors can work against an on-disk path
    content = await file.read()
    with tempfile.NamedTemporaryFile(
        suffix=f".{input_format}", delete=True
    ) as tmp:
        tmp.write(content)
        tmp.flush()
        tmp_path = Path(tmp.name)

        def _work():
            preview = extract_preview(tmp_path, input_format, category)
            return preview, analyze(
                filename=file.filename,
                input_format=input_format,
                file_size=len(content),
                category=category,
                available_output_formats=available,
                preview=preview,
            )

        preview, insight = await asyncio.to_thread(_work)

    return {
        "category": category,
        "inputFormat": input_format,
        "availableOutputFormats": available,
        "preview": preview[:800],
        **insight,
    }
