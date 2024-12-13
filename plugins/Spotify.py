import re
from pyrogram import Client, filters, enums
import os
import requests
import base64
import os, wget
import random
import shutil

client_id = "d3a0f15a75014999945b5628dca40d0a"
client_secret = "e39d1705e35c47e6a0baf50ff3bb587f"
credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')

def get_access_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

from os import environ

API_ID = int(os.environ.get('API_ID', '8914119'))
API_HASH = os.environ.get('API_HASH', '652bae601b07c928b811bdb310fdb4b0')
BOT_TOKEN = os.environ.get('SESSION', '7851303993:AAHYvJLSM3g2nzFKI0r4FrD4fvtrZw52tns')

user = Client("my_account", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@user.on_message(filters.regex(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)'))
async def spotify(client, message):


    access_token = get_access_token()

    song_name_or_url = message.text
    match = re.match(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)', song_name_or_url)
    if match:

       song_id = match.group(1)
    else:

        song_name = song_name_or_url
        url = f'https://api.spotify.com/v1/search?q={song_name}&type=album,track'
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        item = data["tracks"]["items"][0]
        song_id = item["id"]

    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    vthumbnail_url = data["album"]["images"][0]["url"]
    vartist = data["artists"][0]["name"]
    vname = data["name"]
    valbum = data["album"]["name"]
    vrelease_date = data["album"]["release_date"]


    url = "https://saavn.dev/api/search/songs"

    querystring = {"query":vname}

    response = requests.get(url, params=querystring)
    req = response.json()

    song_id = req['data']['results'][0]['id']
    song_name = req['data']['results'][0]['name']
    song_language = req['data']['results'][0]['language']
    song_url = req['data']['results'][0]['url']
    song_downloadurl = req['data']['results'][0]['downloadUrl'][4]['url']

    thumb = wget.download(vthumbnail_url)
    music = wget.download(song_downloadurl)

    ffile = music.replace("mp4", "mp3")
    os.rename(music, ffile)

    await message.reply_photo(photo=thumb, caption=f"Name: {vname}\nAlbum: {valbum}\nLanguage: {song_language}\nRelease date: {vrelease_date}")
    
    await message.reply_audio(audio=ffile, title=vname, caption=vname, thumb=thumb)
     
    os.remove(ffile)
    os.remove(thumb)

print("run")
user.run()
