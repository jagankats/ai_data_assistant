# Free Cloud Deployment Guide

This guide shows how to deploy the AI Data Assistant to completely free cloud services.

## 🏆 Recommended Stack: Railway + Supabase + Hugging Face

### Cost Breakdown
- **Railway**: 512MB RAM, 1GB disk FREE forever
- **Supabase**: 500MB PostgreSQL FREE forever
- **Hugging Face**: 30,000 requests/month FREE
- **Vercel**: 100GB bandwidth FREE forever
- **Total Cost**: $0/month ✅

### Step-by-Step Deployment

#### 1️⃣ Database Setup - Supabase (FREE PostgreSQL)

1. Go to [supabase.com](https://supabase.com) and sign up
2. Click "New project"
3. Choose organization and project name
4. Wait for database creation (~2 minutes)
5. Go to Settings → Database → Connection string
6. Copy the "URI" - it looks like: `postgresql://postgres:[password]@[host]:5432/postgres`
7. Save this as `DATABASE_URL` in your environment variables

#### 2️⃣ LLM Setup - Hugging Face (FREE Inference API)

1. Go to [huggingface.co](https://huggingface.co) and sign up
2. Go to Settings → Access Tokens
3. Click "Create new token"
4. Name it "AI Data Assistant" and create
5. Copy the token - save as `HUGGINGFACE_API_KEY`

#### 3️⃣ Backend Deployment - Railway (FREE)

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "Create new project" → "Deploy from GitHub repo"
3. Connect your `ai_data_assistant` repository
4. Railway will auto-detect it's a Python app
5. Go to Variables tab and add:
   - `DATABASE_URL`: Your Supabase connection string
   - `HUGGINGFACE_API_KEY`: Your Hugging Face token
   - `HUGGINGFACE_MODEL`: `microsoft/DialoGPT-medium`
6. Click "Deploy" - Railway will build and deploy automatically
7. Get the backend URL from Railway dashboard

#### 4️⃣ Frontend Deployment - Vercel (FREE)

1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Click "Import Project" → Import from GitHub
3. Select your repository and click "Import"
4. Configure build settings:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add environment variable:
   - `REACT_APP_API_URL`: Your Railway backend URL
6. Click "Deploy"

#### 5️⃣ Database Initialization

1. Go to your Railway backend logs
2. Run the database setup command:
   ```bash
   python database_setup.py
   ```
3. Or use Railway's "Variables" to temporarily set `RUN_SETUP=true` and redeploy

## 🔧 Alternative Options

### Option 2: Render + Railway PostgreSQL

**Railway PostgreSQL** (FREE):
```bash
railway login
railway init
railway add postgresql
# Get DATABASE_URL from dashboard
```

**Render Deployment**:
- Connect GitHub repo to [render.com](https://render.com)
- Create "Web Service" from your repo
- Set build command: `pip install -r requirements.txt`
- Set start command: `python backend/api.py`
- Add environment variables

### Option 3: Fly.io (Docker-based)

**Fly.io** offers 3 free VMs with 256MB RAM each:
```bash
fly launch  # In your project directory
fly deploy
```

## 🔑 Environment Variables Summary

```bash
# Required for all deployments
DATABASE_URL=postgresql://user:pass@host:port/db
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxx
HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

# For Vercel frontend
REACT_APP_API_URL=https://your-railway-app.up.railway.app
```

## 🚨 Important Notes

1. **Database Schema**: Run `database_setup.py` once after deployment
2. **CORS**: Update allowed origins in `backend/api.py` for production URLs
3. **Rate Limits**: Hugging Face free tier has monthly limits
4. **Scaling**: Free tiers have resource limits but sufficient for personal use

## 🎯 Testing Your Deployment

1. Frontend: `https://your-app.vercel.app`
2. Backend health: `https://your-app.up.railway.app/`
3. API endpoint: `https://your-app.up.railway.app/api/query`

## 💡 Cost Optimization Tips

- Use Railway's free tier limits (512MB RAM)
- Monitor Hugging Face usage in their dashboard
- Supabase free tier includes 500MB database
- Vercel free tier includes 100GB bandwidth

## 🆘 Troubleshooting

**Database Connection Issues**:
- Verify Supabase connection string format
- Check Railway environment variables

**LLM API Errors**:
- Verify Hugging Face token
- Check rate limits on Hugging Face dashboard

**Build Failures**:
- Check Railway/Render build logs
- Ensure all dependencies are in `requirements.txt`