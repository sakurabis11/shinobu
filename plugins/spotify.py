import pyrogram
from pyrogram import filters, Client
import spotipy
import spotipy.util as util
import requests, re, asyncio
import os, traceback, random
from info import LOG_CHANNEL, LOG_CHANNEL as DUMP_GROUP

# Spotify API credentials (replace with your own)
client_id = 'd3a0f15a75014999945b5628dca40d0a'
client_secret = 'e39d1705e35c47e6a0baf50ff3bb587f'
redirect_uri = 'http://localhost:8080' 
username = '315jpvz6ki4e734f7r6uwvue4ina'
scope = 'user-library-read'

# Authenticate with Spotify API
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
sp = spotipy.Spotify(auth=token)

@Client.on_message(filters.regex(r'https?://open.spotify.com/track/[^\s]+') & filters.incoming)
async def spotify_link_handler(Mbot, message):
    link = message.matches[0].group(0)

    try:
        # Extract track ID from Spotify link
        track_id = link.split("/")[-1]

        # Retrieve song information
        track = sp.track(track_id)

        # Get audio stream URL
        preview_url = sp.audio_features(track_id)[0]['preview_url']

        # Download audio stream
        response = requests.get(preview_url, stream=True)
        downfile = f"{os.getcwd()}/{random.randint(1,10000000)}.ogg"  # Adjust file extension if needed
        with open(downfile, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        # Send downloaded audio as a message
        await message.reply_audio(downfile, caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @mrtgcoderbot")

    except Exception as e:
        # Handle errors (e.g., invalid URLs, API rate limits, download errors)
        traceback.print_exc()
        await message.reply("Oops, something went wrong.")
