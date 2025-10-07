#!/usr/bin/env python3
"""
Script to update GroupMe access tokens for different groups
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, db, GroupChat

def update_group_tokens():
    """Update access tokens for both groups"""
    
    with app.app_context():
        # Brothers group token (original user)
        brothers_token = 'HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP'
        brothers_group = GroupChat.query.filter_by(group_id='107939343').first()
        
        if brothers_group:
            brothers_group.access_token = brothers_token
            print(f"✅ Updated brothers group token: {brothers_token[:10]}...")
        else:
            print("❌ Brothers group not found")
        
        # Sisters group token (Amira's token)
        sisters_token = 'BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA'
        sisters_group = GroupChat.query.filter_by(group_id='107937618').first()
        
        if sisters_group:
            sisters_group.access_token = sisters_token
            print(f"✅ Updated sisters group token: {sisters_token[:10]}...")
        else:
            print("❌ Sisters group not found")
        
        # Commit changes
        db.session.commit()
        print("🎉 All tokens updated successfully!")
        
        # Show current groups
        print("\n📋 Current Groups:")
        groups = GroupChat.query.all()
        for group in groups:
            token_preview = group.access_token[:10] + "..." if group.access_token else "None"
            print(f"  - {group.name}: {token_preview}")

if __name__ == "__main__":
    update_group_tokens()
