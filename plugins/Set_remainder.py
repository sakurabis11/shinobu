from hydrogram import Client, filters
from hydrogram.types import *
from hydrogram.errors import *
import pymongo
from pymongo import MongoClient
import os
from os import environ
from info import DATABASE_URI, DATABASE_NAME
import imdb

ia = imdb.IMDb()

client = MongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db["remainder"]

@Client.on_message(filters.command("set") & filters.private)
async def search_movie(client, message):
  try:
    movie_name = " ".join(message.text.split()[1::])
    if not movie_name:
        await message.reply_text("ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ  /sᴇᴀʀᴄʜ ᴍᴏᴠɪᴇɴᴀᴍᴇ")
        return
    s = await message.reply_text(f"sᴇᴀʀᴄʜɪɴɢ {movie_name}")
    movies = ia.search_movie(movie_name)

    if movies:
        first_movie = movies[0]
        movie_title = first_movie['title']
        url = first_movie.get('full-size cover url')
        year = first_movie['year']

        keyboard = [
            [InlineKeyboardButton("Sᴇᴛ Rᴇᴍɪɴᴅᴇʀ", callback_data=f"set_reminder_{movie_name}")]
        ]
        await client.send_photo(
            chat_id=message.chat.id,
            photo=url ,
            caption=f"ᴛɪᴛʟᴇ: <code> {movie_title}</code> \nYᴇᴀʀ: <code>{year}</code> \n\nDᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴛ ᴀ ʀᴇᴍɪɴᴅᴇʀ ғᴏʀ ᴛʜɪs ᴍᴏᴠɪᴇ?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        await s.delete()
    else:
        await client.send_message(
            chat_id=message.chat.id,
            text="Mᴏᴠɪᴇ ɴᴏᴛ ғᴏᴜɴᴅ."
        )
        await s.delete()
  except Exception as e:
      await s.edit(e)

@Client.on_callback_query(filters.regex(r"^set_reminder_(\w+)"))
async def set_reminder(client, callback_query):
    movie_name = callback_query.data.split("_")[2]
    movie_name = "".join(movie_name)
    user_id = callback_query.from_user.id

    existing_reminder = collection.find_one({
        "user_id": user_id,
        "movie_name": movie_name
    })

    if existing_reminder:
        await client.send_message(
            chat_id=user_id,
            text="Yᴏᴜ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀ ʀᴇᴍɪɴᴅᴇʀ sᴇᴛ ғᴏʀ ᴛʜɪs ᴍᴏᴠɪᴇ."
        )
    else:
        collection.insert_one({
            "user_id": user_id,
            "movie_name": movie_name
        })

        await client.send_message(
            chat_id=user_id,
            text="Rᴇᴍɪɴᴅᴇʀ sᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ."
        )

