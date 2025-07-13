#!/usr/bin/env python3
"""
User Data Viewer for Cute Videos Bot
Run this script to view user analytics and tracking data.
"""

import json
import os
from datetime import datetime

def load_user_data():
    """Load user tracking data from user_logs.json"""
    if not os.path.exists('user_logs.json'):
        print("❌ No user data found. Users need to interact with the bot first.")
        return {}
    
    try:
        with open('user_logs.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading user data: {e}")
        return {}

def format_timestamp(timestamp_str):
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

def display_user_stats(users_data):
    """Display user statistics and details"""
    if not users_data:
        print("📊 No user data available yet.")
        return
    
    total_users = len(users_data)
    total_interactions = sum(user.get('interaction_count', 0) for user in users_data.values())
    
    print("=" * 60)
    print("📊 CUTE VIDEOS BOT - USER ANALYTICS")
    print("=" * 60)
    print(f"👥 Total Users: {total_users}")
    print(f"💬 Total Interactions: {total_interactions}")
    print(f"📈 Average Interactions per User: {total_interactions/total_users:.1f}")
    print("=" * 60)
    
    print("\n👤 USER DETAILS:")
    print("-" * 60)
    
    for user_id, user_data in users_data.items():
        print(f"User ID: {user_id}")
        print(f"  📝 Name: {user_data.get('first_name', 'Unknown')}")
        print(f"  🔗 Username: @{user_data.get('username', 'Not set')}")
        print(f"  🕐 First Seen: {format_timestamp(user_data.get('first_seen', 'Unknown'))}")
        print(f"  🕑 Last Seen: {format_timestamp(user_data.get('last_seen', 'Unknown'))}")
        print(f"  💬 Interactions: {user_data.get('interaction_count', 0)}")
        print("-" * 40)

def main():
    """Main function to display user analytics"""
    print("🔍 Loading user data...")
    users_data = load_user_data()
    display_user_stats(users_data)
    
    print(f"\n📁 Data file location: {os.path.abspath('user_logs.json')}")
    print("💡 Tip: User data updates automatically as users interact with the bot.")

if __name__ == "__main__":
    main()