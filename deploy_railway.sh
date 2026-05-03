#!/bin/bash

# AI Data Assistant - Railway Deployment Script
# This script helps deploy the application to Railway

echo "🚀 AI Data Assistant - Railway Deployment"
echo "========================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔑 Logging into Railway..."
railway login

# Initialize project
echo "📁 Initializing Railway project..."
railway init

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
railway add postgresql

# Set environment variables
echo "🔧 Setting environment variables..."
echo "Please provide your Hugging Face API key:"
read -s HF_KEY
railway variables set HUGGINGFACE_API_KEY=$HF_KEY
railway variables set HUGGINGFACE_MODEL=microsoft/DialoGPT-medium

# Deploy
echo "🚀 Deploying to Railway..."
railway up

# Get URL
echo "📍 Getting deployment URL..."
railway domain

echo "✅ Deployment complete!"
echo "Don't forget to:"
echo "1. Run database setup: railway run python database_setup.py"
echo "2. Deploy frontend to Vercel"
echo "3. Update CORS origins in backend/api.py"