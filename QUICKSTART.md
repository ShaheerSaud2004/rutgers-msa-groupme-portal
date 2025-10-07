# 🚀 Quick Start Guide

Get your GroupMe Portal up and running in 5 minutes!

## Step 1: Setup

```bash
python setup.py
```

This will:
- Install all required packages
- Create necessary directories
- Set up configuration files

## Step 2: Get Your GroupMe API Token

1. Go to [GroupMe Developer Console](https://dev.groupme.com/)
2. Sign in with your GroupMe account
3. Create a new application
4. Copy your access token

## Step 3: Configure Your Token

Edit the `.env` file and replace `YOUR_ACCESS_TOKEN_HERE` with your actual token:

```bash
GROUPME_ACCESS_TOKEN=your_actual_token_here
```

## Step 4: Create GroupMe Bots

For each group chat you want to send messages to:

1. Go to [GroupMe Bots](https://dev.groupme.com/bots)
2. Click "Create Bot"
3. Select your group chat
4. Name your bot (e.g., "Event Bot")
5. Copy the Bot ID

## Step 5: Start the Portal

```bash
python run.py
```

Open your browser to: http://localhost:5000

## Step 6: Add Your Groups

1. Click "Add Group Chat"
2. Enter:
   - **Group Name**: Friendly name (e.g., "Event Planning")
   - **Group ID**: From GroupMe (found in group settings)
   - **Bot ID**: From step 4

## Step 7: Create Your First Post

1. Click "Create Post"
2. Upload a poster/image
3. Write your message
4. Add links if needed
5. Choose to send immediately or schedule for later

## 🎉 You're Done!

Your GroupMe Portal is now ready to automatically send messages with images and links to your group chats!

## Need Help?

- Check the full [README.md](README.md) for detailed instructions
- Make sure your bots are added to the group chats
- Verify your API token is correct
- Check the console for any error messages

## Security Note

Never share your GroupMe login credentials (7323148699 / Capricorn@72) with anyone or any service. Use only the official GroupMe API tokens for integration.
