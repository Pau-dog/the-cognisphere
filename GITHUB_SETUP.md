# GitHub Repository Setup Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `the-cognisphere`
3. Description: `Emergent Intelligence Civilization Engine - A living ecosystem of cognitive agents`
4. Make it **Public** (required for GitHub Pages)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Push Your Code

```bash
cd /Users/zaydbashir/the-cognisphere
git push -u origin main
```

## Step 3: Set Up Render.com Backend

1. Go to https://dashboard.render.com/
2. Click "New" → "Web Service"
3. Connect your GitHub repository: `zaydabash/the-cognisphere`
4. Configure the service:
   - **Name**: `cognisphere-backend`
   - **Root Directory**: `backend`
   - **Environment**: Docker
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Plan**: Free
   - **Region**: Oregon (US West)
   - **Auto-Deploy**: Yes

5. Environment Variables:
```
ENV=production
PORT=8000
LLM_MODE=mock
MEM_BACKEND=networkx
VEC_BACKEND=faiss
SIMULATION_SEED=42
SIMULATION_AGENTS=100
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

6. After deployment, note your service URL (e.g., `https://cognisphere-backend.onrender.com`)

## Step 4: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

### Required Secrets:
- **RENDER_API_KEY**: Your Render.com personal API key
- **RENDER_SERVICE_ID**: Your Render service ID (found in service settings)
- **RENDER_HEALTH_URL**: Your Render service URL + `/healthz`

### How to Get RENDER_API_KEY:
1. Go to Render Dashboard → Account Settings → API Keys
2. Create new API key
3. Copy the key

### How to Get RENDER_SERVICE_ID:
1. Go to your service settings in Render
2. Copy the Service ID (looks like `srv-xxxxx`)

### How to Get RENDER_HEALTH_URL:
1. Your service URL + `/healthz`
2. Example: `https://cognisphere-backend.onrender.com/healthz`

## Step 5: Enable GitHub Pages

1. Go to your GitHub repository → Settings → Pages
2. Source: GitHub Actions
3. The deployment will happen automatically when you push to main

## Step 6: Test the Deployment

After pushing your code:
1. Check GitHub Actions tab for CI/CD status
2. Visit your GitHub Pages URL: `https://zaydabash.github.io/the-cognisphere`
3. Test the backend: `https://your-render-url.onrender.com/healthz`

## Expected Results

- **Frontend**: `https://zaydabash.github.io/the-cognisphere`
- **Backend**: `https://cognisphere-backend.onrender.com`
- **API Docs**: `https://cognisphere-backend.onrender.com/docs`

## Troubleshooting

If deployment fails:
1. Check GitHub Actions logs
2. Verify all secrets are set correctly
3. Ensure Render service is healthy
4. Check CORS settings in backend
