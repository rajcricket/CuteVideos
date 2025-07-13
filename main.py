#!/usr/bin/env python3
"""
Cute Videos Bot - Telegram bot for protected video delivery
"""

import asyncio
import logging
import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from telegram.error import TelegramError

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7697080775:AAFU1TZpXHNCMTiBEMiE2e3F9Hk_3DtX3VU")
CHANNEL_ID = "-1002890796928"  # Extracted from video links
VIDEO_DELETE_TIMEOUT = 300  # 5 minutes
VIDEOS_PER_PAGE = 5

# Global data storage
categories_data = {}
videos_data = {}
users_data = {}

def load_json_data():
    """Load configuration data from JSON files."""
    global categories_data, videos_data
    
    try:
        with open('categories.json', 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
    except Exception as e:
        logger.error(f"Error loading categories.json: {e}")
        categories_data = {"categories": []}
    
    try:
        with open('videos.json', 'r', encoding='utf-8') as f:
            videos_data = json.load(f)
    except Exception as e:
        logger.error(f"Error loading videos.json: {e}")
        videos_data = {}

def save_user_data():
    """Save user tracking data."""
    try:
        with open('user_logs.json', 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving user data: {e}")

def track_user(user_id, first_name=None, username=None):
    """Track user interaction."""
    try:
        user_id_str = str(user_id)
        current_time = datetime.now().isoformat()
        
        if user_id_str not in users_data:
            users_data[user_id_str] = {
                "first_seen": current_time,
                "last_seen": current_time,
                "first_name": first_name,
                "username": username,
                "interaction_count": 1
            }
        else:
            users_data[user_id_str]["last_seen"] = current_time
            users_data[user_id_str]["interaction_count"] += 1
            if first_name:
                users_data[user_id_str]["first_name"] = first_name
            if username:
                users_data[user_id_str]["username"] = username
        
        # Save periodically
        if len(users_data) % 10 == 0:
            save_user_data()
            
    except Exception as e:
        logger.error(f"Error tracking user {user_id}: {e}")

def build_categories_keyboard():
    """Build the categories selection keyboard."""
    keyboard = []
    for category in categories_data.get("categories", []):
        button = InlineKeyboardButton(
            category["name"],
            callback_data=category["callback_data"]
        )
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)

def build_videos_keyboard(category, page=1):
    """Build videos keyboard with pagination."""
    if category not in videos_data:
        return InlineKeyboardMarkup([])
    
    videos = videos_data[category]
    total_videos = len(videos)
    total_pages = (total_videos + VIDEOS_PER_PAGE - 1) // VIDEOS_PER_PAGE
    start_idx = (page - 1) * VIDEOS_PER_PAGE
    end_idx = min(start_idx + VIDEOS_PER_PAGE, total_videos)
    
    keyboard = []
    
    # Add video buttons for current page
    video_numbers = list(videos.keys())
    for i in range(start_idx, end_idx):
        if i < len(video_numbers):
            video_num = video_numbers[i]
            video_data = videos[video_num]
            
            # Use shortener link as URL
            button = InlineKeyboardButton(
                f"Video {video_num}",
                url=video_data['shortener_link']
            )
            keyboard.append([button])
    
    # Add navigation buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton("◀️ Back", callback_data=f"page_{category}_{page-1}")
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton("Next ▶️", callback_data=f"page_{category}_{page+1}")
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to categories button
    keyboard.append([
        InlineKeyboardButton("🔙 Back to Categories", callback_data="back_to_categories")
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def send_protected_video(bot, chat_id, video_link, user_id):
    """Send a protected video that auto-deletes after 5 minutes."""
    try:
        if "/c/" in video_link:
            parts = video_link.split("/")
            message_id = int(parts[-1])
            
            # Copy the video from private channel (hides forward source)
            copied_message = await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=CHANNEL_ID,
                message_id=message_id,
                protect_content=True
            )
            
            # Send notification
            notification = await bot.send_message(
                chat_id=chat_id,
                text="💕 Enjoy your video, darling!\n⏰ It will vanish in 5 minutes~ ✨",
                parse_mode=ParseMode.HTML
            )
            
            # Schedule deletion
            asyncio.create_task(
                schedule_video_deletion(bot, chat_id, copied_message.message_id, 
                                      notification.message_id, user_id)
            )
            
            logger.info(f"Protected video sent to user {user_id}")
        else:
            await bot.send_message(chat_id=chat_id, text="❌ Invalid video format.")
            
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await bot.send_message(chat_id=chat_id, text="❌ Error sending video.")

async def schedule_video_deletion(bot, chat_id, video_message_id, notification_message_id, user_id):
    """Schedule video deletion after timeout."""
    try:
        await asyncio.sleep(VIDEO_DELETE_TIMEOUT)
        
        # Delete messages
        try:
            await bot.delete_message(chat_id=chat_id, message_id=video_message_id)
            await bot.delete_message(chat_id=chat_id, message_id=notification_message_id)
            await bot.send_message(chat_id=chat_id, text="✨ Video has been deleted as promised~ 💕")
        except TelegramError as e:
            logger.warning(f"Could not delete messages: {e}")
            
    except Exception as e:
        logger.error(f"Error in schedule_video_deletion: {e}")

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    try:
        user = update.effective_user
        track_user(user.id, user.first_name, user.username)
        
        # Check for deep link from shortener
        if context.args and len(context.args) > 0:
            start_param = context.args[0]
            if start_param.startswith("video_"):
                await handle_video_deep_link(update, context, start_param)
                return
        
        # Show categories menu
        keyboard = build_categories_keyboard()
        welcome_text = (
            "🎬 Welcome Onii‑chan!\n\n"
            "How cute are you feeling today? 💕"
        )
        
        await update.message.reply_text(welcome_text, reply_markup=keyboard)
        logger.info(f"User {user.id} started the bot")
        
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await update.message.reply_text("❌ Something went wrong. Please try again.")

async def handle_video_deep_link(update: Update, context: ContextTypes.DEFAULT_TYPE, start_param: str):
    """Handle video deep link from shortener service."""
    try:
        if start_param.startswith("video_"):
            param_without_prefix = start_param[6:]
            parts = param_without_prefix.split("_")
            
            if len(parts) >= 2:
                number = parts[-1]
                category = "_".join(parts[:-1])
                
                await deliver_video(update, context, category, number)
            else:
                await update.message.reply_text("❌ Invalid video link.")
        else:
            await update.message.reply_text("❌ Invalid video link.")
            
    except Exception as e:
        logger.error(f"Error in handle_video_deep_link: {e}")
        await update.message.reply_text("❌ Error processing video request.")

async def deliver_video(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, video_number: str):
    """Deliver video to user after shortener redirect."""
    try:
        if category not in videos_data or video_number not in videos_data[category]:
            await update.message.reply_text("❌ Video not found.")
            return
        
        video_data = videos_data[category][video_number]
        await send_protected_video(
            bot=context.bot,
            chat_id=update.effective_chat.id,
            video_link=video_data['video_link'],
            user_id=update.effective_user.id
        )
        
    except Exception as e:
        logger.error(f"Error delivering video: {e}")
        await update.message.reply_text("❌ Error processing video.")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()
    
    try:
        callback_data = query.data
        
        if callback_data.startswith("category_"):
            category = callback_data.replace("category_", "")
            await handle_category_selection(query, category)
        elif callback_data.startswith("page_"):
            await handle_pagination(query, callback_data)
        elif callback_data == "back_to_categories":
            await show_categories_menu(query, is_edit=True)
        else:
            await query.edit_message_text("❌ Unknown action.")
            
    except Exception as e:
        logger.error(f"Error in callback_handler: {e}")
        await query.edit_message_text("❌ Something went wrong.")

async def handle_category_selection(query, category):
    """Handle category selection and show video buttons."""
    try:
        keyboard = build_videos_keyboard(category, page=1)
        
        category_names = {
            "cute": "🎀 Onii Chaan",
            "little_cute": "🥺 Little Cute",
            "dark_cute": "😵‍💫 Yamete kudasai"
        }
        
        category_name = category_names.get(category, category)
        message_text = (
            f"💕 {category_name}\n\n"
            "Choose your favorite video, my dear~ 💖\n"
            "⚠️ Videos will disappear in 5 minutes ✨"
        )
        
        await query.edit_message_text(message_text, reply_markup=keyboard)
        logger.info(f"User {query.from_user.id} selected category: {category}")
        
    except Exception as e:
        logger.error(f"Error in handle_category_selection: {e}")
        await query.edit_message_text("❌ Error loading videos.")

async def handle_pagination(query, callback_data):
    """Handle pagination for video lists."""
    try:
        parts = callback_data.split("_")
        if len(parts) >= 3:
            if len(parts) == 4 and (
                (parts[1] == "little" and parts[2] == "cute") or 
                (parts[1] == "dark" and parts[2] == "cute")
            ):
                category = f"{parts[1]}_{parts[2]}"
                page = int(parts[3])
            else:
                category = parts[1]
                page = int(parts[2])
            
            keyboard = build_videos_keyboard(category, page=page)
            
            category_names = {
                "cute": "🎀 Onii Chaan",
                "little_cute": "🥺 Little Cute",
                "dark_cute": "😵‍💫 Yamete kudasai"
            }
            
            category_name = category_names.get(category, category)
            message_text = (
                f"💕 {category_name} (Page {page})\n\n"
                "Choose your favorite video, my dear~ 💖\n"
                "⚠️ Videos will disappear in 5 minutes ✨"
            )
            
            await query.edit_message_text(message_text, reply_markup=keyboard)
            
    except Exception as e:
        logger.error(f"Error in handle_pagination: {e}")
        await query.edit_message_text("❌ Error loading page.")

async def show_categories_menu(query, is_edit=False):
    """Show the categories menu."""
    try:
        keyboard = build_categories_keyboard()
        welcome_text = (
            "🎬 Welcome Onii‑chan!\n\n"
            "How cute are you feeling today? 💕"
        )
        
        if is_edit:
            await query.edit_message_text(welcome_text, reply_markup=keyboard)
        else:
            await query.message.reply_text(welcome_text, reply_markup=keyboard)
            
    except Exception as e:
        logger.error(f"Error in show_categories_menu: {e}")

def main():
    """Main function to run the bot."""
    # Load data
    load_json_data()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Start the bot
    logger.info("Starting Cute Videos Bot...")
    logger.info("Bot is running! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    main()
