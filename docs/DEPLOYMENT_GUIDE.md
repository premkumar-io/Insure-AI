# 🚀 InsureAI™ Deployment & Operations Guide

Comprehensive guide for deploying and managing the **InsureAI™** platform across local development environments, Vercel Serverless Functions, and Docker containers.

---

## 1. Local Development Execution

### Option A: Single Command Runner (Recommended)
Run both backend and frontend servers together using the launcher:

```bash
python run.py
```

*(or `./myvenv/bin/python run.py` if virtualenv is not activated)*

#### Features of `run.py`:
- Checks and automatically clears port conflicts on `8000` and `8501`.
- Concurrently launches Uvicorn (`app:app` on port 8000) and Streamlit (`frontend.py` on port 8501).
- Single `Ctrl + C` gracefully terminates both services.

---

## 2. Deploying to Vercel (Serverless)

Vercel hosts the FastAPI backend serverless function using `@vercel/python`.

### Setup Files Included
- `api/index.py`: Serverless handler entrypoint exporting FastAPI `app`.
- `vercel.json`: Route rewrites directing `/(.*)` to `api/index.py`.

### Deployment Steps (Vercel CLI)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Staging**:
   ```bash
   vercel
   ```

3. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## 3. Docker Container Deployment

### Build Docker Image
```bash
docker build -t insure-ai:latest .
```

### Run Docker Container
```bash
docker run -d -p 8000:8000 --name insure-ai-backend insure-ai:latest
```

Verify backend:
```bash
curl http://localhost:8000/health
```

---

## 4. Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `API_URL` | `http://localhost:8000/predict` | Target FastAPI backend URL for Streamlit UI |
| `PORT` | `8000` | Port for FastAPI server |

To point Streamlit UI to a production backend (e.g. Vercel):
```bash
export API_URL="https://your-app.vercel.app/predict"
python run.py
```
