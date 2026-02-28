# Sentinel

Sentinel is an ML data quality and model-readiness platform for tabular datasets.  
Upload a CSV, run deterministic diagnostics, and get a production-style report with actionable fixes and visual diagnostics.

## Screenshots
<img width="1920" height="1536" alt="257shots_so" src="https://github.com/user-attachments/assets/288288dc-335f-4ec5-877b-617248ee6bb9" />
<img width="1920" height="1536" alt="57shots_so" src="https://github.com/user-attachments/assets/8a983a86-dade-4587-81b8-5a952fbcda1e" />
<img width="1920" height="1536" alt="158shots_so" src="https://github.com/user-attachments/assets/02ed4f8f-710e-4ddb-ae20-e1c4360d2215" />

## Highlights

- Upload CSV datasets and run analysis asynchronously.
- Optional target-aware analysis (target column can be provided at upload time).
- V2 diagnostics stack:
  - missingness + structural risks
  - leakage heuristics
  - categorical / outlier checks
  - target signal diagnostics
  - lightweight model simulation
  - recommendation engine
- V2 calibrated scoring (`sentinel_score`) with difficulty + modeling risk labels.
- Visual diagnostics are generated once during analysis and persisted in DB.
- Report page only opens after processing is complete.
- Works for guest sessions and authenticated users (Supabase).

## Tech Stack

### Frontend
- React + TypeScript + Vite
- Tailwind CSS
- shadcn-style component structure (`frontend/components/ui`)
- Supabase JS client

### Backend
- FastAPI
- SQLAlchemy
- Pandas + SciPy + scikit-learn + Matplotlib
- PostgreSQL (production) / SQLite (local fallback)
- Background processing via FastAPI `BackgroundTasks`

### Infra
- Frontend: Vercel
- Backend: Render
- Database: Neon Postgres
- Auth: Supabase

## Repository Layout

```text
.
├── frontend/          # Vite React app
├── backend/           # FastAPI API + analysis engine
├── render.yaml        # Render blueprint config
├── runtime.txt        # Runtime pin fallback
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

Backend URL: `http://localhost:8000`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## Environment Variables

### Backend (`backend/.env`)

Required:

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_JWT_SECRET`

Optional:

- `APP_NAME` (default: `SentinelAI`)
- `CORS_ALLOW_ORIGINS` (comma-separated)
- `CORS_ALLOW_ORIGIN_REGEX`

### Frontend (`frontend/.env`)

- `VITE_API_URL`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## API Overview

### Datasets
- `POST /datasets/upload`  
  multipart: `file`, `dataset_name`, optional `target_column`
- `GET /datasets`
- `GET /datasets/{dataset_id}/status`
- `DELETE /datasets/{dataset_id}`

### Reports
- `GET /reports/{dataset_id}` (raw payload/status)
- `GET /reports/{dataset_id}/view` (frontend view payload)

### Plots
- `GET /plots/{dataset_id}/{plot_type}` returns `image/png`
- Plot types:
  - `missing_heatmap`
  - `target_distribution`
  - `feature_importance`
  - `numeric_distribution`
  - `correlation_heatmap`

### Health
- `GET /health`

## Plot Storage Model

- Plots are generated in worker after analysis.
- Stored in `analysis_plots` table (`dataset_id + plot_type` unique).
- Served directly from DB bytes (no on-demand regeneration on normal path).
- Delete dataset also removes persisted plots.

## Deployment

### Frontend (Vercel)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

Set:
- `VITE_API_URL=https://<your-render-backend>.onrender.com`
- `VITE_SUPABASE_URL=https://<your-project-ref>.supabase.co`
- `VITE_SUPABASE_ANON_KEY=<anon-key>`

### Backend (Render)

Use `render.yaml` (recommended) or set manually:
- Root directory: `backend`
- Build command: `python -m pip install --upgrade pip && pip install --only-binary=:all: -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Set:
- `DATABASE_URL=postgresql+psycopg2://...`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_JWT_SECRET`
- `CORS_ALLOW_ORIGINS=https://<your-vercel-domain>`

## Troubleshooting

- `ERR_CERT_COMMON_NAME_INVALID` (Supabase): verify exact `VITE_SUPABASE_URL`.
- CORS blocked from Vercel: verify backend env + redeploy latest CORS fixes.
- Render SciPy build failures: use latest requirements + wheel-only install command.


