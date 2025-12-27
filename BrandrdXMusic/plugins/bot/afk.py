import time
import re

from pyrogram.enums import MessageEntityType
from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.mongo.readable_time import get_readable_time
from BrandrdXMusic.mongo.afkdb import add_afk, is_afk, remove_afk


@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return

    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)

    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time(int(time.time() - timeafk))

            if afktype == "text":
                await message.reply_text(
                    f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ "
                    f"ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    disable_web_page_preview=True,
                )

            elif afktype == "text_reason":
                await message.reply_text(
                    f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ "
                    f"ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
                    f"ʀᴇᴀsᴏɴ: `{reasonafk}`",
                    disable_web_page_preview=True,
                )

        except Exception:
            await message.reply_text(
                f"**{message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ",
                disable_web_page_preview=True,
            )

    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = message.text.split(None, 1)[1][:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    else:
        return

    await add_afk(user_id, details)
    await message.reply_text(f"{message.from_user.first_name} ɪs ɴᴏᴡ ᴀғᴋ!")


chat_watcher_group = 1


@app.on_message(
    ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(_, message: Message):
    if message.sender_chat:
        return

    userid = message.from_user.id
    user_name = message.from_user.first_name
    msg = ""

    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time(int(time.time() - timeafk))

            if afktype == "text":
                msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ (ᴀғᴋ {seenago})\n\n"
            elif afktype == "text_reason":
                msg += (
                    f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ (ᴀғᴋ {seenago})\n\n"
                    f"ʀᴇᴀsᴏɴ: `{reasonafk}`\n\n"
                )
        except Exception:
            msg += f"**{user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ\n\n"

    if msg:
        try:
            await message.reply_text(msg, disable_web_page_preview=True)
        except Exception:
            pass
