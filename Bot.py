import requests
from pyrogram import Client, filters
from configs import config
from asyncio import sleep

from pyrogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)

@Bot.on_message(filters.command("start"))
async def start(_, m: Message):
    messy = m.from_user.mention
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Channel", url="https://t.me/NtEasyM0ney"),
                InlineKeyboardButton("Support", url="https://t.me/NtEasyMoney"),
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://github.com/ImDenuwan/Bin-Checker-Bot"
                )
            ],
        ]
    )
    await m.reply_text(
        f"Hi! {messy}\nI can check if a Bin is Valid or Invalid.\n\nTo see more, use the /help command.",
        reply_markup=keyboard,
    )

@Bot.on_message(filters.command("help"))
async def help(_, m: Message):
    await m.reply_text(
        "/start - Check if the bot is alive.\n/help - See the help menu.\n/bin [query] - Check if a Bin is valid or invalid."
    )

@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("Please provide a Bin!\nExample: /bin 401658")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("Processing...")
            inputm = m.text.split(None, 1)[1]
            bincode = len(inputm)
            
            api_key = "0d6542332875d2012b12f3c9d17b8007"
            url = "https://api.bincodes.com/bin"
            headers = {
                "Accept-Version": "3",
                "Authorization": f"Bearer {api_key}",
            }
            payload = {"bin": inputm}
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                bank_name = data["bank"]["name"]
                card_brand = data["scheme"]
                mfrom = m.from_user.mention
                caption = f"""
Bank Name: {bank_name}\nCard Brand: {card_brand}\n\nChecked By: {m.from_user.mention}\nBot By: {mfrom}\nBot Source Code: [GitHub](https://github.com/ImDenuwan/Bin-Checker-Bot)
"""
                await m.edit_message_text(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await m.reply_text(f"Oops! An error occurred:\n{e}\n\nPlease report this bug to the bot owner.")

print("Bot is alive now!")

Bot.run()
