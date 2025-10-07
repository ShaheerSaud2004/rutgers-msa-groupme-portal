# Rutgers MSA GroupMe Portal - Environment Configuration

## Current Setup

### Group Chats
1. **RUmmah Brothers '25-26**
   - Group ID: `107939343`
   - Bot ID: `0253eda15ad81f240b1c2ce892`
   - Access Token: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA` (Amira's token)

2. **RUmmah Sisters '25-26 💫**
   - Group ID: `107937618`
   - Bot ID: `0253eda15ad81f240b1c2ce892`
   - Access Token: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA` (Amira's token)

### Environment Variables

Create a `.env` file in the project root with:

```bash
# Flask Configuration
SECRET_KEY=rutgers-msa-secret-key-2024
DATABASE_URL=sqlite:///groupme_portal.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# GroupMe API Configuration
GROUPME_ACCESS_TOKEN=BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA
GROUPME_BASE_URL=https://api.groupme.com/v3

# Deployment
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001
```

### For Railway Deployment

Set these environment variables in Railway dashboard:

```
GROUPME_ACCESS_TOKEN=BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA
SECRET_KEY=rutgers-msa-secret-key-2024
```

## Current Token Usage

**Amira's Access Token**: `BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA`

This token is currently used for both groups because:
- Amira has access to both the Brothers and Sisters groups
- The bot IDs are the same for both groups
- This simplifies the setup while maintaining functionality

## Future Multi-Token Setup

If you need separate tokens for different groups in the future, the system can be extended to:

1. Store access tokens per group in the database
2. Use different tokens for different group operations
3. Support multiple GroupMe accounts

## Security Notes

- Never commit `.env` files to version control
- Rotate access tokens regularly
- Use environment variables for all sensitive data
- Keep bot IDs and group IDs secure

## Testing

To test with the current setup:

```bash
# Local development
python3 api/index.py

# Access the portal
http://localhost:5001
```

## Deployment URLs

- **Local**: http://localhost:5001
- **Railway**: [Your Railway URL]
- **GitHub**: https://github.com/ShaheerSaud2004/rutgers-msa-groupme-portal
