from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import requests
import json
from datetime import datetime, timedelta
import schedule
import time
import threading
from PIL import Image
import io
import base64
from config import Config

app = Flask(__name__)
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

class GroupMeAPI:
    def __init__(self):
        self.base_url = app.config['GROUPME_BASE_URL']
        self.access_token = app.config['GROUPME_ACCESS_TOKEN']
    
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

# Initialize GroupMe API
groupme_api = GroupMeAPI()

@app.route('/')
def index():
    """Main dashboard"""
    group_chats = GroupChat.query.all()
    upcoming_posts = ScheduledPost.query.filter(
        ScheduledPost.scheduled_time > datetime.utcnow(),
        ScheduledPost.is_sent == False
    ).order_by(ScheduledPost.scheduled_time).limit(5).all()
    
    return render_template('index.html', 
                         group_chats=group_chats, 
                         upcoming_posts=upcoming_posts)

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
            
            # Check if this is a recurring post
            is_recurring = request.form.get('recurring') == 'on'
            posts_created = 0
            
            if is_recurring:
                # Create multiple posts for recurring schedule
                interval = int(request.form.get('recurring_interval', 1))
                unit = request.form.get('recurring_unit', 'days')
                
                # Calculate time delta
                if unit == 'hours':
                    delta = timedelta(hours=interval)
                elif unit == 'days':
                    delta = timedelta(days=interval)
                elif unit == 'weeks':
                    delta = timedelta(weeks=interval)
                else:
                    delta = timedelta(days=interval)
                
                # Create posts for the next 4 occurrences
                current_time = scheduled_time
                for i in range(4):
                    new_post = ScheduledPost(
                        title=f"{title} (Recurring #{i+1})",
                        message=message,
                        image_path=image_path,
                        links=links,
                        group_chat_id=group_chat_id,
                        scheduled_time=current_time
                    )
                    db.session.add(new_post)
                    posts_created += 1
                    current_time += delta
                
                flash(f'Recurring post scheduled successfully! Created {posts_created} scheduled posts.', 'success')
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
                # Upload image if present
                image_url = None
                if post.image_path and os.path.exists(post.image_path):
                    image_url = groupme_api.upload_image(post.image_path)
                
                # Send message
                success = groupme_api.send_message(group_chat.bot_id, post.message, image_url)
                
                if success:
                    post.is_sent = True
                    db.session.commit()
                    print(f"Sent scheduled post: {post.title}")
                else:
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
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
