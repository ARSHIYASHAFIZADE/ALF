import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase
import enum


class Base(DeclarativeBase):
    pass


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ConversionJob(Base):
    __tablename__ = "conversion_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String, nullable=False)
    input_format = Column(String, nullable=False)
    output_format = Column(String, nullable=False)
    category = Column(String, nullable=False)  # image, document, audio, video, etc.
    status = Column(String, default=JobStatus.PENDING)
    progress = Column(Integer, default=0)  # 0-100
    input_path = Column(String, nullable=False)
    output_path = Column(String, nullable=True)
    output_filename = Column(String, nullable=True)
    file_size = Column(Integer, default=0)  # input file size in bytes
    output_size = Column(Integer, default=0)  # output file size in bytes
    error_message = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "originalFilename": self.original_filename,
            "inputFormat": self.input_format,
            "outputFormat": self.output_format,
            "category": self.category,
            "status": self.status,
            "progress": self.progress,
            "outputFilename": self.output_filename,
            "fileSize": self.file_size,
            "outputSize": self.output_size,
            "errorMessage": self.error_message,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "completedAt": self.completed_at.isoformat() if self.completed_at else None,
        }
