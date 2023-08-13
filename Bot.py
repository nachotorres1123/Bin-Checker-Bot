import requests
from pyrogram import Client, filters
from configs import config
from asyncio import sleep
import stripe

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

# Configura tu clave de API de Stripe
stripe.api_key = "sk_live_tuclaveaqui"

def luhn_algorithm(card_number):
    # Función luhn_algorithm se mantiene igual

def validate_credit_card(card_number):
    # Función validate_credit_card se mantiene igual

@Bot.on_message(filters.command("start"))
async def inicio(_, m: Message):
    # Función inicio se mantiene igual

@Bot.on_message(filters.command("ayuda"))
async def ayuda(_, m: Message):
    # Función ayuda se mantiene igual

@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    # Función bin se mantiene igual

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

            # Verifica la tarjeta de crédito con la función validate_credit_card
            es_valida = validate_credit_card(numero_tarjeta)

            # Verifica la tarjeta con la API de Stripe
            try:
                respuesta = stripe.Token.create(card={
                    "number": numero_tarjeta,
                })

                if respuesta and respuesta.get("id"):
                    mensaje = f"La tarjeta de crédito {numero_tarjeta} es válida."
                else:
                    mensaje = f"La tarjeta de crédito {numero_tarjeta} es inválida."
            except stripe.error.CardError as e:
                mensaje = f"Error al verificar la tarjeta: {e}"

            mencion_de = m.from_user.mention
            mensaje += f"\n\nVerificado por: {mencion_de}"

            await mafia.edit_text(mensaje)
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error:\n{e}\n\nPor favor, informa este error al propietario del bot.")

print("¡El bot está en línea!")

Bot.run()
