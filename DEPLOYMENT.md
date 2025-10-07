# 🚀 Deploy GroupMe Portal to Vercel

This guide will help you deploy your GroupMe Portal to Vercel for free hosting.

## 📋 Prerequisites

1. **GitHub Account** - You'll need to push your code to GitHub
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **GroupMe API Token** - You already have this: `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP`

## 🔧 Step 1: Prepare Your Code

Your code is already prepared for Vercel deployment! The following files have been created:

- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ `.vercelignore` - Files to exclude from deployment

## 📤 Step 2: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - GroupMe Portal"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `groupme-portal`
   - Make it **Public** (required for free Vercel)
   - Don't initialize with README (you already have files)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/groupme-portal.git
   git branch -M main
   git push -u origin main
   ```

## 🌐 Step 3: Deploy to Vercel

1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**:
   - Click "New Project"
   - Select your `groupme-portal` repository
   - Click "Import"

3. **Configure Environment Variables**:
   - In the "Environment Variables" section, add:
     - `GROUPME_ACCESS_TOKEN` = `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP`
     - `SECRET_KEY` = `your-secret-key-here` (generate a random string)

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete (2-3 minutes)

## 🎯 Step 4: Set Up Database

Since Vercel uses serverless functions, we need a persistent database. You have two options:

### Option A: Use Vercel Postgres (Recommended)

1. **Add Vercel Postgres**:
   - In your Vercel dashboard, go to "Storage"
   - Click "Create Database" → "Postgres"
   - Name it: `groupme-portal-db`

2. **Update Environment Variables**:
   - Add `DATABASE_URL` from the Postgres connection string

### Option B: Use External Database

You can use any PostgreSQL database service like:
- **Supabase** (free tier available)
- **Railway** (free tier available)
- **Neon** (free tier available)

## 🔄 Step 5: Update Your Bots

After deployment, you'll get a new URL like: `https://your-app.vercel.app`

1. **Update Bot Callback URLs** (if needed):
   - Go to [GroupMe Developer Console](https://dev.groupme.com/bots)
   - Edit your bots
   - Set callback URL to: `https://your-app.vercel.app/webhook`

## ✅ Step 6: Test Your Deployment

1. **Visit your deployed app**: `https://your-app.vercel.app`
2. **Add your group chat**:
   - Group Name: `RUmmah Brothers '25-26`
   - Group ID: `107939343`
   - Bot ID: `a890eb8fe19b87fab1fc97fe2a`
3. **Create a test post** and send it immediately
4. **Check your GroupMe chat** for the message

## 🚨 Important Notes

### File Uploads
- **Images are stored temporarily** in Vercel's `/tmp` directory
- **Files are deleted** after each serverless function execution
- **For persistent storage**, consider using:
  - AWS S3
  - Cloudinary
  - Vercel Blob Storage

### Scheduled Posts
- **Background scheduling** doesn't work on serverless
- **Alternative solutions**:
  - Use Vercel Cron Jobs
  - External cron service (cron-job.org)
  - GitHub Actions with scheduled workflows

### Database
- **SQLite won't work** on Vercel (read-only filesystem)
- **Use PostgreSQL** for persistent data storage

## 🔧 Troubleshooting

### Common Issues:

1. **"Module not found" errors**:
   - Check `requirements.txt` includes all dependencies
   - Redeploy the project

2. **Database connection errors**:
   - Verify `DATABASE_URL` environment variable
   - Check database is accessible from Vercel

3. **File upload issues**:
   - Files are stored in `/tmp` (temporary)
   - Consider external storage for persistence

4. **GroupMe API errors**:
   - Verify `GROUPME_ACCESS_TOKEN` is correct
   - Check bot is added to the group chat

## 🎉 Success!

Once deployed, your GroupMe Portal will be:
- ✅ **Accessible worldwide** via your Vercel URL
- ✅ **Automatically updated** when you push to GitHub
- ✅ **Free hosting** with Vercel's generous limits
- ✅ **HTTPS enabled** by default
- ✅ **Fast global CDN** for quick loading

Your portal URL will be something like: `https://groupme-portal-abc123.vercel.app`

## 📱 Next Steps

1. **Create your second bot** for your other group chat
2. **Add the second group** to your portal
3. **Start creating and scheduling posts**!
4. **Share the portal URL** with others who need to post to the groups

## 🔒 Security Reminder

- Never share your GroupMe login credentials
- Use only the API token for integration
- Keep your Vercel environment variables secure
- Regularly rotate your API tokens
