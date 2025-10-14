# GitHub Secrets Setup Guide

This guide explains how to set up the required secrets for The Cognisphere's CI/CD pipeline.

## Where to Set Secrets

1. Go to your GitHub repository
2. Click **Settings**  **Secrets and variables**  **Actions**
3. Click **New repository secret**

## Required Secrets

### Render.com Backend Deployment

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `RENDER_API_KEY` | Render personal API key | 1. Go to [Render Dashboard](https://dashboard.render.com/) 2. Click **Account Settings**  **API Keys** 3. Create new API key |
| `RENDER_SERVICE_ID` | Render service ID for backend | 1. Create Web Service in Render 2. Copy Service ID from service settings |
| `RENDER_HEALTH_URL` | Health check URL | Your Render service URL + `/healthz` (e.g., `https://cognisphere-backend.onrender.com/healthz`) |

### Optional Secrets

| Secret Name | Description | Default |
|-------------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for real LLM mode | Uses mock mode if not set |
| `NEO4J_URI` | Neo4j database URI | Uses NetworkX fallback |
| `NEO4J_AUTH` | Neo4j authentication | Uses NetworkX fallback |
| `REDIS_URL` | Redis cache URL | Not used in free tier |

## Render.com Setup

### 1. Create Backend Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New**  **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `cognisphere-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Plan**: Free

### 2. Environment Variables

Set these in Render service settings:

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

### 3. Get Service ID

1. Go to your service settings
2. Copy the **Service ID** (looks like `srv-xxxxx`)
3. Add to GitHub secrets as `RENDER_SERVICE_ID`

## Health Check Setup

### 1. Get Health URL

Your health check URL will be:
```
https://your-service-name.onrender.com/healthz
```

### 2. Test Health Endpoint

```bash
curl https://your-service-name.onrender.com/healthz
# Should return: {"ok": true}
```

### 3. Add to GitHub Secrets

Add the full health URL as `RENDER_HEALTH_URL`

## Verification

After setting up secrets:

1. **Push to main branch** - Should trigger backend deployment
2. **Check GitHub Actions** - Should show deployment success
3. **Verify health endpoint** - Should return `{"ok": true}`
4. **Test API** - Visit your Render URL + `/docs`

## Troubleshooting

### Backend Deployment Fails

- Check Render service logs
- Verify `RENDER_SERVICE_ID` is correct
- Ensure `RENDER_API_KEY` has proper permissions

### Health Check Fails

- Wait 5-10 minutes after deployment
- Check if service is actually running
- Verify health endpoint URL is correct

### Frontend Can't Connect

- Check CORS settings in backend
- Verify backend URL in frontend environment
- Check network tab in browser dev tools

## Automatic Updates

Once set up, the system will:

-  Auto-deploy backend on every push to `main`
-  Auto-deploy frontend to GitHub Pages
-  Run health checks after deployment
-  Build and push Docker images on releases

## Support

If you encounter issues:

1. Check GitHub Actions logs
2. Check Render service logs  
3. Verify all secrets are set correctly
4. Ensure service URLs are accessible

---

**That's it! Your Cognisphere will now auto-deploy with every push!**
