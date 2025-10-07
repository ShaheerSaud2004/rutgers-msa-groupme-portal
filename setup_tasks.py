#!/usr/bin/env python3
"""
Script to set up default tasks for the Rutgers MSA portal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, db, Task
from datetime import datetime, timedelta

def setup_tasks():
    """Set up default tasks"""
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Clear existing tasks
        Task.query.delete()
        db.session.commit()
        print("✅ Cleared existing tasks")
        
        # Create default tasks
        tasks = [
            Task(
                title="Test Brothers Group Messaging",
                description="Send a test message to the Brothers group to verify the bot and token are working correctly",
                status="pending",
                priority="high",
                due_date=datetime.utcnow() + timedelta(days=1)
            ),
            Task(
                title="Test Sisters Group Messaging", 
                description="Send a test message to the Sisters group to verify Amira's bot and token are working correctly",
                status="pending",
                priority="high",
                due_date=datetime.utcnow() + timedelta(days=1)
            ),
            Task(
                title="Set up Daily Prayer Reminders",
                description="Create daily messages for prayer times to be sent to both groups",
                status="pending",
                priority="medium",
                due_date=datetime.utcnow() + timedelta(days=3)
            ),
            Task(
                title="Create Event Announcement Template",
                description="Design a template for announcing MSA events with consistent formatting",
                status="pending",
                priority="medium",
                due_date=datetime.utcnow() + timedelta(days=5)
            ),
            Task(
                title="Test Image Upload Functionality",
                description="Verify that poster and image uploads work correctly for both groups",
                status="in_progress",
                priority="medium",
                due_date=datetime.utcnow() + timedelta(days=2)
            ),
            Task(
                title="Document Portal Usage",
                description="Create user guide for other MSA members on how to use the portal",
                status="pending",
                priority="low",
                due_date=datetime.utcnow() + timedelta(days=7)
            )
        ]
        
        for task in tasks:
            db.session.add(task)
            print(f"✅ Created task: {task.title}")
        
        # Commit all changes
        db.session.commit()
        print("🎉 All tasks set up successfully!")
        
        # Show current tasks
        print("\n📋 Current Tasks:")
        all_tasks = Task.query.all()
        for task in all_tasks:
            print(f"  - {task.title} ({task.status}, {task.priority} priority)")

if __name__ == "__main__":
    setup_tasks()
