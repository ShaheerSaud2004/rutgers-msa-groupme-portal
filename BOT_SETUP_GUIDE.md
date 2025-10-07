# Bot Setup Guide - Separate Bots Needed

## 🚨 **Current Issue**

Both groups are using the **same bot ID**: `0253eda15ad81f240b1c2ce892`

This means:
- ❌ Messages might go to the wrong group
- ❌ Both groups share the same bot
- ❌ No proper separation between Brothers and Sisters

## ✅ **What We Need**

### **Separate Bot IDs for Each Group:**

1. **Brothers Group** needs its own bot:
   - Group ID: `107939343`
   - Bot ID: `[BROTHERS_BOT_ID]` (different from current)
   - Access Token: `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP`

2. **Sisters Group** needs its own bot:
   - Group ID: `107937618` 
   - Bot ID: `[SISTERS_BOT_ID]` (different from current)
   - Access Token: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA`

## 🔧 **How to Fix This**

### **Step 1: Create Separate Bots**

1. **For Brothers Group:**
   - Go to [GroupMe Developer Console](https://dev.groupme.com/bots)
   - Create a new bot for the Brothers group
   - Get the new Bot ID

2. **For Sisters Group:**
   - Create another new bot for the Sisters group  
   - Get the new Bot ID

### **Step 2: Update the Database**

Once you have the separate bot IDs, we'll update the database with:
- Brothers: Group ID `107939343` + New Bot ID + Original Token
- Sisters: Group ID `107937618` + New Bot ID + Amira's Token

## 🎯 **Why This Matters**

- **Proper Separation**: Each group has its own bot
- **No Cross-Contamination**: Messages go to the right group
- **Better Security**: Each group uses its own access token
- **Easier Management**: Clear separation between Brothers and Sisters

## 📱 **Next Steps**

1. **Create separate bots** for each group
2. **Get the new bot IDs**
3. **Update the database** with the correct bot IDs
4. **Test messaging** to ensure proper separation

**This will ensure that Brothers and Sisters groups are completely separate!** 🎊
