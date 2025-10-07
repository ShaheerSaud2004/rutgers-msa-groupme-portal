#!/usr/bin/env python3
"""
Script to fix bot IDs for each group with correct separation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app, db, GroupChat

def fix_bot_ids():
    """Fix bot IDs for each group"""
    
    with app.app_context():
        # Update brothers group with correct bot ID
        brothers_group = GroupChat.query.filter_by(group_id='107939343').first()
        if brothers_group:
            brothers_group.bot_id = 'a890eb8fe19b87fab1fc97fe2a'  # Brothers bot ID
            print(f"✅ Updated brothers group bot ID: {brothers_group.bot_id}")
        
        # Update sisters group with Amira's bot ID
        sisters_group = GroupChat.query.filter_by(group_id='107937618').first()
        if sisters_group:
            sisters_group.bot_id = '0253eda15ad81f240b1c2ce892'  # Amira's bot ID
            print(f"✅ Updated sisters group bot ID: {sisters_group.bot_id}")
        
        # Commit changes
        db.session.commit()
        print("🎉 Bot IDs fixed successfully!")
        
        # Show current groups
        print("\n📋 Current Groups with Correct Bot IDs:")
        groups = GroupChat.query.all()
        for group in groups:
            print(f"  - {group.name}")
            print(f"    Group ID: {group.group_id}")
            print(f"    Bot ID: {group.bot_id}")
            if group.group_id == '107939343':
                print(f"    Access Token: HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP (Original user)")
            elif group.group_id == '107937618':
                print(f"    Access Token: BY3uMTwpFAEqpQAspag7qOAMyvqruRI16a6QkJkA (Amira)")
            print()

if __name__ == "__main__":
    fix_bot_ids()
