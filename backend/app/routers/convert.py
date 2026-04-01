import os
from pathlib import Path
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import ConversionJob, JobStatus
from app.converters import get_registry

router = APIRouter(prefix="/api", tags=["convert"])


@router.post("/convert/{job_id}")
async def start_conversion(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ConversionJob).where(ConversionJob.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != JobStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Job is already {job.status}")

    # Start conversion
    registry = get_registry()
    converter = registry.find_converter(job.input_format, job.output_format)

    if not converter:
        job.status = JobStatus.FAILED
        job.error_message = "No converter found for this format pair"
        await db.commit()
        raise HTTPException(status_code=400, detail="No converter available")

    job.status = JobStatus.PROCESSING
    job.progress = 0
    await db.commit()

    try:
        async def update_progress(pct: int):
            job.progress = pct
            await db.commit()

        input_path = Path(job.input_path)
        output_path = Path(job.output_path)

        await converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format=job.input_format,
            output_format=job.output_format,
            progress_callback=update_progress,
        )

        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.completed_at = datetime.now(timezone.utc)

        if output_path.exists():
            job.output_size = output_path.stat().st_size

        await db.commit()

        return job.to_dict()

    except Exception as e:
        error_msg = str(e) or f"{type(e).__name__}: Unknown error"
        job.status = JobStatus.FAILED
        job.error_message = error_msg[:1000]
        job.completed_at = datetime.now(timezone.utc)
        await db.commit()

        raise HTTPException(status_code=500, detail=f"Conversion failed: {error_msg[:200]}")


@router.get("/job/{job_id}")
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ConversionJob).where(ConversionJob.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job.to_dict()


@router.get("/download/{job_id}")
async def download_file(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ConversionJob).where(ConversionJob.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="File is not ready for download")

    output_path = Path(job.output_path)
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found (may have been cleaned up)")

    return FileResponse(
        path=str(output_path),
        filename=job.output_filename,
        media_type="application/octet-stream",
    )
