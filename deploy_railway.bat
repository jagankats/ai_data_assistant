@echo off
REM AI Data Assistant - Railway Deployment Script (Windows)
REM This script helps deploy the application to Railway

echo 🚀 AI Data Assistant - Railway Deployment
echo =========================================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Installing...
    npm install -g @railway/cli
)

REM Login to Railway
echo 🔑 Logging into Railway...
railway login

REM Initialize project
echo 📁 Initializing Railway project...
railway init

REM Add PostgreSQL database
echo 🗄️ Adding PostgreSQL database...
railway add postgresql

REM Set environment variables
echo 🔧 Setting environment variables...
echo Please provide your Hugging Face API key:
set /p HF_KEY=
railway variables set HUGGINGFACE_API_KEY=%HF_KEY%
railway variables set HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

REM Deploy
echo 🚀 Deploying to Railway...
railway up

REM Get URL
echo 📍 Getting deployment URL...
railway domain

echo ✅ Deployment complete!
echo Don't forget to:
echo 1. Run database setup: railway run python database_setup.py
echo 2. Deploy frontend to Vercel
echo 3. Update CORS origins in backend/api.py

pause