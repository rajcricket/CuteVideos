# Cute Videos Bot - Telegram Bot for Protected Video Delivery

## Overview

This is a Telegram bot written in Python that serves protected videos from a private channel through a category-based navigation system. The bot integrates with shortener services to monetize video access and implements automatic video deletion for content protection.

## User Preferences

- Preferred communication style: Simple, everyday language
- Keep all files in main directory for easy GitHub upload and Render deployment
- Use python-telegram-bot version 21.1 specifically
- Streamlined single-file architecture for deployment simplicity

## System Architecture

The bot follows a streamlined single-file architecture optimized for deployment:

- **Entry Point**: `main.py` contains all bot functionality in one file
- **Data Storage**: JSON files for categories and videos configuration
- **User Tracking**: Integrated user logging system
- **Protected Video Delivery**: Built-in video forwarding with auto-deletion
- **Shortener Integration**: Direct URL buttons linking to xpshort.com

## Key Components

### Main Application (`main.py`)
- Single-file architecture containing all bot functionality
- Processes `/start` command and deep links from shortener services
- Handles category selection and video navigation with inline keyboards
- Forwards videos from private channel with content protection
- Implements 5-minute auto-deletion timer with protect_content feature
- Creates paginated video lists (5 videos per page)
- Integrated user tracking system logging to JSON file
- Direct shortener link integration via URL buttons

## Data Flow

1. **User Interaction**: User starts bot or clicks shortener link
2. **Category Selection**: Bot presents 3 categories with anime-themed names
3. **Video Navigation**: Users browse paginated video lists
4. **Shortener Integration**: Video buttons contain embedded shortener links
5. **Protected Delivery**: After shortener redirect, bot forwards protected video
6. **Auto-Deletion**: Videos automatically delete after 5 minutes

## External Dependencies

### Telegram Integration
- Uses `python-telegram-bot` library for bot functionality
- Integrates with private Telegram channel for video storage
- Implements Telegram's content protection features

### Shortener Service Integration
- Works with xpshort.com for monetized video access
- Handles deep links returning from shortener service
- Embeds shortener links directly in inline keyboard buttons

### Data Storage
- JSON-based configuration for categories (`categories.json`)
- JSON-based video database (`videos.json`)
- File-based user tracking logs (`user_logs.json`)

## Deployment Strategy

### Environment Configuration
- Bot token configured via environment variable or hardcoded fallback
- Channel ID extracted from video links for private channel access
- No database dependencies - pure file-based storage

### File Structure Requirements
- All files kept in main directory for easy deployment
- JSON configuration files (categories.json, videos.json) in root directory
- Bot requires admin access to private channel "That Friend" for video forwarding
- User logs automatically created and maintained in user_logs.json

### Runtime Features
- Python 3.11 with python-telegram-bot version 21.1
- Single-file architecture for simplified deployment
- Comprehensive error handling and logging
- Easy addition of new categories or videos via JSON files

### Content Management
- Admin manually uploads videos to private channel
- JSON files updated to add/remove videos without code changes
- Bot automatically adapts to configuration changes
- Shortener links embedded directly in video buttons

### Recent Changes (July 13, 2025)
- ✅ Restructured to single-file architecture for easy GitHub/Render deployment
- ✅ Updated to python-telegram-bot version 21.1 as requested
- ✅ Consolidated all functionality into main.py
- ✅ Maintained all original features: categories, pagination, video protection, auto-deletion
- ✅ Bot successfully tested and running with video delivery working properly

The architecture prioritizes deployment simplicity while maintaining robust video protection and user experience features. The system handles shortener-based monetization with protected video delivery in a streamlined single-file design.