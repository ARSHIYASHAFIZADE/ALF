FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install ALL system dependencies upfront
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    imagemagick \
    libmagickwand-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    ffmpeg \
    ghostscript \
    p7zip-full \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade core pip packages
RUN pip install --upgrade pip setuptools wheel

# Install in groups to identify issues
# Group 1: Core FastAPI
RUN pip install \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.6 \
    python-multipart==0.0.9

# Group 2: Database
RUN pip install \
    sqlalchemy==2.0.35 \
    aiosqlite==0.20.0

# Group 3: Async utilities
RUN pip install \
    aiofiles==24.1.0 \
    httpx==0.27.2

# Group 4: Data formats
RUN pip install \
    pydantic==2.9.2 \
    pydantic-settings==2.5.2 \
    PyYAML==6.0.2 \
    toml==0.10.2 \
    xmltodict==0.13.0 \
    dicttoxml==1.7.16 \
    markdown==3.7

# Group 5: Document processing
RUN pip install \
    python-pptx==1.0.2 \
    python-docx==1.1.2 \
    openpyxl==3.1.5 \
    pypdf==4.3.1

# Group 6: Image processing (might need compilation)
RUN pip install \
    Pillow==10.4.0 \
    fonttools==4.54.1 \
    brotli==1.1.0 \
    zopfli==0.2.3

# Group 7: Binary magic (file type detection)
RUN pip install \
    python-magic-bin==0.4.14

# Group 8: ImageMagick wrapper (Wand)
RUN pip install \
    Wand==0.6.13

# Group 9: WeasyPrint for PDF generation
RUN pip install \
    weasyprint==62.3

# Group 10: Archive support
RUN pip install \
    py7zr==0.22.0

# Group 11: Celery + Redis
RUN pip install \
    celery==5.4.0 \
    redis==5.1.1

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
