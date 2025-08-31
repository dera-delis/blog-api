#!/bin/bash

echo "🚀 Deploying Blog API to Render.com"
echo "====================================="

echo "1. ✅ Checking if all required files exist..."
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

if [ ! -f "app/main.py" ]; then
    echo "❌ app/main.py not found!"
    exit 1
fi

echo "✅ All required files found!"

echo ""
echo "2. 📝 Next steps:"
echo "   a) Push your code to GitHub:"
echo "      git add ."
echo "      git commit -m 'Add deployment configuration'"
echo "      git push origin main"
echo ""
echo "   b) Go to https://render.com and sign up/login"
echo "   c) Click 'New +' → 'Blueprint'"
echo "   d) Connect your GitHub repository"
echo "   e) Render will auto-detect render.yaml"
echo "   f) Click 'Apply' and wait for deployment"
echo ""
echo "3. 🌐 Once deployed, your API will be available at:"
echo "   - API: https://your-app-name.onrender.com"
echo "   - Docs: https://your-app-name.onrender.com/docs"
echo "   - Health: https://your-app-name.onrender.com/health"
echo ""
echo "🎉 Perfect for showing recruiters your live API!"
