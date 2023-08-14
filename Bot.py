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

def validate_credit_card(card_number, exp_month, exp_year):
    try:
        response = stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year
            }
        )
        
        # Obtener información adicional de la tarjeta usando el ID del token
        card_info = stripe.Customer.create(source=response.id).sources.data[0]
        
        return card_info
    except stripe.error.CardError as e:
        return None

# ... Resto del código ...

@Bot.on_message(filters.command("cck"))
async def cck(_, m: Message):
    if len(m.command) < 4:
        msg = await m.reply_text("¡Por favor, proporciona una tarjeta de crédito válida!\nEjemplo: /cck 4111111111111111 12 23")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("Procesando...")
            entrada = m.text.split(None, 1)[1]
            params = entrada.split()
            
            numero_tarjeta = params[0]
            exp_month = params[1]
            exp_year = params[2]

            card_info = validate_credit_card(numero_tarjeta, exp_month, exp_year)
            
            if card_info:
                info_text = f"Información de la tarjeta:\n"
                info_text += f"Número de tarjeta: {card_info.last4}\n"
                info_text += f"Marca: {card_info.brand}\n"
                info_text += f"País: {card_info.country}\n"
                info_text += f"Tipo: {card_info.funding}\n"
                info_text += f"MES ID: {card_info.customer}\n"

                mencion_de = m.from_user.mention
                mensaje = f"La tarjeta de crédito {numero_tarjeta} es Válida.\n\n{info_text}\nVerificado por: {mencion_de}"
                await mafia.edit_text(mensaje)
            else:
                mensaje = f"La tarjeta de crédito {numero_tarjeta} es Inválida."
                await mafia.edit_text(mensaje)

        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error:\n{e}\n\nPor favor, informa este error al propietario del bot.")

print("¡El bot está en línea!")

Bot.run()
