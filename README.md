# GroupMe Portal

A web-based portal for automatically sending messages with images and links to your GroupMe group chats. Perfect for event announcements, poster sharing, and scheduled communications.

## Features

- 🎯 **Multi-Group Support**: Manage multiple GroupMe group chats
- 📅 **Scheduled Posting**: Schedule messages to be sent at specific times
- 🖼️ **Image Upload**: Upload and share posters, event images, and more
- 🔗 **Link Integration**: Include multiple links in your messages
- ⚡ **Immediate Sending**: Send messages instantly or schedule for later
- 📊 **Dashboard**: Overview of your groups and upcoming posts
- 🔄 **Automatic Processing**: Background scheduler handles timed posts

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure GroupMe API

1. Go to [GroupMe Developer Console](https://dev.groupme.com/)
2. Create a new application and get your access token
3. Update the `access_token` in `app.py`:

```python
self.access_token = "YOUR_ACTUAL_ACCESS_TOKEN_HERE"
```

### 3. Create GroupMe Bots

For each group chat you want to send messages to:

1. Go to [GroupMe Bots](https://dev.groupme.com/bots)
2. Click "Create Bot"
3. Select your group chat
4. Give your bot a name (e.g., "Event Bot")
5. Copy the Bot ID

### 4. Add Your Groups

1. Run the application: `python app.py`
2. Go to http://localhost:5000
3. Click "Add Group Chat"
4. Enter:
   - Group Name (friendly name)
   - Group ID (from GroupMe)
   - Bot ID (from step 3)

### 5. Start Creating Posts

1. Click "Create Post"
2. Upload your poster/image
3. Write your message
4. Add links if needed
5. Choose to send immediately or schedule for later

## Usage

### Creating Posts

1. **Upload Images**: Drag and drop or click to upload posters/images
2. **Write Messages**: Compose your message with event details
3. **Add Links**: Include ticket links, event pages, etc.
4. **Schedule**: Set specific date/time or send immediately

### Managing Groups

- Add multiple group chats
- Each group needs its own bot
- View all groups on the dashboard

### Scheduled Posts

- View all scheduled posts
- Edit or delete pending posts
- Monitor sent posts
- Automatic background processing

## File Structure

```
GroupMe/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_group.html
│   ├── create_post.html
│   └── scheduled_posts.html
├── static/               # Static files (CSS, JS, images)
│   └── uploads/          # Uploaded images
└── groupme_portal.db     # SQLite database (created automatically)
```

## API Integration

The portal uses the GroupMe API for:
- Sending messages via bots
- Uploading images
- Managing group communications

## Security Notes

- Never share your GroupMe login credentials
- Use official GroupMe API tokens only
- Keep your access tokens secure
- The portal stores data locally in SQLite

## Troubleshooting

### Bot Not Sending Messages
- Verify the bot is added to the group chat
- Check that the Bot ID is correct
- Ensure your access token is valid

### Images Not Uploading
- Check file size (max 16MB)
- Verify file format (PNG, JPG, GIF)
- Ensure uploads directory exists

### Scheduled Posts Not Sending
- Check that the application is running
- Verify the scheduler is working
- Check the console for error messages

## Support

For issues with:
- **GroupMe API**: Check [GroupMe Developer Documentation](https://dev.groupme.com/docs)
- **Application Issues**: Check the console output for error messages
- **Bot Creation**: Follow the GroupMe bot creation guide

## License

This project is for personal use. Please respect GroupMe's terms of service when using their API.
