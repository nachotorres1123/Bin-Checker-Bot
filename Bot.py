<?php

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'https://bin-ip-checker.p.rapidapi.com/?bin=448590', [
	'body' => '{
    "bin": "448590"
}',
	'headers' => [
		'X-RapidAPI-Host' => 'bin-ip-checker.p.rapidapi.com',
		'X-RapidAPI-Key' => '8591782eb8msh35855b7b3e23774p11ee22jsncda4429bc4ec',
		'content-type' => 'application/json',
	],
]);

echo $response->getBody();


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
            mafia = await m.reply_text("Buscando Datos...")
            inputm = m.text.split(None, 1)[1]
            bincode = 6
            ask = inputm[:bincode]
            req = requests.get(f"https://madbin.herokuapp.com/api/{ask}").json()
            res = req["result"]

            if res == False:
                return await mafia.edit("❌ #INVALID_BIN ❌\n\nPlease provide a valid bin.")
            da = req["data"]
            bi = da["bin"]
            ve = da["vendor"]
            ty = da["type"]
            le = da["level"]
            ban = da["bank"]
            co = da["country"]
            cc = da["countryInfo"]
            nm = cc["name"]
            em = cc["emoji"]
            cod = cc["code"]
            dial = cc["dialCode"]

            mfrom = m.from_user.mention
            caption = f"""
    ╔ Valid :- {res} ✅\n╚ Bin :- {bi}\n\n╔ Brand :- {ve}\n╠ Type :- {ty}\n╚ Level :- {le}\n\n╔ Bank :- {ban} ({co})\n╠ Country :- {nm} {em}\n╠ Alpha2 :- {cod}\n╚ DialCode :- {dial}\n\n↠ Checked By :- {mfrom}\n↠ Bot By :- [Denuwan](https://github.com/ImDenuwan/Bin-Checker-Bot)
    """
            await mafia.edit(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await bot.reply_text(f"Oops Error!\n{e}\n\nReport This Bug to Bot Owner.")

print("Bot IS Alive Now")

Bot.run()
