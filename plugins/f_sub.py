from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import not_subscriber
import re

@Client.on_message(filters.create(not_subscriber))
async def is_not_subscribed(client, message):
    if message.text.startswith('/'): 
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ", url="https://t.me/sd_bots")]]
        text = f"sᴏʀʀʏ {message.from_user.mention}\nʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍʏ ʙᴏᴛ."
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    elif message.text: 
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ", url="https://t.me/sd_bots")]]
        text = f"sᴏʀʀʏ {message.from_user.mention}\nʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍʏ ʙᴏᴛ."
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        return
