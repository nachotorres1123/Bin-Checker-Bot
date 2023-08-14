import requests
from pyrogram import Client, filters
from configs import config
from asyncio import sleep
import random
import string

from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

# Lista para almacenar los usuarios con acceso de administrador
admin_users = []

Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)

# Resto del código...

@Bot.on_message(filters.text & filters.private & filters.command("bin"))
async def bin_command_handler(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("📝 ¡Por favor, proporciona un Bin!\nEjemplo: /bin 401658")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("⌛ Procesando...")
            entrada = m.text.split(None, 1)[1]
            codigo_bin = entrada

            url = f"https://api.apilayer.com/bincheck/{codigo_bin}"

            cabeceras = {
                "apikey": "G6wqRUaOVzlvwlvavzHeefh2j1exTjse"
            }

            respuesta = requests.get(url, headers=cabeceras)

            if respuesta.status_code == 200:
                datos = respuesta.json()
                try:
                    nombre_banco = datos.get("bank_name", "No disponible")
                    marca_tarjeta = datos.get("scheme", "No disponible")
                    pais = datos.get("country", "No disponible")
                    tipo = datos.get("type", "No disponible")
                    bin_numero = datos.get("bin", "No disponible")
                    mencion_de = m.from_user.mention
                    caption = f"""
🏦 Nombre del banco: {nombre_banco}
💳 Marca de la tarjeta: {marca_tarjeta}
🌎 País: {pais}
📋 Tipo: {tipo}
🔢 Número Bin: {bin_numero}

Verificado por: {mencion_de}
Bot creado por: {mencion_de}
Código fuente del bot: [GitHub](https://github.com/ImDenuwan/Bin-Checker-Bot)
"""
                    await mafia.edit_text(caption, disable_web_page_preview=True)
                except KeyError as e:
                    await mafia.edit_text(f"❗ Error: {e}\n\nRespuesta: {respuesta.text}")
            else:
                await mafia.edit_text("❌ Bin inválido o se produjo un error.")
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")

@Bot.on_message(filters.text & filters.private & filters.command("cck"))
async def cck_command_handler(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("💳 ¡Por favor, proporciona una tarjeta de crédito!\nEjemplo: /cck 4111111111111111")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("⌛ Procesando...")
            entrada = m.text.split(None, 1)[1]
            numero_tarjeta = entrada

            # Lógica para validar la tarjeta de crédito
            es_valida = validate_credit_card(numero_tarjeta)

            mencion_de = m.from_user.mention
            mensaje = f"La tarjeta de crédito {numero_tarjeta} es {es_valida}.\n\nVerificado por: {mencion_de} 👤"

            await mafia.edit_text(mensaje)
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")

@Bot.on_message(filters.text & filters.private & filters.command("Scr"))
async def scr_command_handler(_, m: Message):
    try:
        longitud = 12
        if len(m.command) > 1:
            longitud = int(m.command[1])

        # Lógica para generar contraseña segura
        password = generate_password(longitud)

        mensaje = f"🔐 Contraseña generada: `{password}`\n\nGenerada por: {m.from_user.mention} 👤"
        await m.reply_text(mensaje, parse_mode="markdown")

    except Exception as e:
        await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")

# Resto del código...

print("🚀 ¡El bot está en línea! 🚀")

Bot.run()
