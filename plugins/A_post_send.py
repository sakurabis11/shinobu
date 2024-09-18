from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.errors import *
import asyncio

async def send_messages(group_id, message):
        idd=await message.copy(chat_id=group_id)
        messageid = idd.id
        return messageid

@Client.on_message(filters.command("get_id"))
async def get_i_d(client:Client, message:Message):
    chat_type = message.chat.type
    if chat_type in [enums.ChatType.CHANNEL]:
        id = message.chat.id
        r=await message.reply(f"<code>/send {id}</code>\n\ncopy this command and reply to the post that you wanna to send to your channel. This message will delete in 8 seconds.")
        await asyncio.sleep(8)
        await r.delete()

    elif chat_type in [enums.ChatType.PRIVATE, enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return

@Client.on_message(filters.command("send") & filters.reply & filters.private)
async def send_msg(client:Client, message:Message):
  try:
    uid = message.from_user.id
    user_id = int(uid)
    group_id = message.text.split()[1::]
    gid = "".join(group_id)
    groupid = int(gid)
    msg = message.reply_to_message

    me = await client.get_me()

    user = await client.get_chat_member(groupid , user_id)
    if user.status not in [enums.ChatMemberStatus.OWNER , enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.reply_text("You are not allowed to use this command")
        return

    bot = await client.get_chat_member(groupid , me.id)
    if bot.status not in [enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.reply_text("Please promote me as admin.")
        return

    m_id = await send_messages(groupid, msg)
    if m_id:
        
        await message.reply_text(f"Success")
        await client.pin_chat_message(groupid, m_id)
    else:
        await message.reply_text("Something error occured.")
        return
  except Exception as e:
      await message.reply_text(e)
