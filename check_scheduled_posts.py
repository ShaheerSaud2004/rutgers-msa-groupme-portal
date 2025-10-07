#!/usr/bin/env python3
"""
Script to check scheduled posts in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, db, ScheduledPost, GroupChat

def check_scheduled_posts():
    """Check what scheduled posts exist in the database"""
    
    with app.app_context():
        # Get all scheduled posts
        all_posts = ScheduledPost.query.all()
        print(f"Total scheduled posts in database: {len(all_posts)}")
        
        # Get unsent posts
        unsent_posts = ScheduledPost.query.filter(ScheduledPost.is_sent == False).all()
        print(f"Unsent scheduled posts: {len(unsent_posts)}")
        
        # Show details
        for post in unsent_posts:
            group = GroupChat.query.get(post.group_chat_id)
            group_name = group.name if group else "Unknown Group"
            print(f"  - {post.title}")
            print(f"    Group: {group_name}")
            print(f"    Scheduled: {post.scheduled_time}")
            print(f"    Sent: {post.is_sent}")
            print()

if __name__ == "__main__":
    check_scheduled_posts()
