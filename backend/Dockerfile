FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install ALL system dependencies needed for:
# - Wand (ImageMagick)
# - WeasyPrint (GTK, Cairo, Pango)
# - File conversion tools (ffmpeg, ghostscript)
# - Build tools for C extensions
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    pkg-config \
    # ImageMagick + Wand
    imagemagick \
    libmagickwand-dev \
    # WeasyPrint dependencies (GTK/Cairo/Pango)
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    # File conversion tools
    ffmpeg \
    ghostscript \
    # Archive support
    p7zip-full \
    # Fonts for WeasyPrint
    fonts-dejavu-core \
    # Remove apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, wheel, setuptools
RUN pip install --upgrade pip setuptools wheel

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
