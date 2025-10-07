#!/usr/bin/env python3
"""
Simple setup script to create groups without access_token column
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the old model structure
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a simple app for setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groupme_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple GroupChat model without access_token
class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.String(100), nullable=False, unique=True)
    bot_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def setup_groups():
    """Set up both groups"""
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Clear existing groups
        GroupChat.query.delete()
        db.session.commit()
        print("✅ Cleared existing groups")
        
        # Create brothers group
        brothers_group = GroupChat(
            name="RUmmah Brothers '25-26",
            group_id="107939343",
            bot_id="0253eda15ad81f240b1c2ce892"
        )
        db.session.add(brothers_group)
        print("✅ Created brothers group")
        
        # Create sisters group
        sisters_group = GroupChat(
            name="RUmmah Sisters '25-26 💫",
            group_id="107937618",
            bot_id="0253eda15ad81f240b1c2ce892"
        )
        db.session.add(sisters_group)
        print("✅ Created sisters group")
        
        # Commit all changes
        db.session.commit()
        print("🎉 All groups set up successfully!")
        
        # Show current groups
        print("\n📋 Current Groups:")
        groups = GroupChat.query.all()
        for group in groups:
            print(f"  - {group.name}")
            print(f"    Group ID: {group.group_id}")
            print(f"    Bot ID: {group.bot_id}")
            print()

if __name__ == "__main__":
    setup_groups()
