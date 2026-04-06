# ALF — Ash Loves Files

A universal file converter supporting 120+ formats across 8 categories. Free, private, no sign-up required.

**Live:** convert any image, document, audio, video, ebook, archive, data, or font file — instantly in your browser.

---

## Features

- **120+ formats** across 8 categories: Image, Document, Audio, Video, Ebook, Archive, Data, Font
- **Drag-and-drop upload** up to 100 MB
- **Real-time progress** with file size comparison
- **No account required** — files auto-deleted after 1 hour
- **Format explorer** — browse all supported input/output combinations
- **Fully containerized** — all conversion tools bundled in Docker

---

## Supported Formats

### Image
| | Formats |
|---|---|
| **Input** | png, jpg, gif, bmp, tiff, webp, ico, psd, pcx, tga, ppm, pgm, pbm, heic, heif, avif, svg, eps, raw, cr2, nef, arw, dng, orf, rw2 |
| **Output** | png, jpg, gif, bmp, tiff, webp, ico, pdf, eps, pcx, tga, ppm |

### Document
| | Formats |
|---|---|
| **Input** | pdf, docx, doc, xlsx, xls, pptx, ppt, odt, ods, odp, rtf, txt, html, md, csv, tsv, tex, epub, xml |
| **Output** | pdf, docx, xlsx, pptx, odt, ods, odp, rtf, txt, html, csv, md, epub, tex |

### Audio
| | Formats |
|---|---|
| **Input** | mp3, wav, flac, aac, ogg, wma, m4a, aiff, opus, amr, ac3, dts, ape, mid |
| **Output** | mp3, wav, flac, aac, ogg, m4a, aiff, opus, ac3, wma |

### Video
| | Formats |
|---|---|
| **Input** | mp4, avi, mkv, mov, wmv, flv, webm, mpeg, 3gp, m4v, vob, ts, mts, ogv, asf, rm |
| **Output** | mp4, avi, mkv, mov, webm, gif, mpeg, 3gp, m4v, ts, flv, ogv |

### Ebook
| | Formats |
|---|---|
| **Input** | epub, mobi, azw3, azw, fb2, lit, pdb, lrf, cbz, cbr |
| **Output** | epub, mobi, azw3, fb2, pdf, txt, html, docx, rtf |

### Archive
| | Formats |
|---|---|
| **Input** | zip, tar, gz, tgz, bz2, tbz2, xz, 7z, rar |
| **Output** | zip, tar, gz, tgz, bz2, xz, 7z |

### Data
| | Formats |
|---|---|
| **Input/Output** | json, yaml, toml, xml, csv, tsv, ini |

### Font
| | Formats |
|---|---|
| **Input** | ttf, otf, woff, woff2, eot, svg |
| **Output** | ttf, otf, woff, woff2 |

---

## Tech Stack

### Frontend
| | |
|---|---|
| **Framework** | Next.js 15 (App Router) |
| **UI** | React 19, Tailwind CSS 4, TypeScript 5 |

### Backend
| | |
|---|---|
| **Framework** | FastAPI + Uvicorn |
| **Language** | Python 3.12 |
| **Task Queue** | Celery + Redis |
| **Database** | SQLite (async via SQLAlchemy + aiosqlite) |

### Conversion Tools
| Category | Tool |
|---|---|
| Images | Pillow, ImageMagick (Wand) |
| Audio / Video | FFmpeg |
| Documents | LibreOffice, Pandoc, python-docx, python-pptx, openpyxl, PyPDF, WeasyPrint |
| Ebooks | Calibre (`ebook-convert`) |
| Archives | py7zr |
| Data | PyYAML, toml, xmltodict |
| Fonts | fontTools |

### Infrastructure
| | |
|---|---|
| **Containerization** | Docker + Docker Compose |
| **Services** | `api`, `worker`, `redis`, `frontend` |
| **Storage** | Docker volumes (`file_data`, `redis_data`) |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- `make` (optional, for convenience commands)

### Run with Docker (recommended)

```bash
git clone https://github.com/ARSHIYASHAFIZADE/ALF.git
cd ALF
cp .env.example .env
make dev
```

App available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Other make commands

```bash
make up          # Run in background
make down        # Stop all services
make logs        # Stream all logs
make logs-backend   # Backend logs only
make logs-frontend  # Frontend logs only
make clean       # Stop and remove volumes
```

### Local Development (without Docker)

You'll need Redis, FFmpeg, LibreOffice, Pandoc, and Calibre installed locally.

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Worker (separate terminal)
cd backend
celery -A app.tasks worker --loglevel=info --concurrency=2

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

```env
# Backend
REDIS_URL=redis://redis:6379/0
DATABASE_URL=sqlite+aiosqlite:///./data/ash.db
UPLOAD_DIR=/data/uploads
OUTPUT_DIR=/data/outputs
MAX_UPLOAD_SIZE_MB=100
ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_PER_MINUTE=20
CLEANUP_AFTER_HOURS=1

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## API Reference

### Upload & Convert

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a file and select output format |
| `POST` | `/api/convert/{job_id}` | Start conversion for a job |
| `GET` | `/api/job/{job_id}` | Poll job status and progress |
| `GET` | `/api/download/{job_id}` | Download the converted file |

### Formats

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/formats` | All formats grouped by category |
| `GET` | `/api/formats/{input_format}` | Available output formats for a given input |
| `GET` | `/api/formats-list` | Flat lists of all input and output formats |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |

Full interactive docs at `/docs` (Swagger) or `/redoc` when the backend is running.

---

## Project Structure

```
ALF/
├── frontend/                    # Next.js app
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout + metadata
│   │   │   ├── page.tsx         # Main converter page
│   │   │   └── globals.css      # Global styles + theme
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── UploadZone.tsx   # Drag-and-drop upload
│   │   │   ├── FormatPicker.tsx # Category tabs + format selection
│   │   │   ├── ConversionProgress.tsx
│   │   │   ├── FormatExplorer.tsx
│   │   │   ├── HowItWorks.tsx
│   │   │   └── Footer.tsx
│   │   └── lib/
│   │       ├── api.ts           # API client
│   │       └── formats.ts       # Format metadata
│   └── Dockerfile
│
├── backend/                     # FastAPI app
│   ├── app/
│   │   ├── main.py              # App setup + routes
│   │   ├── config.py            # Settings
│   │   ├── models.py            # ConversionJob DB model
│   │   ├── converters/
│   │   │   ├── base.py          # BaseConverter abstract class
│   │   │   ├── registry.py      # Converter registry
│   │   │   ├── image.py
│   │   │   ├── document.py
│   │   │   ├── audio_video.py
│   │   │   ├── archive.py
│   │   │   ├── data.py
│   │   │   ├── ebook.py
│   │   │   └── font.py
│   │   └── routers/
│   │       ├── upload.py
│   │       ├── convert.py
│   │       └── formats.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## How Conversion Works

1. **Upload** — file is sent to `/api/upload`, saved to disk, a `ConversionJob` record is created in SQLite
2. **Convert** — `/api/convert/{job_id}` starts the conversion in a thread pool; progress is updated in real time
3. **Poll** — frontend polls `/api/job/{job_id}` until status is `completed` or `failed`
4. **Download** — `/api/download/{job_id}` streams the output file back
5. **Cleanup** — files are automatically deleted after 1 hour

Each converter inherits from `BaseConverter` and is auto-registered at startup via `ConversionRegistry`. Adding a new format means creating a subclass and registering it — nothing else needs to change.

---

## License

MIT
