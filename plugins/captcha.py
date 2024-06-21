import pyrogram
from pyrogram import Client , filters , enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram.errors import UserNotParticipant
from pyromod import Message
from pyrogram import filters
from pyromod import listen
from pyromod.exceptions import ListenerTimeout
import random
import string

import asyncio

user_status = {}

@Client.on_chat_join_request()
async def auto_request(client: Client, message: ChatMemberUpdated):
    chat_id = message.chat.id
    title = message.chat.title
    user_id = message.from_user.id
    global user_status
    print(user_id)
    try:
        letters = string.ascii_letters
        digits = string.digits

        desired_length = 10
        all_chars = ''.join(random.sample(letters , 5) + random.sample(digits , 5))

        password = ''.join(random.choice(all_chars) for _ in range(desired_length))

        user_status.update(user_id=user_id,chat_id=chat_id,title=title ,captcha=password)
        print(user_status)
        passw = user_status.get('captcha')

        if chat_type == enums.ChatType.PRIVATE
             v=await client.send_message(chat_id=user_id, text=f"Hello {message.from_user.mention}\n\n<code>{str(passw)}</code>")
             c = await client.listen(user_id)
             print(f"captcha is {c.text}")
             print(c)
             if c.text == passw:
                 await client.send_message(chat_id=user_id, text="crt")
                 return

    except Exception as e:
        await client.send_message(user_id, text=e)


