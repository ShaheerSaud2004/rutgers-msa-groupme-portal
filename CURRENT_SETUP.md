# Rutgers MSA GroupMe Portal - Current Setup

## 🎯 **Dual Access Token System**

The portal now automatically uses the correct access token for each group:

### **Brothers Group**
- **Name**: RUmmah Brothers '25-26
- **Group ID**: `107939343`
- **Bot ID**: `0253eda15ad81f240b1c2ce892`
- **Access Token**: `HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP` (Original user)

### **Sisters Group**
- **Name**: RUmmah Sisters '25-26 💫
- **Group ID**: `107937618`
- **Bot ID**: `0253eda15ad81f240b1c2ce892`
- **Access Token**: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA` (Amira's token)

## 🔧 **How It Works**

The `GroupMeAPI` class automatically selects the correct token based on the group ID:

```python
if group_id == '107939343':  # Brothers group
    self.access_token = 'HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP'
elif group_id == '107937618':  # Sisters group
    self.access_token = 'BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA'
```

## 🚀 **Current Features**

✅ **Dual Token Support** - Automatic token selection per group
✅ **Message History** - Track all sent messages
✅ **Daily Messages** - Set up recurring daily posts
✅ **Scheduled Posts** - Schedule messages for specific times
✅ **Image Upload** - Send posters and images
✅ **Link Support** - Include links in messages
✅ **Both Groups Ready** - Brothers and Sisters chats

## 🌐 **Access URLs**

- **Local**: http://localhost:5001
- **Railway**: [Auto-deployed from GitHub]
- **GitHub**: https://github.com/ShaheerSaud2004/rutgers-msa-groupme-portal

## 📱 **Ready to Use**

Both groups are now properly configured with their respective access tokens. When you create a post and select a group, the system will automatically use the correct token for that group.

**Test it out by creating a post and selecting either the Brothers or Sisters group!** 🎊
