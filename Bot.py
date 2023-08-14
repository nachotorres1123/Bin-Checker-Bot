import requests
import subprocess
import sys
from pyrogram import Client, filters
from configs import config
from asyncio import sleep

from pyrogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

# Instalar o actualizar la biblioteca de Stripe
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "stripe"])

import stripe

Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)

def validate_credit_card(card_number):
    response = requests.post(
        "https://api.stripe.com/v1/tokens",
        data={"card[number]": card_number},
        headers={"Authorization": f"Bearer {sk_test_51NeoLxLkYoNV0b9fn6epV2j5fuE6pdRj5fbMBfhV6feUjV14UHDT7ATdvNKHGYcZ6v8xbfOVKFs0lZZXr8iN9fGu00mrZa0Im9}"}
    )

    if response.status_code == 200:
        token = response.json()
        return "Válida"
    else:
        return "Inválida"

@Bot.on_message(filters.command("start"))
async def inicio(_, m: Message):
    mencion_usuario = m.from_user.mention
    teclado = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Canal", url="https://t.me/NtEasyM0ney"),
                InlineKeyboardButton("Soporte", url="https://t.me/NtEasyMoney"),
            ],
            [
                InlineKeyboardButton(
                    "Código fuente", url="https://github.com/ImDenuwan/Bin-Checker-Bot"
                )
            ],
        ]
    )
    await m.reply_text(
        f"Hola, {mencion_usuario}\nPuedo verificar si una tarjeta de crédito es válida o inválida.\n\nPara ver más, usa el comando /ayuda.",
        reply_markup=teclado,
    )

@Bot.on_message(filters.command("ayuda"))
async def ayuda(_, m: Message):
    await m.reply_text(
        "/inicio - Verificar si el bot está activo.\n/ayuda - Ver el menú de ayuda.\n/cck [tarjeta] - Verificar si una tarjeta de crédito es válida o inválida.\n/datos - Obtener datos de una URL."
    )

@Bot.on_message(filters.command("cck"))
async def cck(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("¡Por favor, proporciona una tarjeta de crédito!\nEjemplo: /cck 4111111111111111")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("Procesando...")
            entrada = m.text.split(None, 1)[1]
            numero_tarjeta = entrada

            es_valida = validate_credit_card(numero_tarjeta)

            mencion_de = m.from_user.mention
            mensaje = f"La tarjeta de crédito {numero_tarjeta} es {es_valida}.\n\nVerificado por: {mencion_de}"

            await mafia.edit_text(mensaje)
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error:\n{e}\n\nPor favor, informa este error al propietario del bot.")

print("¡El bot está en línea!")

Bot.run()
