# Vercel Deployment Fixes

## Issues Fixed

### 1. TypeError: issubclass() arg 1 must be a class
**Problem**: Incorrect Vercel handler implementation in `api/index.py`
**Solution**: 
- Fixed the handler function to properly import and use the Flask app
- Updated the handler to use the correct Vercel Python runtime format

### 2. OSError: [Errno 30] Read-only file system: '/var/task/instance'
**Problem**: SQLAlchemy trying to create instance directory in read-only filesystem
**Solution**:
- Modified `config.py` to use in-memory SQLite for Vercel deployments
- Removed instance path configuration that was causing filesystem issues
- Added proper environment detection for Vercel vs local development

### 3. Missing Dependencies
**Problem**: `requirements.txt` was incomplete
**Solution**:
- Added all required dependencies: Flask-SQLAlchemy, python-dotenv, Pillow, schedule, Werkzeug
- Specified exact versions for compatibility

### 4. Database Configuration
**Problem**: App trying to use persistent SQLite database on serverless platform
**Solution**:
- Configured in-memory SQLite for Vercel deployments
- Added support for external PostgreSQL database via `DATABASE_URL` environment variable
- Added fallback configuration for different deployment environments

## Configuration Changes

### `api/index.py`
- Simplified to properly import and handle the Flask app
- Fixed Vercel handler function

### `config.py`
- Added Vercel environment detection
- Configured in-memory SQLite for serverless deployment
- Set proper upload directory for Vercel (`/tmp/uploads`)
- Removed problematic instance path configuration

### `app.py`
- Added database initialization on import for Vercel
- Disabled scheduler for Vercel deployments (serverless doesn't support background threads)
- Added error handling for database operations
- Added health check endpoint

### `vercel.json`
- Added VERCEL environment variable
- Maintained proper routing configuration

### `requirements.txt`
- Added all missing dependencies with specific versions

## Environment Variables

Set these in your Vercel dashboard:

```
GROUPME_ACCESS_TOKEN=your_groupme_access_token
DATABASE_URL=postgresql://username:password@host:port/database (optional)
SECRET_KEY=your-secret-key
```

## Deployment Steps

1. Commit all changes to your repository
2. Push to your main branch
3. Vercel will automatically redeploy
4. Check the `/health` endpoint to verify deployment

## Testing

The app now includes:
- `/health` - Simple health check endpoint
- `/` - Main dashboard with error handling
- All existing functionality preserved for local development

## Notes

- Scheduler functionality is disabled on Vercel (serverless limitation)
- Database is in-memory on Vercel (data won't persist between requests)
- For production use, configure a PostgreSQL database via `DATABASE_URL`
- File uploads use `/tmp/uploads` on Vercel (temporary storage)

## Next Steps

1. **Set up external database**: Configure PostgreSQL or another persistent database
2. **Configure environment variables**: Set up all required environment variables in Vercel
3. **Test functionality**: Verify all endpoints work correctly
4. **Consider alternatives**: For scheduled posts, consider using Vercel Cron Jobs or external scheduling services
