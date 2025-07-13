# Deployment Guide for Cute Videos Bot

## For GitHub + Render Deployment

### 1. Files to Upload to GitHub:
**Essential Files:**
- `main.py` (main bot application)
- `categories.json` (category configuration) 
- `videos.json` (video links and shortener configuration)
- `DEPLOYMENT.md` (this guide)

**Optional Files:**
- `replit.md` (project documentation)
- `user_logs.json` (auto-generated user tracking)

### 2. Render Setup:

**Environment Variables:**
- `BOT_TOKEN`: Your bot token (optional if hardcoded in main.py)

**Build Configuration:**
- Build Command: `pip install python-telegram-bot==21.1`
- Start Command: `python main.py`
- Python Version: 3.11

**Auto-Deploy:** Enable from GitHub repository

### 3. Important Notes:

**✅ What Works Automatically:**
- Single-file architecture works perfectly on Render
- JSON files load correctly from repository
- User tracking creates user_logs.json automatically
- Bot restarts automatically on deployment
- All video protection features work

**⚠️ Requirements:**
- Bot token must be valid
- Bot must be admin in private channel "That Friend"
- Channel ID (-1002890796928) must be accessible
- Shortener links in videos.json must be working

**🔧 No Code Changes Needed:**
The bot is designed for easy deployment - just upload files and deploy!

## File Structure
```
project/
├── main.py           # Main bot application
├── categories.json   # Category configuration
├── videos.json      # Video links and shortener data
└── user_logs.json   # Auto-generated user tracking file
```

## Bot Configuration
- **Bot Username:** @CuteVideos_bot
- **Private Channel:** "That Friend" (Channel ID: -1002890796928)
- **Video Auto-delete:** 5 minutes
- **Videos per page:** 5

## Features
- Category-based video navigation
- Shortener link integration (xpshort.com)
- Protected video delivery (no download/forward)
- Automatic video deletion after 5 minutes
- User tracking and analytics
- Pagination for large video collections