#!/usr/bin/env python3
"""
Script to set up both groups with their correct access tokens
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, db, GroupChat
from datetime import datetime

def setup_groups():
    """Set up both groups with their correct access tokens"""
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Clear existing groups
        GroupChat.query.delete()
        db.session.commit()
        print("✅ Cleared existing groups")
        
        # Create brothers group with original token
        brothers_group = GroupChat(
            name="RUmmah Brothers '25-26",
            group_id="107939343",
            bot_id="0253eda15ad81f240b1c2ce892",
            access_token="HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP"
        )
        db.session.add(brothers_group)
        print("✅ Created brothers group with original token")
        
        # Create sisters group with Amira's token
        sisters_group = GroupChat(
            name="RUmmah Sisters '25-26 💫",
            group_id="107937618",
            bot_id="0253eda15ad81f240b1c2ce892",
            access_token="BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA"
        )
        db.session.add(sisters_group)
        print("✅ Created sisters group with Amira's token")
        
        # Commit all changes
        db.session.commit()
        print("🎉 All groups set up successfully!")
        
        # Show current groups
        print("\n📋 Current Groups:")
        groups = GroupChat.query.all()
        for group in groups:
            token_preview = group.access_token[:10] + "..." if group.access_token else "None"
            print(f"  - {group.name}")
            print(f"    Group ID: {group.group_id}")
            print(f"    Bot ID: {group.bot_id}")
            print(f"    Token: {token_preview}")
            print()

if __name__ == "__main__":
    setup_groups()
