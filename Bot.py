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
                InlineKeyboardButton("Channel", url="https://t.me/NtEasyM0ney"),
                InlineKeyboardButton("Support", url="https://t.me/NtEasyMoney"),
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://t.me/NtEasyM0ney"
                )
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://t.me/NtEasyM0ney"
                )
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://t.me/NtEasyM0ney"
                )
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://t.me/NtEasyM0ney"
                )
            ],



            
        ]
    )
    await m.reply_text(
        f"Hi! {messy} \nI can Check bins Valid or Invalid.\n\nTo see more check /help command",
        reply_markup=keyboard,
    )


@Bot.on_message(filters.command("help"))
async def help(_, m: Message):
    await m.reply_text(
        "/start - To check bot alive.\n/help - To see help menu.\n/bin [qoury] - To check Bin is valide or Invalid."
    )


@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("Please Provide a Bin!\nEx:- /bin 401658")
        await sleep(15)
        await msg.delete()

    else:
        try:
            mafia = await m.reply_text("processing...")
            inputm = m.text.split(None, 1)[1]
            bincode = 6
            ask = inputm[:bincode]

            # Hacer una solicitud GET a la API de bincheck.io
            url = f"https://lookup.bincheck.io/bin/{ask}"
            response = requests.get(url)
            data = response.json()

            # Analizar los datos JSON devueltos por la API
            success = data['success']
            if not success:
                return await mafia.edit("❌ #INVALID_BIN ❌\n\nPlease provide a valid bin.")
            card = data['card']
            country = card['country']
            brand = card['brand']
            card_type = card['type']
            level = card['level']
            bank = card['bank']

            # Formatear la salida en Markdown
            mfrom = m.from_user.mention
            caption = f"""
    ╔ Valid :- {success} ✅\n╚ Bin :- {ask}\n\n╔ Brand :- {brand}\n╠ Type :- {card_type}\n╚ Level :- {level}\n\n╔ Bank :- {bank} ({country})\n\n↠ Checked By :- {mfrom}\n↠ Bot By :- [Denuwan](https://github.com/ImDenuwan/Bin-Checker-Bot)
    """
            await mafia.edit(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await bot.reply_text(f"Oops Error!\n{e}\n\nReport This Bug to Bot Owner.")

print("Bot IS Alive Now")

Bot.run()
