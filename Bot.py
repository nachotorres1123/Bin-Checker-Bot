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
                InlineKeyboardButton("Buy", url="https://t.me/NtEasyMoney"),
                InlineKeyboardButton("Free", url="https://t.me/NtEasyMoney"),
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
            req = import requests

url = "https://bin-ip-checker.p.rapidapi.com/"

querystring = {"bin":"448590"}

payload = { "bin": "448590" }
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "8591782eb8msh35855b7b3e23774p11ee22jsncda4429bc4ec",
	"X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers, params=querystring)

print(response.json())
            da = req
            print(da)
            if "False" in str(da):
                return await mafia.edit("❌ #INVALID_BIN ❌\n\nPlease provide a valid bin.")
            #da = req["data"]
            bi = str(da["bin"])
            ve = str(da["card"])
            #ve = da["vendor"]
            ty = str(da["type"])
            le = str(da["level"])
            ban = str(da["bank"])
            co = str(da["country"])
            cc = str(da["countrycode"])
            #nm = cc["name"]
            #em = cc["emoji"]
            #cod = cc["code"]
            #dial = cc["dialCode"]

            mfrom = m.from_user.mention
            caption = f"""
    ╔ Valid :- Yes ✅\n╚ Bin :- {bi}\n\n╔ Brand :- {ve}\n╠ Type :- {ty}\n╚ Level :- {le}\n\n╔ Bank :- {ban} ({co})\n╠ Country :- {co} {cc}\n╚ DialCode :- {da['phone']}\n\n↠ Checked By :- {str(mfrom)}\n↠ Bot By :- [Denuwan](https://github.com/ImDenuwan/Bin-Checker-Bot)
    """
            await mafia.edit(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await mafia.reply_text(f"Oops Error!\n{e}\n\nReport This Bug to Bot Owner.")

print("Bot IS Alive Now")

Bot.run()
   #da = req["data"]
            bi = str(da["bin"])
            ve = str(da["card"])
            #ve = da["vendor"]
            ty = str(da["type"])
            le = str(da["level"])
            ban = str(da["bank"])
            co = str(da["country"])
            cc = str(da["countrycode"])
            #nm = cc["name"]
            #em = cc["emoji"]
            #cod = cc["code"]
            #dial = cc["dialCode"]

            mfrom = m.from_user.mention
            caption = f"""
    ╔ Valid :- Yes ✅\n╚ Bin :- {bi}\n\n╔ Brand :- {ve}\n╠ Type :- {ty}\n╚ Level :- {le}\n\n╔ Bank :- {ban} ({co})\n╠ Country :- {co} {cc}\n╚ DialCode :- {da['phone']}\n\n↠ Checked By :- {str(mfrom)}\n↠ Bot By :- [Denuwan](https://github.com/ImDenuwan/Bin-Checker-Bot)
    """
            await mafia.edit(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await mafia.reply_text(f"Oops Error!\n{e}\n\nReport This Bug to Bot Owner.")

prin
