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
import stripe

# Instalar o actualizar la biblioteca de Stripe
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "stripe"])

Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)

# Configura tu clave secreta de Stripe
stripe.api_key = "sk_test_51NeoLxLkYoNV0b9fn6epV2j5fuE6pdRj5fbMBfhV6feUjV14UHDT7ATdvNKHGYcZ6v8xbfOVKFs0lZZXr8iN9fGu00mrZa0Im9"

def validate_credit_card(card_number):
    try:
        response = stripe.Token.create(
            card={
                "number": card_number,
            }
        )
        return "Válida"
    except stripe.error.CardError as e:
        return "Inválida"

# ... Resto del código ...

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
