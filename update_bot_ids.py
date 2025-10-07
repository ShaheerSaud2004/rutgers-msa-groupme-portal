#!/usr/bin/env python3
"""
Script to update bot IDs for each group
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, db, GroupChat

def update_bot_ids():
    """Update bot IDs for each group"""
    
    with app.app_context():
        # Update brothers group with its bot ID
        brothers_group = GroupChat.query.filter_by(group_id='107939343').first()
        if brothers_group:
            # You'll need to provide the brothers bot ID
            print("Brothers group found. Please provide the brothers bot ID.")
            print(f"Current bot ID: {brothers_group.bot_id}")
        
        # Update sisters group with Amira's bot ID
        sisters_group = GroupChat.query.filter_by(group_id='107937618').first()
        if sisters_group:
            sisters_group.bot_id = '0253eda15ad81f240b1c2ce892'  # Amira's bot ID
            print(f"✅ Updated sisters group bot ID: {sisters_group.bot_id}")
        
        # Commit changes
        db.session.commit()
        print("🎉 Bot IDs updated successfully!")
        
        # Show current groups
        print("\n📋 Current Groups:")
        groups = GroupChat.query.all()
        for group in groups:
            print(f"  - {group.name}")
            print(f"    Group ID: {group.group_id}")
            print(f"    Bot ID: {group.bot_id}")
            print()

if __name__ == "__main__":
    update_bot_ids()
