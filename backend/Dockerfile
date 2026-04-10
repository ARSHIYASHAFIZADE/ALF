FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install system dependencies for file conversion
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    imagemagick \
    ghostscript \
    libmagickwand-dev \
    libpq-dev \
    libpython3.11-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
