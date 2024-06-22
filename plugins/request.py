from pyrogram import Client , filters , enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import *
from pyrogram.errors import UserNotParticipant
from pyrogram import filters
from pyromod.exceptions import ListenerTimeout
import random
import string



@Client.on_chat_join_request()
async def auto_request(client: Client, message: ChatMemberUpdated):
  try:
    chat_id = message.chat.id
    title = message.chat.title
    user_id = message.from_user.id
    global user_status
    print(user_id)
    letters = string.ascii_letters
    digits = string.digits

    desired_length = 6
    all_chars = ''.join(random.sample(digits , 6))

    password = ''.join(random.choice(all_chars) for _ in range(desired_length))

    
    chat_type=message.chat.type
    if enums.ChatType.PRIVATE:
     try:
       c = await client.ask(user_id , f"Hello {message.from_user.mention}\n\n📃 Enter the below 6-digit captcha to join in {title}\n\n📝 Captcha: {str(password)}\n\n⏳ Time Out: 2 Min (120 Sec)" ,
                         filters=filters.text, timeout=120)
       
       
       if user_id == message.from_user.id:
           if c.text == password:
               await client.approve_chat_join_request(chat_id , user_id)
               await client.send_photo(chat_id=user_id , photo="https://telegra.ph/file/abce311b41052c52bc8ec.jpg" ,
                                       caption=f"Hello {message.from_user.mention}\n\nYou're joined in {title} Successfully")
               return

           elif c.text != passw:
               await client.send_message(user_id, text=f"The captcha is wrong")

               return
     except ListenerTimeout:
       await client.send_message(user_id, text='You took too long to answer.')

  except Exception as e:
     await client.send_message(user_id, text=e)
