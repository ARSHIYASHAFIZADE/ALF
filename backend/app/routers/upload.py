import uuid
import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import get_db
from app.models import ConversionJob, JobStatus
from app.converters import get_registry

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    output_format: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not output_format:
        raise HTTPException(status_code=400, detail="Output format is required")

    # Get input format from filename
    ext = Path(file.filename).suffix.lower().lstrip(".")
    if not ext:
        raise HTTPException(status_code=400, detail="Cannot determine file format")

    output_format = output_format.lower().lstrip(".")

    # Prevent same-format conversion
    if ext == output_format:
        raise HTTPException(
            status_code=400,
            detail=f"Input and output format are both .{ext}. Please choose a different output format.",
        )

    # Check if conversion is supported
    registry = get_registry()
    converter = registry.find_converter(ext, output_format)
    if not converter:
        raise HTTPException(
            status_code=400,
            detail=f"Conversion from .{ext} to .{output_format} is not supported",
        )

    # Read file content
    content = await file.read()
    file_size = len(content)

    if file_size > settings.max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    # Save uploaded file
    job_id = str(uuid.uuid4())
    upload_dir = Path(settings.UPLOAD_DIR) / job_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    input_path = upload_dir / file.filename
    input_path.write_bytes(content)

    # Create output filename
    output_filename = f"{Path(file.filename).stem}.{output_format}"
    output_dir = Path(settings.OUTPUT_DIR) / job_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename

    # Create job record
    job = ConversionJob(
        id=job_id,
        original_filename=file.filename,
        input_format=ext,
        output_format=output_format,
        category=converter.category,
        status=JobStatus.PENDING,
        input_path=str(input_path),
        output_path=str(output_path),
        output_filename=output_filename,
        file_size=file_size,
        ip_address=request.client.host if request.client else None,
    )
    db.add(job)
    await db.commit()

    return {"jobId": job_id, "status": "pending"}
