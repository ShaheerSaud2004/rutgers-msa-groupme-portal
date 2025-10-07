import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import requests
from datetime import datetime, timedelta
from PIL import Image
import io
import base64
from config import Config

# Set environment variable for Vercel
os.environ['VERCEL'] = '1'

# Configure Flask for Vercel
if os.environ.get('VERCEL'):
    # For Vercel, use /tmp as instance path and ensure it exists
    instance_path = '/tmp'
    os.makedirs(instance_path, exist_ok=True)
    app = Flask(__name__, template_folder='../templates', static_folder='../static', instance_path=instance_path)
else:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.String(50), nullable=False, unique=True)
    bot_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScheduledPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# GroupMe API functions
def upload_image_to_groupme(image_path):
    """Upload image to GroupMe and return the URL"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'access_token': app.config['GROUPME_ACCESS_TOKEN']}
            response = requests.post('https://image.groupme.com/pictures', files=files, data=data)
            
        if response.status_code == 200:
            return response.json()['payload']['url']
        else:
            print(f"Image upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Image upload error: {e}")
        return None

def send_groupme_message(group_id, bot_id, message, image_url=None):
    """Send message to GroupMe group"""
    try:
        url = f"{app.config['GROUPME_BASE_URL']}/bots/post"
        data = {
            'bot_id': bot_id,
            'text': message
        }
        
        if image_url:
            data['attachments'] = [{'type': 'image', 'url': image_url}]
        
        response = requests.post(url, json=data)
        
        if response.status_code == 202:
            return True
        else:
            print(f"Message send failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Message send error: {e}")
        return False

# Routes
@app.route('/')
def index():
    try:
        groups = GroupChat.query.all()
        scheduled_posts = ScheduledPost.query.filter_by(sent=False).order_by(ScheduledPost.scheduled_time).all()
        return render_template('index.html', groups=groups, scheduled_posts=scheduled_posts)
    except Exception as e:
        print(f"Index route error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            group_id = request.form.get('group_id')
            bot_id = request.form.get('bot_id')
            
            if not all([name, group_id, bot_id]):
                flash('All fields are required.', 'error')
                return redirect(url_for('add_group'))
            
            # Check if group already exists
            existing_group = GroupChat.query.filter_by(group_id=group_id).first()
            if existing_group:
                flash('Group with this ID already exists.', 'error')
                return redirect(url_for('add_group'))
            
            new_group = GroupChat(name=name, group_id=group_id, bot_id=bot_id)
            db.session.add(new_group)
            db.session.commit()
            
            flash('Group added successfully!', 'success')
            return redirect(url_for('index'))
        
        return render_template('add_group.html')
    except Exception as e:
        print(f"Add group route error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            message = request.form.get('message')
            image = request.files.get('image')
            send_immediately = request.form.get('send_immediately')
            
            if not title or not message:
                flash('Title and message are required.', 'error')
                return redirect(url_for('create_post'))
            
            image_path = None
            if image and image.filename:
                filename = secure_filename(image.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
            
            if send_immediately:
                # Send immediately to all groups
                groups = GroupChat.query.all()
                success_count = 0
                
                for group in groups:
                    image_url = None
                    if image_path:
                        image_url = upload_image_to_groupme(image_path)
                    
                    if send_groupme_message(group.group_id, group.bot_id, message, image_url):
                        success_count += 1
                
                flash(f'Message sent to {success_count}/{len(groups)} groups!', 'success')
                return redirect(url_for('index'))
            else:
                # Schedule for later
                scheduled_time_str = request.form.get('scheduled_time')
                if not scheduled_time_str:
                    flash('Please select a scheduled time or send immediately.', 'error')
                    return redirect(url_for('create_post'))
                scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
                
                new_post = ScheduledPost(
                    title=title,
                    message=message,
                    image_path=image_path,
                    scheduled_time=scheduled_time
                )
                db.session.add(new_post)
                db.session.commit()
                
                flash('Post scheduled successfully!', 'success')
                return redirect(url_for('index'))
        
        groups = GroupChat.query.all()
        return render_template('create_post.html', groups=groups)
    except Exception as e:
        print(f"Create post route error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/scheduled_posts')
def scheduled_posts():
    try:
        posts = ScheduledPost.query.filter_by(sent=False).order_by(ScheduledPost.scheduled_time).all()
        return render_template('scheduled_posts.html', posts=posts)
    except Exception as e:
        print(f"Scheduled posts route error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    try:
        post = ScheduledPost.query.get_or_404(post_id)
        if post.image_path and os.path.exists(post.image_path):
            os.remove(post.image_path)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('scheduled_posts'))
    except Exception as e:
        print(f"Delete post route error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/test')
def test():
    try:
        return jsonify({
            'status': 'success',
            'message': 'Flask app is working!',
            'vercel': os.environ.get('VERCEL', 'false'),
            'upload_folder': app.config['UPLOAD_FOLDER'],
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI'][:20] + '...' if len(app.config['SQLALCHEMY_DATABASE_URI']) > 20 else app.config['SQLALCHEMY_DATABASE_URI']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Initialize database
try:
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")
except Exception as e:
    print(f"Database initialization error: {e}")

# This is the entry point for Vercel
def handler(request):
    try:
        return app(request.environ, lambda *args: None)
    except Exception as e:
        print(f"Handler error: {e}")
        from flask import Response
        return Response(f"Internal Server Error: {str(e)}", status=500)

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)