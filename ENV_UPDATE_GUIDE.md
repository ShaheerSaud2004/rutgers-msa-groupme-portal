# Environment Variables Update Guide

## 🔧 **What You Need to Update**

### **For Local Development (.env file)**

Create a `.env` file in your project root with:

```bash
# Flask Configuration
SECRET_KEY=rutgers-msa-secret-key-2024
DATABASE_URL=sqlite:///groupme_portal.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# GroupMe API Configuration
# This is the fallback token (Amira's token)
GROUPME_ACCESS_TOKEN=BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA
GROUPME_BASE_URL=https://api.groupme.com/v3

# Deployment
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001
```

### **For Railway Deployment**

In your Railway dashboard, set these environment variables:

```
GROUPME_ACCESS_TOKEN=BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA
SECRET_KEY=rutgers-msa-secret-key-2024
```

## 🎯 **Important Notes**

### **Dual Token System**
The system now automatically uses the correct token for each group:

- **Brothers Group** (ID: 107939343) → Uses: `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP`
- **Sisters Group** (ID: 107937618) → Uses: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA`

### **No Manual Token Switching Needed**
- The system automatically detects which group you're sending to
- It selects the appropriate token based on the group ID
- You don't need to manually switch tokens

## 🚀 **Current Status**

✅ **Local Development**: Ready with dual token system
✅ **Railway Deployment**: Auto-deployed with latest changes
✅ **Both Groups**: Properly configured with their respective tokens

## 📱 **How to Test**

1. **Local**: http://localhost:5001
2. **Create a post** and select either Brothers or Sisters group
3. **Send the message** - the system will use the correct token automatically!

**The environment is now properly configured for both groups!** 🎊
