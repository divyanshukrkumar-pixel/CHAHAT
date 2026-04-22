import time
import asyncio
from pathlib import Path

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


BASE_DIR = Path(__file__).resolve().parents[3]
NODP_PATH = BASE_DIR / "assets" / "nodp.png"


def get_default_photo() -> str:
    if NODP_PATH.exists():
        return str(NODP_PATH)
    return config.START_IMG_URL


async def send_safe_photo(message: Message, photo: str, caption: str, reply_markup=None):
    try:
        return await message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=reply_markup,
        )
    except Exception:
        return await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=caption,
            reply_markup=reply_markup,
        )


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    try:
        await message.react("❤")
    except Exception:
        pass

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            try:
                await message.reply_sticker(
                    "CAACAgUAAxkBAAEQI1RlTLnRAy4h9lOS6jgS5FYsQoruOAAC1gMAAg6ryVcldUr_lhPexzME"
                )
            except Exception:
                pass

            return await send_safe_photo(
                message=message,
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {username}"
                    ),
                )
            return

        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            try:
                query = str(name).replace("info_", "", 1)
                query = f"https://www.youtube.com/watch?v={query}"
                results = VideosSearch(query, limit=1)
                data = await results.next()

                if not data.get("result"):
                    await m.edit_text("No result found.")
                    return

                result = data["result"][0]
                title = result.get("title", "Unknown")
                duration = result.get("duration", "Unknown")
                views = result.get("viewCount", {}).get("short", "Unknown")
                thumbnail = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
                channellink = result.get("channel", {}).get("link", "")
                channel = result.get("channel", {}).get("name", "Unknown")
                link = result.get("link", "")
                published = result.get("publishedTime", "Unknown")

                searched_text = _["start_6"].format(
                    title, duration, views, published, channellink, channel, app.mention
                )

                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text=_["S_B_8"], url=link),
                            InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                        ],
                    ]
                )

                await m.delete()

                if thumbnail:
                    await app.send_photo(
                        chat_id=message.chat.id,
                        photo=thumbnail,
                        caption=searched_text,
                        reply_markup=key,
                    )
                else:
                    await app.send_message(
                        chat_id=message.chat.id,
                        text=searched_text,
                        reply_markup=key,
                        disable_web_page_preview=True,
                    )

                if await is_on_off(2):
                    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
                    return await app.send_message(
                        chat_id=config.LOGGER_ID,
                        text=(
                            f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                            f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                            f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {username}"
                        ),
                    )
                return

            except Exception:
                try:
                    await m.edit_text("Failed to fetch track details.")
                except Exception:
                    pass
                return

    out = private_panel(_)
    lols = None
    sticker_msg = None

    try:
        lol = await message.reply_text(
            "𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ︎ {}.. ❣️".format(message.from_user.mention)
        )
        await lol.edit_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ {}.. 🥳".format(message.from_user.mention))
        await lol.edit_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ {}.. 💥".format(message.from_user.mention))
        await lol.edit_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ {}.. 🤩".format(message.from_user.mention))
        await lol.edit_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ {}.. 💌".format(message.from_user.mention))
        await lol.edit_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ {}.. 💞".format(message.from_user.mention))
        await lol.delete()

        lols = await message.reply_text("**⚡️ѕ**")
        await asyncio.sleep(0.1)
        await lols.edit_text("⚡ѕт")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтα**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαя**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαят**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятι**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятιи**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятιиg**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятιиg.**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятιиg....**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятιиg.**")
        await asyncio.sleep(0.1)
        await lols.edit_text("**⚡ѕтαятιиg....**")

        try:
            sticker_msg = await message.reply_sticker(
                "CAACAgUAAxkBAAEQI1BlTLmx7PtOO3aPNshEU2gCy7iAFgACNQUAApqMuVeA6eJ50VbvmDME"
            )
        except Exception:
            sticker_msg = None

        userss_photo = None
        if message.chat.photo:
            try:
                userss_photo = await app.download_media(message.chat.photo.big_file_id)
            except Exception:
                userss_photo = None

        chat_photo = userss_photo if userss_photo else get_default_photo()

    except Exception:
        chat_photo = get_default_photo()

    try:
        if lols:
            await lols.delete()
    except Exception:
        pass

    try:
        if sticker_msg:
            await sticker_msg.delete()
    except Exception:
        pass

    await send_safe_photo(
        message=message,
        photo=chat_photo,
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )

    try:
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            await app.send_message(
                config.LOG_GROUP_ID,
                (
                    f"{message.from_user.mention} ʜᴀs sᴛᴀʀᴛᴇᴅ ʙᴏᴛ.\n\n"
                    f"**ᴜsᴇʀ ɪᴅ : {sender_id}\n"
                    f"ᴜsᴇʀ ɴᴀᴍᴇ: {sender_name}**"
                ),
            )
    except Exception:
        pass


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await send_safe_photo(
        message=message,
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await send_safe_photo(
                    message=message,
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
