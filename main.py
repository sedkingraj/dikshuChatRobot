from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import requests
import os
import re


API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 
KUKI_API = os.environ.get("HANA_API", None) 
ERROR_LOG = os.environ.get("ERROR_LOG", None) 
MONGO_URL = os.environ.get("MONGO_URL", None)


bot = Client(
    "HanaChatRobot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


@bot.on_message(
    filters.command("chatbot", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def addchat(_, message): 
    hanadb = MongoClient(MONGO_URL)
    
    hana = hanadb["HanaDb"]["Hana"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "» ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ. | ᴄʜʟᴀ ᴊᴀ ʙsᴅᴋ ʙɴᴀ ᴅᴜ ᴏᴡɴᴇʀ 😂"
            )
    is_hana = hana.find_one({"chat_id": message.chat.id})
    if not is_hana:
        hana.insert_one({"chat_id": message.chat.id})
        await message.reply_text(f"✅ | sᴜᴄᴄᴇssғᴜʟʟʏ\nʜᴀɴᴀ ᴄʜᴀᴛʙᴏᴛ ᴏɴ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ ɪs sᴇᴛ ᴛᴏ @{message.chat.username}\n ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n ᴛᴇᴄʜ ǫᴜᴀʀᴅ")
    else:
        await message.reply_text(f"» ᴀʟʀᴇᴀᴅʏ sᴇᴛᴜᴘ ʜᴀɴᴀ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ ɪs @{message.chat.username}")


@bot.on_message(
    filters.command("offchatbot", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def rmchat(_, message): 
    hanadb = MongoClient(MONGO_URL)
    
    hana = hanadb["HanaDb"]["Hana"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "» ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ. | ᴄʜʟᴀ ᴊᴀ ʙsᴅᴋ ʙɴᴀ ᴅᴜ ᴏᴡɴᴇʀ 😂"
            )
    is_hana = hana.find_one({"chat_id": message.chat.id})
    if not is_hana:
        await message.reply_text("» ᴀʟʀᴇᴀᴅʏ ʜᴀɴᴀ ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ")
    else:
        hana.delete_one({"chat_id": message.chat.id})
        await message.reply_text("✅ | ʜᴀɴᴀ ᴄʜᴀᴛʙᴏᴛ ɪs ᴅɪsᴀʙʟᴇ")





@bot.on_message(
    filters.text
    & filters.reply
    & ~filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def hanaai(client: Client, message: Message):

   hanadb = MongoClient(MONGO_URL)
    
   hana = hanadb["HanaDb"]["Hana"] 

   is_hana = hana.find_one({"chat_id": message.chat.id})
   if is_hana:
       if message.reply_to_message:      
           botget = await bot.get_me()
           botid = botget.id
           if not message.reply_to_message.from_user.id == botid:
               return
           await bot.send_chat_action(message.chat.id, "typing")
           if not message.text:
               msg = "/"
           else:
               msg = message.text
           try: 
               x = requests.get(f"https://kukiapi.xyz/api/apikey={HANA_API}/message={msg}").json()
               x = x['reply']
               await asyncio.sleep(1)
           except Exception as e:
               error = str(e)
           await message.reply_text(x)
           await bot.send_message(
           ERROR_LOG, f"""{error}""")
           await bot.send_chat_action(message.chat.id, "cencel") 
   


@bot.on_message(
    filters.text
    & filters.reply
    & filters.private
    & ~filters.bot
    & ~filters.edited,
    group=2,
)
async def hanaai(client: Client, message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    if not message.text:
        msg = "/"
    else:
        msg = message.text
    try:
        x = requests.get(f"https://kukiapi.xyz/api/apikey={HANA_API}/message={msg}").json()
        x = x['reply']
        await asyncio.sleep(1)
    except Exception as e:
        ERROR = str(e)
    await message.reply_text(x)
    await bot.send_message(
           ERROR_LOG, f"""{ERROR}""")
    await bot.send_chat_action(message.chat.id, "cancel")



@bot.on_message(
    filters.command("chat", prefixes=["/", ".", "?", "-"]))
async def hanaai(client: Client, message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    if not message.text:
        msg = "/"
    else:
        msg = message.text.replace(message.text.split(" ")[0], "")
    try:
        x = requests.get(f"https://kukiapi.xyz/api/apikey={HANA_API}/message={msg}").json()
        x = x['reply']
        await asyncio.sleep(1)
    except Exception as e:
        ERROR = str(e)
    await bot.send_message(
           ERROR_LOG, f"""{ERROR}""")
    await message.reply_text(x)
    





@bot.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
                  [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/TechQuard"),
                   InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/TechQuardSupport"),
                  ][InlineKeyboardButton(text="ᴄʟɪᴄᴋ ʜᴇʀᴇ", url=f"t.me/HanachatRobot?start")]])
        await message.reply("ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴇʀsᴏɴᴀʟ",
                            reply_markup=buttons)
        
    else:
        buttons = [[
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/HanaChatRobot?startgroup=true")
        ],
        
        [
            InlineKeyboardButton("👥 ᴏғғɪᴄɪᴀʟ ɢʀᴏᴜᴘ", url="https://t.me/TechQuardSupport"),
            InlineKeyboardButton("📣 ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url="https://t.me/TechQuard")
        ],
        [
            InlineKeyboardButton("💠 ʏᴏᴜᴛᴜʙᴇ 💠", url="https://youtube.com/channel/UCtI7hbY-BD7wvuIzoSU0cEw")
        ]]
        Photo = "https://te.legra.ph/file/b9eab8788d5c8bcb85f9f.jpg"
        await message.reply_photo(Photo, caption=f"""ʜᴇʟʟᴏ [{message.from_user.first_name}](tg://user?id={message.from_user.id}),
*ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀʀᴛɪғɪᴄᴀʟ ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ ᴄʜᴀᴛ ʙᴏᴛ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀʟᴋ ᴀʙᴏᴜᴛ ᴀɴʏ ᴛᴏᴘɪᴄ ɪɴ ᴀɴʏ ʟᴀɴɢᴜᴀɢᴇ.*
➖➖➖➖➖➖➖➖➖➖➖➖➖
➛ ɪғ ʏᴏᴜ ᴀʀᴇ ғᴇᴇʟɪɴɢ ʟᴏɴᴇʟʏ, ʏᴏᴜ ᴄᴀɴ ᴀʟᴡᴀʏs ᴄᴏᴍᴇ ᴛᴏ ᴍᴇ ᴀɴᴅ ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ
➛ ᴛʀʏ ᴛʜᴇ ʜᴇʟᴘ ᴄᴍᴅs. ᴛᴏ ᴋɴᴏᴡ ᴍʏ ᴀʙɪʟɪᴛɪᴇs ××""", reply_markup=InlineKeyboardMarkup(buttons))



@bot.on_message(filters.command(["help"], prefixes=["/", "!"]))
async def help(client, message):
    self = await bot.get_me()
    busername = self.username
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="ᴄʟɪᴄᴋ ʜᴇʀᴇ",
                url=f"t.me/HanaChatRobot?start=help_")]])
        await message.reply("ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴇʀsᴏɴᴀʟ",
                            reply_markup=buttons)
        
    else: 
        await message.reply_photo("https://te.legra.ph/file/cf6db920f0fe84daae6a3.jpg , https://te.legra.ph/file/b9eab8788d5c8bcb85f9f.jpg")   
        await message.reply_text("➛ /start - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n➛ /chat - sᴇɴᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜɪs ʙᴏᴛ\n➛ /chatbot - ᴀᴄᴛɪᴠᴇ ʜᴀɴᴀ ᴄʜᴀᴛʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n➛ /offchatbot - ᴅɪsᴀʙʟᴇ ʜᴀɴᴀ ᴄʜᴀᴛʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ")






bot.run()

