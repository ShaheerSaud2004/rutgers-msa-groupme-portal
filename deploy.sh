#!/bin/bash

# GroupMe Portal Deployment Script
echo "🚀 GroupMe Portal Deployment Script"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - GroupMe Portal ready for Vercel"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "🔗 Please add your GitHub repository as origin:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/groupme-portal.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
else
    echo "✅ Remote origin already configured"
    echo "📤 Pushing latest changes..."
    git add .
    git commit -m "Update for Vercel deployment" || echo "No changes to commit"
    git push origin main
    echo "✅ Code pushed to GitHub"
fi

echo ""
echo "🌐 Next Steps:"
echo "1. Go to https://vercel.com"
echo "2. Sign in with GitHub"
echo "3. Click 'New Project'"
echo "4. Select your 'groupme-portal' repository"
echo "5. Add environment variables:"
echo "   - GROUPME_ACCESS_TOKEN = HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP"
echo "   - SECRET_KEY = your-secret-key-here"
echo "6. Click 'Deploy'"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo "🎉 Your GroupMe Portal will be live at: https://your-app.vercel.app"
