FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install all required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    imagemagick \
    ghostscript \
    libmagickwand-dev \
    libpq-dev \
    zlib1g-dev \
    libjpeg-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
