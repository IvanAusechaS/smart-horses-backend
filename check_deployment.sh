#!/bin/bash

# Quick deployment checklist and verification script

echo "🐴 Smart Horses Backend - Deployment Checklist"
echo "================================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Check required files
echo ""
echo "✓ Checking required files..."
FILES=("requirements.txt" "run.py" "wsgi.py" "Procfile" "runtime.txt" ".env.example" "render.yaml")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing!"
    fi
done

# Check .env file
echo ""
if [ -f ".env" ]; then
    echo "✓ .env file exists"
    echo "  Current CORS_ORIGINS:"
    grep CORS_ORIGINS .env || echo "  Not set"
else
    echo "⚠ .env file not found. Copy from .env.example"
fi

# Check virtual environment
echo ""
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "⚠ Virtual environment not found. Run: python3 -m venv venv"
fi

# Check git status
echo ""
echo "✓ Git status:"
git status --short

echo ""
echo "================================================"
echo "📋 Pre-deployment Checklist:"
echo "================================================"
echo ""
echo "□ Install dependencies: pip install -r requirements.txt"
echo "□ Test locally: python run.py"
echo "□ Update CORS_ORIGINS in .env for production"
echo "□ Commit all changes: git add . && git commit -m 'message'"
echo "□ Push to GitHub: git push origin main"
echo ""
echo "🚀 For Render Deployment:"
echo "  1. Go to https://render.com"
echo "  2. Create new Web Service"
echo "  3. Connect this GitHub repo"
echo "  4. Set environment variables (see README.md)"
echo "  5. Deploy!"
echo ""
echo "================================================"
