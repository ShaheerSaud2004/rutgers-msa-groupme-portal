from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import sys
import requests
import json
from datetime import datetime, timedelta
import schedule
import time
import threading
from PIL import Image
import io
import base64

# Configuration class
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rutgers-msa-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///groupme_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # GroupMe API settings
    GROUPME_ACCESS_TOKEN = os.environ.get('GROUPME_ACCESS_TOKEN') or 'BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA'
    GROUPME_BASE_URL = 'https://api.groupme.com/v3'

# Set template and static folders to parent directory
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.String(100), nullable=False, unique=True)
    bot_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScheduledPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    links = db.Column(db.Text)  # JSON string of links
    group_chat_id = db.Column(db.Integer, db.ForeignKey('group_chat.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    is_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MessageHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    links = db.Column(db.Text)
    group_chat_id = db.Column(db.Integer, db.ForeignKey('group_chat.id'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(50), default='manual')  # manual, scheduled, daily
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

class GroupMeAPI:
    def __init__(self, access_token=None, group_id=None):
        self.base_url = app.config['GROUPME_BASE_URL']
        
        # Select token based on group ID
        if group_id:
            if group_id == '107939343':  # Brothers group
                self.access_token = os.environ.get('BROTHERS_ACCESS_TOKEN') or 'HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP'
            elif group_id == '107937618':  # Sisters group
                self.access_token = os.environ.get('SISTERS_ACCESS_TOKEN') or 'BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA'
            else:
                self.access_token = access_token or app.config['GROUPME_ACCESS_TOKEN']
        else:
            self.access_token = access_token or app.config['GROUPME_ACCESS_TOKEN']
    
    def send_message(self, bot_id, text, image_url=None):
        """Send a message to GroupMe via bot"""
        url = f"{self.base_url}/bots/post"
        
        data = {
            "bot_id": bot_id,
            "text": text
        }
        
        if image_url:
            # Use the proper attachment format for images
            data["attachments"] = [
                {
                    "type": "image",
                    "url": image_url
                }
            ]
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            return response.status_code == 202
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def upload_image(self, image_path):
        """Upload image to GroupMe and return URL"""
        # Use the correct GroupMe image service endpoint
        url = "https://image.groupme.com/pictures"
        
        with open(image_path, 'rb') as image_file:
            headers = {
                'X-Access-Token': self.access_token,
                'Content-Type': 'image/jpeg'  # GroupMe expects this content type
            }
            
            try:
                response = requests.post(url, headers=headers, data=image_file)
                print(f"Image upload response: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    return result['payload']['url']
                else:
                    print(f"Image upload failed: {response.text}")
                    return None
            except Exception as e:
                print(f"Error uploading image: {e}")
                return None

@app.route('/')
def index():
    """Main dashboard"""
    group_chats = GroupChat.query.all()
    upcoming_posts = ScheduledPost.query.filter(
        ScheduledPost.scheduled_time > datetime.utcnow(),
        ScheduledPost.is_sent == False
    ).order_by(ScheduledPost.scheduled_time).limit(5).all()
    
    # Get current tasks
    current_tasks = Task.query.filter(
        Task.status.in_(['pending', 'in_progress'])
    ).order_by(Task.priority.desc(), Task.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         group_chats=group_chats, 
                         upcoming_posts=upcoming_posts,
                         current_tasks=current_tasks)

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    """Add a new GroupMe group chat"""
    if request.method == 'POST':
        name = request.form['name']
        group_id = request.form['group_id']
        bot_id = request.form['bot_id']
        
        # Check if group already exists
        existing_group = GroupChat.query.filter_by(group_id=group_id).first()
        if existing_group:
            flash('Group with this ID already exists!', 'error')
            return redirect(url_for('add_group'))
        
        new_group = GroupChat(name=name, group_id=group_id, bot_id=bot_id)
        db.session.add(new_group)
        db.session.commit()
        
        flash('Group added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_group.html')

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    """Create a new post (immediate or scheduled)"""
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        group_chat_id = request.form['group_chat_id']
        links = request.form.get('links', '')
        
        # Handle file upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)
        
        # Check if immediate or scheduled
        if request.form.get('send_immediately') == 'on':
            # Send immediately
            group_chat = GroupChat.query.get(group_chat_id)
            if group_chat:
                # Initialize GroupMe API with group-specific token
                groupme_api = GroupMeAPI(group_id=group_chat.group_id)
                
                # Upload image if present
                image_url = None
                image_upload_failed = False
                if image_path and os.path.exists(image_path):
                    print(f"Uploading image: {image_path}")
                    image_url = groupme_api.upload_image(image_path)
                    if image_url:
                        print(f"Image uploaded successfully: {image_url}")
                    else:
                        print("Image upload failed, sending text-only message")
                        image_upload_failed = True
                
                # Send message
                print(f"Sending message to bot {group_chat.bot_id}: {message}")
                success = groupme_api.send_message(group_chat.bot_id, message, image_url)
                print(f"Message sent successfully: {success}")
                
                # Record in message history
                history_entry = MessageHistory(
                    title=title,
                    message=message,
                    image_path=image_path,
                    links=links,
                    group_chat_id=group_chat_id,
                    message_type='manual',
                    success=success
                )
                db.session.add(history_entry)
                db.session.commit()
                
                if success:
                    if image_upload_failed:
                        flash('Message sent successfully, but image upload failed. GroupMe image service may be temporarily unavailable.', 'warning')
                    else:
                        flash('Message sent successfully!', 'success')
                else:
                    flash('Failed to send message. Please check your bot configuration.', 'error')
        else:
            # Schedule for later
            scheduled_time_str = request.form.get('scheduled_time')
            if not scheduled_time_str:
                flash('Please select a scheduled time or send immediately.', 'error')
                return redirect(url_for('create_post'))
            scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
            
            # Check recurring type
            repeat_type = request.form.get('repeat_type', 'none')
            posts_created = 0
            
            if repeat_type == 'daily':
                # Handle daily recurring
                daily_time = request.form.get('daily_time', '09:00')
                daily_days = int(request.form.get('daily_days', 7))
                
                current_date = scheduled_time.date()
                for day in range(daily_days):
                    daily_datetime = datetime.combine(current_date, datetime.strptime(daily_time, '%H:%M').time())
                    new_post = ScheduledPost(
                        title=f"{title} (Day {day+1})",
                        message=message,
                        image_path=image_path,
                        links=links,
                        group_chat_id=group_chat_id,
                        scheduled_time=daily_datetime
                    )
                    db.session.add(new_post)
                    posts_created += 1
                    current_date += timedelta(days=1)
                
                flash(f'Daily messages scheduled successfully! Created {posts_created} scheduled posts.', 'success')
            
            elif repeat_type == 'weekly':
                # Handle weekly recurring
                weekly_time = request.form.get('weekly_time', '09:00')
                weekly_weeks = int(request.form.get('weekly_weeks', 4))
                weekly_day = request.form.get('weekly_day', 'monday')
                
                # Calculate the first occurrence of the selected day
                current_date = scheduled_time.date()
                day_offset = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(weekly_day)
                first_occurrence = current_date + timedelta(days=(day_offset - current_date.weekday()) % 7)
                
                for week in range(weekly_weeks):
                    weekly_datetime = datetime.combine(first_occurrence, datetime.strptime(weekly_time, '%H:%M').time())
                    new_post = ScheduledPost(
                        title=f"{title} (Week {week+1})",
                        message=message,
                        image_path=image_path,
                        links=links,
                        group_chat_id=group_chat_id,
                        scheduled_time=weekly_datetime
                    )
                    db.session.add(new_post)
                    posts_created += 1
                    first_occurrence += timedelta(weeks=1)
                
                flash(f'Weekly messages scheduled successfully! Created {posts_created} scheduled posts.', 'success')
            
            else:
                # Single scheduled post
                new_post = ScheduledPost(
                    title=title,
                    message=message,
                    image_path=image_path,
                    links=links,
                    group_chat_id=group_chat_id,
                    scheduled_time=scheduled_time
                )
                
                db.session.add(new_post)
                posts_created = 1
                flash('Post scheduled successfully!', 'success')
            
            db.session.commit()
        
        return redirect(url_for('index'))
    
    group_chats = GroupChat.query.all()
    return render_template('create_post.html', group_chats=group_chats)

@app.route('/scheduled_posts')
def scheduled_posts():
    """View all scheduled posts"""
    posts = ScheduledPost.query.filter(
        ScheduledPost.is_sent == False
    ).order_by(ScheduledPost.scheduled_time).all()
    
    return render_template('scheduled_posts.html', posts=posts)

@app.route('/message_history')
def message_history():
    """View message history"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get all message history with pagination
    history = MessageHistory.query.order_by(MessageHistory.sent_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get all groups for reference
    groups = {group.id: group for group in GroupChat.query.all()}
    
    return render_template('message_history.html', history=history, groups=groups)

@app.route('/update_group_tokens', methods=['POST'])
def update_group_tokens():
    """Update access tokens for groups"""
    brothers_token = request.form.get('brothers_token')
    sisters_token = request.form.get('sisters_token')
    
    # Update brothers group (Group ID: 107939343)
    brothers_group = GroupChat.query.filter_by(group_id='107939343').first()
    if brothers_group and brothers_token:
        brothers_group.access_token = brothers_token
        print(f"Updated brothers group token: {brothers_token[:10]}...")
    
    # Update sisters group (Group ID: 107937618)
    sisters_group = GroupChat.query.filter_by(group_id='107937618').first()
    if sisters_group and sisters_token:
        sisters_group.access_token = sisters_token
        print(f"Updated sisters group token: {sisters_token[:10]}...")
    
    db.session.commit()
    flash('Group access tokens updated successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete a scheduled post"""
    post = ScheduledPost.query.get_or_404(post_id)
    
    # Delete associated image file
    if post.image_path and os.path.exists(post.image_path):
        os.remove(post.image_path)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('scheduled_posts'))

def send_scheduled_posts():
    """Function to send scheduled posts (runs in background)"""
    with app.app_context():
        current_time = datetime.utcnow()
        posts_to_send = ScheduledPost.query.filter(
            ScheduledPost.scheduled_time <= current_time,
            ScheduledPost.is_sent == False
        ).all()
        
        for post in posts_to_send:
            group_chat = GroupChat.query.get(post.group_chat_id)
            if group_chat:
                # Initialize GroupMe API with group-specific token
                groupme_api = GroupMeAPI(group_id=group_chat.group_id)
                
                # Upload image if present
                image_url = None
                if post.image_path and os.path.exists(post.image_path):
                    image_url = groupme_api.upload_image(post.image_path)
                
                # Send message
                success = groupme_api.send_message(group_chat.bot_id, post.message, image_url)
                
                # Record in message history
                history_entry = MessageHistory(
                    title=post.title,
                    message=post.message,
                    image_path=post.image_path,
                    links=post.links,
                    group_chat_id=post.group_chat_id,
                    message_type='scheduled',
                    success=success
                )
                db.session.add(history_entry)
                
                if success:
                    post.is_sent = True
                    db.session.commit()
                    print(f"Sent scheduled post: {post.title}")
                else:
                    db.session.commit()
                    print(f"Failed to send scheduled post: {post.title}")

def run_scheduler():
    """Run the scheduler in a separate thread"""
    schedule.every(1).minutes.do(send_scheduled_posts)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Initialize database
with app.app_context():
    db.create_all()
    print("Database initialized successfully")

# Start scheduler in background thread (only in production)
if os.environ.get('VERCEL') or os.environ.get('RAILWAY_ENVIRONMENT'):
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

# Vercel handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
