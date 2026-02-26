# Sentinel

Sentinel is an ML data quality platform that analyzes tabular datasets before model training.  
It detects leakage risk, missing data patterns, class imbalance, outliers, and structural issues, then returns an actionable report and a sentinel score.

## What It Does

- Upload CSV datasets and trigger analysis automatically.
- Run analyzer pipeline for:
  - basic dataset stats
  - missing value diagnostics
  - categorical feature checks
  - class imbalance diagnostics
  - leakage heuristics
  - outlier detection
- Track dataset processing status (`uploaded -> processing -> completed/failed`).
- View analysis reports with sectioned insights and recommendations.
- Support guest sessions and authenticated users (Supabase auth).
- Provide history for logged-in users in the Analyses page.

## Tech Stack

### Frontend
- React + TypeScript + Vite
- Tailwind CSS
- shadcn/ui primitives
- Supabase JS client

### Backend
- FastAPI
- SQLAlchemy
- Pandas
- PostgreSQL (production) / SQLite (local fallback)
- Background processing via FastAPI `BackgroundTasks`

### Infrastructure
- Frontend: Vercel
- Backend: Render
- Database: Neon Postgres
- Auth: Supabase

## Repository Structure

```text
.
├── frontend/        # Vite React app
├── backend/         # FastAPI API + analysis engine
├── docs/            # project docs
└── README.md
```

## Local Development

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend default URL: `http://localhost:8000`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend default URL: `http://localhost:5173`

## Environment Variables

### Backend (`backend/.env`)

Required:

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_JWT_SECRET`

Optional:

- `APP_NAME` (default: `SentinelAI`)
- `CORS_ALLOW_ORIGINS` (comma-separated origins)
- `CORS_ALLOW_ORIGIN_REGEX`

Reference templates:

- `backend/.env.example`
- `backend/.env.render.example`

### Frontend (`frontend/.env`)

- `VITE_API_URL`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## API Overview

### Datasets
- `POST /datasets/upload` - upload CSV + create dataset + queue analysis
- `GET /datasets` - list current user/session datasets
- `GET /datasets/{dataset_id}/status` - processing status
- `DELETE /datasets/{dataset_id}` - delete dataset + cleanup storage

### Reports
- `GET /reports/{dataset_id}` - raw report/status payload
- `GET /reports/{dataset_id}/view` - structured report view payload

### Health
- `GET /health`

## Deployment

### Frontend (Vercel)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

Set env vars in Vercel:

- `VITE_API_URL=https://<your-render-backend>.onrender.com`
- `VITE_SUPABASE_URL=<your-supabase-url>`
- `VITE_SUPABASE_ANON_KEY=<your-supabase-anon-key>`

### Backend (Render)

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Uses `backend/Procfile` and `backend/runtime.txt`

Set env vars in Render:

- `DATABASE_URL=postgresql+psycopg2://...` (Neon)
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_JWT_SECRET`
- `CORS_ALLOW_ORIGINS=https://<your-vercel-domain>`

## Notes

- Local development may use SQLite by default.
- Production should use managed Postgres (Neon recommended).

