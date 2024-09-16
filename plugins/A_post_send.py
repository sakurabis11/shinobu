from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.errors import *

async def send_messages(group_id, message):
    try:
        await message.copy(chat_id=group_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(group_id, message)
    except PeerIdInvalid:
        print(f"{group_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"

@Client.on_message(filters.command("send") & filters.reply & filters.private)
async def send_msg(client:Client, message:Message):
  try:
    user_id = message.from_user.id
    group_id = message.text.split()[1::]
    groupid = "".join(group_id)
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

    suc = await send_messages(groupid, msg)
    if suc:
        await message.reply_text("Success.")
    else:
        await message.reply_text("Something error occured.")
        return
  except Exception as e:
      await message.reply_text(e)


