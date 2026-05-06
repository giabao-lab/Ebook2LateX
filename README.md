# Ebook2LateX

Project scaffold for extracting mathematical formulas from PDFs and converting to LaTeX.

This README covers quick setup for the Parse tool (3.2) using either a local `pix2tex` model or the Mathpix API as a fallback.

## Quick start (local development)

Prerequisites:
- Python 3.11+ (project tested on 3.11+)
- Node 18+ (for frontend development)
- Docker & Docker Compose (optional, see below)

Backend setup (local Python):

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend requirements:

```powershell
pip install -r backend/requirements.txt
```

3. Configure `.env` in `backend/.env`. You can provide Mathpix credentials to use the Mathpix API as a fallback:

```
DATABASE_URL=postgresql+psycopg2://postgres:123asd@localhost:5432/ebook2latex_db
MATHPIX_APP_ID=
MATHPIX_APP_KEY=
UPLOAD_DIR=uploads
```

4. Run the API locally:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
uvicorn app.main:app --reload
```

If PowerShell says `uvicorn` is not recognized, run it through the virtual environment instead:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

You can also use the helper script:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
.\run_backend.ps1
```

(Note: the project includes a small CLI to run the parse pipeline directly without starting the HTTP server.)

Run Parse CLI:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
python tools/run_parse.py path/to/sample.pdf
```

This will extract images to `backend/uploads/<pdfname>_extracted` and print LaTeX outputs.

## pix2tex vs Mathpix

- pix2tex: a local LaTeX-OCR model (high quality) but heavy: requires installing model weights and possibly `torch`/`cuda` for best performance. If you intend to run locally with pix2tex, install its dependencies separately and ensure you can `from pix2tex.cli import LatexOCR` in Python.

- Mathpix API: a hosted solution requiring `MATHPIX_APP_ID` and `MATHPIX_APP_KEY`. It's easy to integrate (HTTP requests) and is used as a fallback when the local model is unavailable. Beware of usage quotas and costs.

## Docker

The repository includes `docker-compose.yml` that defines services: `db` (Postgres), `backend`, and `frontend`. To bring the system up:

```powershell
docker compose up --build
```

This will start Postgres and the backend; ensure `.env` values are compatible with the compose settings (the compose file sets DB URL for backend to use the `db` container).

## Next steps

- Implement improved formula region detection (currently all page images are extracted).
- Add tests and sample PDFs for quality checks.
- Optionally add GitHub Actions to run lint/tests on push.

## Database migrations (Alembic)

This project includes Alembic for creating and versioning the PostgreSQL schema.

1. Activate a Python environment and install dependencies:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Apply the initial migration to create the tables:

```powershell
alembic upgrade head
```

3. If you change the SQLAlchemy models later, generate a new migration:

```powershell
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

Relevant files:
- [backend/alembic.ini](backend/alembic.ini)
- [backend/migrations/env.py](backend/migrations/env.py)
- [backend/migrations/versions/0001_initial_schema.py](backend/migrations/versions/0001_initial_schema.py)

## Seeding sample data

After running the migration, you can insert sample records into `users`, `documents`, `formula_entries`, and `logs`:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
python seed.py
```

The seed script is idempotent: if you run it again, it reuses the existing sample rows instead of creating duplicate users.

## Web services / FastAPI

The backend exposes web services that the React frontend can call over HTTP.

Quick run from the `backend` folder:

```powershell
cd "c:\Users\HELLO\OneDrive\Desktop\EBOOK2LATEX\backend"
uvicorn main:app --reload
```

Useful endpoints:
- `GET /` returns the welcome message
- `GET /api/health` returns `{"status": "ok"}`
- `POST /api/upload` accepts a PDF file
- `POST /api/process/{document_id}` runs the parse/OCR pipeline

In this project, React acts as the client and FastAPI acts as the web service provider, which matches the client-server model described in the lesson.

Frontend demo tip: open the app and click the green `Kiểm tra FastAPI` button to call `GET /api/health`.
