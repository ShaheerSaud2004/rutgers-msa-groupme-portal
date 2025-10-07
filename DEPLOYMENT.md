# 🚀 Deployment Guide - GroupMe Portal

Deploy your GroupMe Portal to the cloud so others can access it! Here are the easiest hosting options:

## 🌟 **Option 1: Railway (Recommended - Easiest)**

Railway is the simplest way to deploy your portal:

### Steps:
1. **Go to**: https://railway.app/
2. **Sign up** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your GroupMe repository**
6. **Add Environment Variables**:
   - `GROUPME_ACCESS_TOKEN`: Your GroupMe API token
   - `SECRET_KEY`: Any random string (e.g., `my-secret-key-123`)
7. **Click "Deploy"**

**✅ Done!** Your portal will be live at a URL like: `https://your-project.railway.app`

---

## 🌟 **Option 2: Vercel (Great for Static + API)**

Vercel is perfect for web apps:

### Steps:
1. **Go to**: https://vercel.com/
2. **Sign up** with GitHub
3. **Click "New Project"**
4. **Import your GroupMe repository**
5. **Add Environment Variables**:
   - `GROUPME_ACCESS_TOKEN`: Your GroupMe API token
   - `SECRET_KEY`: Any random string
6. **Click "Deploy"**

**✅ Done!** Your portal will be live at a URL like: `https://your-project.vercel.app`

---

## 🌟 **Option 3: Render (Free Tier Available)**

Render offers a free tier:

### Steps:
1. **Go to**: https://render.com/
2. **Sign up** with GitHub
3. **Click "New +" → "Web Service"**
4. **Connect your repository**
5. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. **Add Environment Variables**:
   - `GROUPME_ACCESS_TOKEN`: Your GroupMe API token
   - `SECRET_KEY`: Any random string
7. **Click "Create Web Service"**

**✅ Done!** Your portal will be live at a URL like: `https://your-project.onrender.com`

---

## 🔧 **Environment Variables Needed**

All hosting platforms need these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `GROUPME_ACCESS_TOKEN` | Your GroupMe API token | `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP` |
| `SECRET_KEY` | Random string for security | `my-super-secret-key-123` |

---

## 📱 **After Deployment**

1. **Share the URL** with your team
2. **Add your GroupMe groups** using the web interface
3. **Start creating posts** with images and scheduling
4. **Everyone can access** the portal from anywhere!

---

## 🆓 **Free Tier Limits**

- **Railway**: 500 hours/month free
- **Vercel**: 100GB bandwidth/month free
- **Render**: 750 hours/month free

All are perfect for personal/small team use!

---

## 🔒 **Security Notes**

- Never share your `GROUPME_ACCESS_TOKEN` publicly
- Use environment variables for all sensitive data
- The portal is designed to be secure for team use

---

## 🆘 **Need Help?**

If you run into issues:
1. Check the deployment logs
2. Verify environment variables are set
3. Make sure your GroupMe API token is valid
4. Check that your bot IDs are correct

**Your GroupMe Portal will be live and accessible to everyone!** 🎉
