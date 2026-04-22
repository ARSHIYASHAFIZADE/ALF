<div align="center">

# ALF — Ash Loves Files

**A universal file converter supporting 120+ formats across 8 categories**

[![Next.js](https://img.shields.io/badge/Next.js-15.3.1-black?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Free · Private · No sign-up · Files auto-deleted after 1 hour*

</div>

---

## Demo

<div align="center">

![ALF demo — 21 real conversions across all 8 categories with AI insight card](docs/demo.gif)

<sub>21 real conversions across all 8 categories — each preceded by a live AI content summary and format recommendation. <a href="docs/demo.mp4">Download the full MP4</a> (8 MB, 4 min).</sub>

</div>

---

## AI Insights

Every upload is analysed by Llama 3.3 70B (via Groq) before you pick a format. The assistant reads the actual content of the file — not just its extension — and recommends the output format that best fits your likely use case.

<div align="center">
  <img src="docs/ai-insight.png" alt="AI Smart Insight card showing summary, recommended format, alternatives, tips, and a suggested filename" width="560">
</div>

The card surfaces five things per file:

- **Content summary** — what's actually in the file: subject matter, dominant colours, page count, audio bitrate, EPUB title, archive manifest, font glyph count, data schema
- **Recommended format** with a one-line justification (pre-selects the format pill)
- **Alternatives** — two ranked fallbacks, each with their own reason
- **Tips** — format-specific gotchas ("TIFF → JPG loses transparency", "low-bitrate audio won't improve on re-encode")
- **Suggested filename** — a content-aware kebab-case rename for the output file

Set `GROQ_API_KEY` in `backend/.env` to enable it. Free tier available at [console.groq.com](https://console.groq.com).

---

## Features

- **120+ formats** across 8 categories — image, document, audio, video, data, archive, ebook, font
- **AI-powered insight** before every conversion — Llama 3.3 70B reads the file and recommends the right format
- **Drag-and-drop upload** with real-time conversion progress
- **No account required** — upload, convert, download
- **Privacy-first** — files are deleted from the server after 1 hour
- **100 MB upload limit** (configurable)
- **Self-hostable** — one `docker compose up` starts everything

---

## Supported Formats

### Image
| | Formats |
|---|---|
| **Input** | `png` `jpg` `gif` `bmp` `tiff` `webp` `ico` `psd` `pcx` `tga` `ppm` `pgm` `pbm` `heic` `heif` `avif` `svg` `eps` `raw` `cr2` `nef` `arw` `dng` `orf` `rw2` |
| **Output** | `png` `jpg` `gif` `bmp` `tiff` `webp` `ico` `pdf` `eps` `pcx` `tga` `ppm` |

### Document
| | Formats |
|---|---|
| **Input** | `pdf` `docx` `doc` `xlsx` `xls` `pptx` `ppt` `odt` `ods` `odp` `rtf` `txt` `html` `md` `csv` `tsv` `tex` `epub` `xml` |
| **Output** | `pdf` `docx` `xlsx` `pptx` `odt` `ods` `odp` `rtf` `txt` `html` `csv` `md` `epub` `tex` |

### Audio
| | Formats |
|---|---|
| **Input** | `mp3` `wav` `flac` `aac` `ogg` `wma` `m4a` `aiff` `opus` `amr` `ac3` `dts` `ape` `mid` |
| **Output** | `mp3` `wav` `flac` `aac` `ogg` `m4a` `aiff` `opus` `ac3` `wma` |

### Video
| | Formats |
|---|---|
| **Input** | `mp4` `avi` `mkv` `mov` `wmv` `flv` `webm` `mpeg` `3gp` `m4v` `vob` `ts` `mts` `ogv` `asf` `rm` |
| **Output** | `mp4` `avi` `mkv` `mov` `webm` `gif` `mpeg` `3gp` `m4v` `ts` `flv` `ogv` |

### Ebook
| | Formats |
|---|---|
| **Input** | `epub` `mobi` `azw3` `azw` `fb2` `lit` `pdb` `lrf` `cbz` `cbr` |
| **Output** | `epub` `mobi` `azw3` `fb2` `pdf` `txt` `html` `docx` `rtf` |

### Archive
| | Formats |
|---|---|
| **Input** | `zip` `tar` `gz` `tgz` `bz2` `tbz2` `xz` `7z` `rar` |
| **Output** | `zip` `tar` `gz` `tgz` `bz2` `xz` `7z` |

### Data
| | Formats |
|---|---|
| **Input / Output** | `json` `yaml` `toml` `xml` `csv` `tsv` `ini` |

### Font
| | Formats |
|---|---|
| **Input** | `ttf` `otf` `woff` `woff2` `eot` `svg` |
| **Output** | `ttf` `otf` `woff` `woff2` |

---

## Tech Stack

### Frontend

| | |
|---|---|
| Framework | Next.js 15.3.1 (App Router) + React 19 |
| Language | TypeScript 5.8.3 |
| Styling | Tailwind CSS 4.1.4 — zero external UI libraries |

### Backend

| | |
|---|---|
| Framework | FastAPI 0.115.0 + Uvicorn 0.30.6 |
| Language | Python 3.11 |
| Database | SQLAlchemy 2.0 + aiosqlite (async SQLite) |
| Task queue | Celery 5.4 + Redis 7 |

### Conversion Libraries

| Category | Library |
|----------|---------|
| Images | Pillow 10.4 · Wand / ImageMagick (SVG, EPS, PSD, RAW, HEIC) |
| Documents | Pandoc · LibreOffice · PyMuPDF · pdf2docx · WeasyPrint |
| Audio / Video | FFmpeg |
| Office docs | python-docx · python-pptx · openpyxl |
| Ebooks | Calibre (`ebook-convert` CLI) |
| Archives | py7zr · zipfile · tarfile |
| Data formats | PyYAML · toml · xmltodict |
| Fonts | fontTools · Brotli · Zopfli |
| AI insights | Groq SDK · Llama 3.3 70B |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

### Run with Docker

```bash
git clone https://github.com/ARSHIYASHAFIZADE/ALF.git
cd ALF
cp .env.example .env
make dev
```

| URL | Service |
|-----|---------|
| http://localhost:3000 | Frontend |
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | Swagger UI |

To enable AI insights, add your Groq API key to `.env`:

```env
GROQ_API_KEY=your_key_here
```

### Make Commands

```bash
make dev           # Start all services with live logs
make up            # Start in background
make down          # Stop all services
make build         # Rebuild images from scratch
make logs          # Stream all logs
make logs-backend  # API + worker logs only
make clean         # Stop and remove volumes
make shell-backend # Bash shell inside the API container
make test-backend  # Run pytest inside the API container
```

### Local Development (without Docker)

Requires **Redis**, **FFmpeg**, **LibreOffice**, **Pandoc**, **Calibre**, and **ImageMagick** installed locally.

```bash
# Terminal 1 — Backend API
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Celery worker
cd backend
celery -A app.tasks worker --loglevel=info --concurrency=2

# Terminal 3 — Frontend
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

---

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```env
# ── Backend ────────────────────────────────────
DATABASE_URL=sqlite+aiosqlite:///./data/ash.db
REDIS_URL=redis://redis:6379/0

UPLOAD_DIR=/data/uploads
OUTPUT_DIR=/data/outputs
MAX_UPLOAD_SIZE_MB=100

ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_PER_MINUTE=20
CLEANUP_AFTER_HOURS=1

# AI insights (optional — leave blank to disable)
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile

# ── Frontend ───────────────────────────────────
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## API Reference

### Upload & Convert

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a file and specify the output format — returns `jobId` |
| `POST` | `/api/convert/{job_id}` | Start the conversion |
| `GET` | `/api/job/{job_id}` | Poll job status and progress (0–100) |
| `GET` | `/api/download/{job_id}` | Download the converted file |

### AI

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai/analyze-upload` | Analyse a file before creating a job — returns summary, recommended format, alternatives, tips, suggested filename |
| `POST` | `/api/ai/analyze/{job_id}` | Same analysis for an already-uploaded job |

### Formats

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/formats` | All supported formats grouped by category |
| `GET` | `/api/formats/{input_format}` | Available output formats for a given input |
| `GET` | `/api/formats-list` | Flat lists of all input and output formats |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Returns `{"status": "healthy"}` |

Full interactive docs at [`/docs`](http://localhost:8000/docs) (Swagger UI) when the backend is running.

---

## Project Structure

```
ALF/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            # Root layout + metadata
│   │   │   ├── page.tsx              # Main converter page (upload → AI → pick → convert → download)
│   │   │   └── globals.css           # Global styles + CSS variables
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── UploadZone.tsx        # Drag-and-drop file input
│   │   │   ├── FileInfo.tsx          # Uploaded file name + size
│   │   │   ├── AIInsight.tsx         # AI analysis card with typewriter animation
│   │   │   ├── FormatPicker.tsx      # Category tabs + format selection grid
│   │   │   ├── ConversionProgress.tsx # Real-time progress bar
│   │   │   ├── FormatExplorer.tsx    # Browse all 120+ formats by category
│   │   │   ├── HowItWorks.tsx        # Explainer modal
│   │   │   └── Footer.tsx
│   │   └── lib/
│   │       ├── api.ts                # Typed fetch wrappers for all endpoints
│   │       └── formats.ts            # Format metadata (labels, icons, colours)
│   ├── Dockerfile
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI app — CORS, lifespan, route registration
│   │   ├── config.py                 # Pydantic settings (reads .env)
│   │   ├── models.py                 # ConversionJob SQLAlchemy model
│   │   ├── database.py               # Async SQLite engine + session factory
│   │   ├── converters/
│   │   │   ├── base.py               # BaseConverter abstract class
│   │   │   ├── registry.py           # Auto-discovery + format routing
│   │   │   ├── image.py              # Pillow + Wand / ImageMagick
│   │   │   ├── document.py           # Pandoc + LibreOffice + PyMuPDF
│   │   │   ├── audio_video.py        # FFmpeg (Audio and Video classes)
│   │   │   ├── archive.py            # zipfile · tarfile · py7zr
│   │   │   ├── data.py               # JSON · YAML · TOML · XML · CSV · INI
│   │   │   ├── ebook.py              # Calibre ebook-convert CLI
│   │   │   └── font.py               # fontTools
│   │   ├── services/
│   │   │   └── ai.py                 # File preview extraction + Groq/Llama call
│   │   └── routers/
│   │       ├── upload.py
│   │       ├── convert.py
│   │       ├── formats.py
│   │       └── ai.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docs/
│   ├── demo.gif                      # Animated preview (README)
│   ├── demo.mp4                      # Full demo video
│   └── ai-insight.png                # AI card screenshot
│
├── docker-compose.yml                # api · worker · redis · frontend
├── Makefile
└── .env.example
```

---

## How It Works

### Conversion flow

1. **Drop a file** — the frontend calls `POST /api/ai/analyze-upload` immediately; the AI insight card animates in while the format picker loads in parallel
2. **Pick a format** — the AI pre-selects its recommendation; you can override it with any of the 120+ format pills
3. **Upload** — `POST /api/upload` saves the file and creates a `ConversionJob` record (status: `pending`)
4. **Convert** — `POST /api/convert/{job_id}` runs the appropriate converter in a thread pool with real-time progress callbacks
5. **Poll** — the frontend polls `GET /api/job/{job_id}` every second until `completed` or `failed`
6. **Download** — `GET /api/download/{job_id}` streams the output file back
7. **Cleanup** — both input and output files are deleted after 1 hour

### Converter architecture

Each category has one converter class that inherits `BaseConverter` and declares its `supported_input_formats` and `supported_output_formats`. The `ConversionRegistry` auto-discovers all converter classes at startup and routes any format pair to the right handler. To add a new format: create a subclass, add the format strings, done — nothing else changes.

### AI analysis

The `analyze` function in `services/ai.py` extracts a rich preview from each file type (PDF text, DOCX paragraphs, image colour palette + EXIF, audio codec details, EPUB metadata, archive manifest, font glyph count, etc.), then sends it to Llama 3.3 70B via Groq. The model returns structured JSON: summary, recommended format, two alternatives, tips, and a suggested filename. All format values are validated against the actual available output formats before the response is returned.

---

## License

MIT

---

<div align="center">

Built with Next.js · FastAPI · Celery · Redis · Docker

[![GitHub](https://img.shields.io/badge/GitHub-ARSHIYASHAFIZADE%2FALF-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/ARSHIYASHAFIZADE/ALF)

</div>
