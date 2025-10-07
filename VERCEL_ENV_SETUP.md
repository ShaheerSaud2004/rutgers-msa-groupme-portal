# Vercel Environment Variables Setup

## 🔧 **Environment Variables for Vercel**

Go to your Vercel project dashboard → Settings → Environment Variables and add these:

### **Required Variables:**

```
SECRET_KEY=rutgers-msa-secret-key-2024
```

### **Group-Specific Access Tokens (Required):**

```
BROTHERS_ACCESS_TOKEN=HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP
SISTERS_ACCESS_TOKEN=BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA
```

### **Fallback Token (Optional):**

```
GROUPME_ACCESS_TOKEN=BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA
```

### **Optional Variables (if needed):**

```
DATABASE_URL=sqlite:///groupme_portal.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🎯 **Important Notes:**

### **Dual Token System**
The system automatically uses the correct token for each group:
- **Brothers Group** (ID: 107939343) → Uses: `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP`
- **Sisters Group** (ID: 107937618) → Uses: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA`

### **Bot IDs**
- **Brothers Bot ID**: `a890eb8fe19b87fab1fc97fe2a`
- **Sisters Bot ID**: `0253eda15ad81f240b1c2ce892`

## 🚀 **Steps to Deploy:**

1. **Go to Vercel Dashboard**
2. **Select your project**
3. **Go to Settings → Environment Variables**
4. **Add the variables above**
5. **Redeploy your project**

## 📱 **After Deployment:**

Your portal will be available at your Vercel URL and will:
- ✅ Use correct tokens for each group
- ✅ Send messages to the right group
- ✅ Handle both Brothers and Sisters groups properly

**The system is now ready for Vercel deployment!** 🎊
