#!/bin/bash
echo "🚀 Deploying DreamDirector to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
    echo "✅ Railway CLI installed!"
fi

# Check if logged in to Railway
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway. Please run:"
    echo "   railway login"
    exit 1
fi

echo "✅ Railway authentication verified!"

# Check if this is a Railway project
if [ ! -f "railway.toml" ]; then
    echo "❌ railway.toml not found!"
    exit 1
fi

echo "📦 Preparing for deployment..."
echo "   - Frontend will be built automatically in Docker"
echo "   - Backend will start with FastAPI + Uvicorn"
echo "   - Static files will be served at the root"

# Deploy to Railway
echo "🚂 Deploying to Railway..."
railway up

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your app should be available at your Railway domain"
    echo "📊 Check status: railway status"
    echo "📜 View logs: railway logs"
else
    echo "❌ Deployment failed. Check the logs above."
    exit 1
fi 