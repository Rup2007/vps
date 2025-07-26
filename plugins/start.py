import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import *
from database.database import add_user, del_user, full_userbase, present_user

async def delete_after_delay(message: Message, delay):
    await asyncio.sleep(1800)
    await message.delete()

@Bot.on_message(filters.command('start') & filters.private & subscribed1 & subscribed2 & subscribed3)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("tham ja bhai de raha hu ⚡ ")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("iski maa ki chut bhai file nahi hai be ")
            return
        await temp_msg.delete()
        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html
            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None
            try:
                if msg and (msg.text or msg.photo or msg.document or msg.video or msg.audio or msg.sticker or msg.voice or msg.animation or msg.video_note or msg.contact or msg.location or msg.venue or msg.poll):
                    k = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.01)
                    if k is not None:
                        asyncio.create_task(delete_after_delay(k, 1800))
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        await message.reply_text(f"<b><i>\n──────────────────────────\n➥ 𝚃𝚑𝚒𝚜 𝙼𝚊𝚜𝚜𝚊𝚐𝚎 𝚆𝚒𝚕𝚕 𝙱𝚎 𝙳𝚎𝚕𝚎𝚝𝚎𝚍 𝙸𝚗 3 𝙷𝚘𝚞𝚛𝚜.\n➥ 𝙼𝚞𝚜𝚝 𝙹𝚘𝚒𝚗 𝙾𝚞𝚛 𝙲𝚑𝚊𝚗𝚗al</i></b>")
        await message.reply_text(f"<b>➥𝙸𝚏 𝚈𝚘𝚞 𝙷𝚊𝚟𝚎 𝙰𝚗𝚢 𝙿𝚛𝚘𝚋𝚕𝚎𝚖 𝚁𝚎𝚕𝚊𝚝𝚎𝚍 𝚃𝚘 𝙲𝚘𝚗𝚝𝚎𝚗𝚝 𝚃𝚑𝚊𝚝 𝚆𝚊𝚜 𝚁𝚎𝚖𝚘𝚟𝚎𝚍 𝙸𝚗 𝙲𝚑𝚊𝚗𝚗𝚎𝚕/𝙱𝚘𝚝 𝙸𝚜 𝙽𝚘𝚝 𝚆𝚘𝚛𝚔𝚒𝚗𝚐 𝙿𝚛𝚘𝚙𝚎𝚛𝚕𝚢 𝚃𝚑𝚎𝚗  contact paid promotion also available :- @Goat_Me</b>")
        
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("About Me", callback_data = "about"),
                    InlineKeyboardButton("Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

# =====================================================================================##
WAIT_MSG = "<b>Working....</b>"
REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"
# =====================================================================================##
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    user_id = message.from_user.id
    # Check subscription status
    sub1 = await is_subscribed1(None, client, message)
    sub2 = await is_subscribed2(None, client, message)
    sub3 = await is_subscribed3(None, client, message)
    buttons = []
    if sub1 and not sub2 and not sub3:
        # User subscribed to 1, show buttons for 2 and 3
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub2 and not sub1 and not sub3:
        # User subscribed to 2, show buttons for 1 and 3
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub3 and not sub1 and not sub2:
        # User subscribed to 3, show buttons for 1 and 2
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
    elif not sub1 and not sub2 and not sub3:
        # User subscribed to none, show all three buttons
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub1 and sub2 and not sub3:
        # User subscribed to 1 and 2, show button for 3
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink3)])
    elif sub1 and sub3 and not sub2:
        # User subscribed to 1 and 3, show button for 2
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink2)])
    elif sub2 and sub3 and not sub1:
        # User subscribed to 2 and 3, show button for 1
        buttons.append([InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=client.invitelink)])
    elif sub1 and sub2 and sub3:
        # All subscriptions satisfied, no join buttons
        pass
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass
    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ....</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ...</u>
Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

