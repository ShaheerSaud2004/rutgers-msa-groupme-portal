# 🚀 Deploy to Vercel NOW!

Your GroupMe Portal is ready for deployment! Here's the quickest way to get it live:

## 📤 Step 1: Push to GitHub

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `groupme-portal`
3. **Make it PUBLIC** (required for free Vercel)
4. **Don't initialize** with README, .gitignore, or license
5. **Click "Create repository"**

6. **Copy the repository URL** (it will look like: `https://github.com/YOUR_USERNAME/groupme-portal.git`)

7. **Run these commands** in your terminal:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/groupme-portal.git
   git push -u origin main
   ```

## 🌐 Step 2: Deploy to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with your GitHub account
3. **Click "New Project"**
4. **Select** your `groupme-portal` repository
5. **Click "Import"**

## ⚙️ Step 3: Configure Environment Variables

In the Vercel deployment settings, add these environment variables:

- **`GROUPME_ACCESS_TOKEN`** = `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP`
- **`SECRET_KEY`** = `your-secret-key-here` (generate a random string)

## 🗄️ Step 4: Set Up Database (Optional but Recommended)

For persistent data storage, add a PostgreSQL database:

### Option A: Vercel Postgres (Easiest)
1. In your Vercel project dashboard
2. Go to "Storage" tab
3. Click "Create Database" → "Postgres"
4. Name it: `groupme-portal-db`
5. Vercel will automatically add the `DATABASE_URL` environment variable

### Option B: External Database
Use any of these free PostgreSQL services:
- **Supabase**: https://supabase.com (free tier)
- **Railway**: https://railway.app (free tier)
- **Neon**: https://neon.tech (free tier)

Copy the connection string and add it as `DATABASE_URL` environment variable.

## 🚀 Step 5: Deploy!

1. **Click "Deploy"**
2. **Wait 2-3 minutes** for deployment
3. **Get your live URL** (e.g., `https://groupme-portal-abc123.vercel.app`)

## ✅ Step 6: Test Your Deployment

1. **Visit your Vercel URL**
2. **Add your group chat**:
   - Group Name: `RUmmah Brothers '25-26`
   - Group ID: `107939343`
   - Bot ID: `a890eb8fe19b87fab1fc97fe2a`
3. **Create a test post** with an image
4. **Send immediately** to test
5. **Check your GroupMe chat** for the message!

## 🎉 Success!

Your GroupMe Portal is now:
- ✅ **Live on the internet** via your Vercel URL
- ✅ **Automatically updated** when you push to GitHub
- ✅ **Free hosting** with Vercel
- ✅ **HTTPS enabled** by default
- ✅ **Global CDN** for fast loading

## 🔄 For Your Second Group

1. Create another bot at https://dev.groupme.com/bots
2. Add the second group to your portal
3. Start scheduling posts for both groups!

## 📱 Your Portal Features

- **Upload posters/images** and send to GroupMe
- **Schedule messages** for specific times
- **Send immediately** or schedule for later
- **Include multiple links** in messages
- **Manage multiple group chats**
- **Beautiful web interface**

**Your GroupMe Portal is production-ready! 🚀**
