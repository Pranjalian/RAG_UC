# Deployment Guide: Vercel (Frontend) & Railway (Backend)

This document provides step-by-step instructions for deploying the RAG Mutual Fund Assistant. 
We use **Railway** for the FastAPI backend and persistent Vector Store, and **Vercel** for the Next.js frontend.

---

## 1. Backend Deployment (Railway)

### Prerequisites
1. Push your repository to GitHub.
2. Sign up / Log in to [Railway.app](https://railway.app/).

### Steps
1. Click **"New Project"** -> **"Deploy from GitHub repo"**.
2. Select your repository.
3. Railway will detect the `railway.json` file and automatically configure Nixpacks to use Uvicorn for Python 3.11.
4. **Environment Variables**: Go to the **Variables** tab and add:
   - `GOOGLE_API_KEY`: Your Gemini API Key
   - `GROQ_API_KEY`: Your Groq API Key
   - `ADMIN_TOKEN`: Generate a random secure string (e.g., `openssl rand -hex 32`). This protects your ingestion endpoint.
   - `FRONTEND_URL`: Leave blank for now (or set to `*`).
5. **Persistent Volume**:
   - Go to the **Settings** tab of your service.
   - Under **Volumes**, create a new Persistent Volume.
   - Mount the volume to the absolute path `/app/data` (which is where `data/rawdata` etc will live) or `/app/vector_db` if configured absolutely. 
   - *Note: Since the codebase accesses `./vector_db/chroma` locally, you should map the volume to `/app/vector_db` and `/app/data` inside the container.*
6. **Trigger Initial Ingestion**:
   - Once deployed, grab the generated Railway Public Domain (e.g., `https://my-rag.up.railway.app`).
   - Run this command from your terminal to populate the database:
     ```bash
     curl -X POST https://my-rag.up.railway.app/api/ingest -H "Authorization: Bearer <YOUR_ADMIN_TOKEN>"
     ```
   - Go to the **Logs** tab in Railway to watch the ingestion pipeline run!

---

## 2. Frontend Deployment (Vercel)

### Steps
1. Sign up / Log in to [Vercel.com](https://vercel.com/).
2. Click **"Add New..."** -> **"Project"** and import your GitHub repository.
3. Vercel will auto-detect Next.js. Make sure the **Root Directory** is set to `frontend/`.
4. **Environment Variables**:
   - Add `NEXT_PUBLIC_API_URL` and set its value to your Railway Domain (e.g., `https://my-rag.up.railway.app`).
5. Click **Deploy**.

---

## 3. Post-Deployment (Security & Automation)

### CORS Lockdown
Once you have your Vercel URL (e.g., `https://rag-frontend.vercel.app`), go back to Railway:
1. Update the `FRONTEND_URL` variable to `https://rag-frontend.vercel.app`.
2. Railway will automatically redeploy. The API will now block requests from any other origin.

### GitHub Actions Automation
Your `.github/workflows/schedule.yml` is already configured to run every 12 hours. It needs secrets to talk to your Railway app:
1. Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Add **New repository secret**:
   - `ADMIN_TOKEN`: The same random string you used in Railway.
   - `RAILWAY_APP_URL`: The domain of your Railway app (no trailing slash).

Now, GitHub Actions will hit the API endpoint every 12 hours, and Railway will scrape and embed the data, saving it directly to its Persistent Volume!
