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

Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)

def luhn_algorithm(card_number):
    card_number = card_number.replace(" ", "")  # 🧹 Elimina los espacios en blanco
    card_digits = [int(digit) for digit in card_number]
    card_digits.reverse()

    total = 0
    for i, digit in enumerate(card_digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0

def validate_credit_card(card_number):
    if luhn_algorithm(card_number):
        return "Válida ✅"
    else:
        return "Inválida ❌"

def generate_password(length=12):
    characters = string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@Bot.on_message(filters.command("start"))
async def inicio(_, m: Message):
    mencion_usuario = m.from_user.mention
    teclado = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Canal", url="https://t.me/NtEasyM0ney"),
                InlineKeyboardButton("💬 Soporte", url="https://t.me/NtEasyMoney"),
            ],
            [
                InlineKeyboardButton(
                    "Pasar A Premium 🏆", url="https://t.me/NtEasyMoney"
                )
            ],
        ]
    )
    await m.reply_text(
        f"Hola, {mencion_usuario} 👋\nPuedo verificar si un Bin es válido o inválido y generar contraseñas seguras.\n\nPara ver más, usa el comando /ayuda.",
        reply_markup=teclado,
    )

@Bot.on_message(filters.command("ayuda"))
async def ayuda(_, m: Message):
    await m.reply_text(
        "📚 **Menú de ayuda** 📚\n\n"
        "🏠 /inicio - Verificar si el bot está activo.\n"
        "❓ /ayuda - Ver el menú de ayuda.\n"
        "💳 /bin [consulta] - Verificar si un Bin es válido o inválido.\n"
        "💳 /cck [tarjeta] - Verificar si una tarjeta de crédito es válida o inválida.\n"
        "🔐 /Scr [longitud] - Generar una contraseña segura (opcional: longitud de la contraseña, por defecto: 12 caracteres).\n"
        "🌐 /datos - Obtener datos de una URL.🚫"
    )

@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("📝 ¡Por favor, proporciona un Bin!\nEjemplo: /bin 401658")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("⌛ Verificando el Bin...")
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
                    mensaje = f"🏦 **Información del Bin Verificada** 🏦\n\n"
                    mensaje += f"**Nombre del Banco:** {nombre_banco}\n"
                    mensaje += f"**Marca de la Tarjeta:** {marca_tarjeta}\n"
                    mensaje += f"**País:** {pais}\n"
                    mensaje += f"**Tipo:** {tipo}\n"
                    mensaje += f"**Número Bin:** {bin_numero}\n\n"
                    mensaje += f"Verificado por: {mencion_de} 👤\n"
                    mensaje += "[Admin 🏆](https://t.me/NtEasyMoney) - Haste Premium"

                    await mafia.edit_text(mensaje, disable_web_page_preview=True)
                except KeyError as e:
                    await mafia.edit_text(f"❗ Error: {e}\n\nRespuesta: {respuesta.text}")
            else:
                await mafia.edit_text("❌ Bin inválido o se produjo un error.")
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")

@Bot.on_message(filters.command("cck"))
async def cck(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("💳 Por favor, proporciona una tarjeta de crédito.\nEjemplo: /cck 4111111111111111")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("⌛ Verificando la tarjeta de crédito...")
            entrada = m.text.split(None, 1)[1]
            numero_tarjeta = entrada

            es_valida = validate_credit_card(numero_tarjeta)

            mencion_de = m.from_user.mention
            mensaje = f"🛒 Tarjeta de Crédito: `{numero_tarjeta}`\n"
            mensaje += f"🔍 Estado: **{es_valida}**\n"
            mensaje += f"👤 Verificado por: {mencion_de}"

            await mafia.edit_text(mensaje, parse_mode="markdown")
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")


@Bot.on_message(filters.command("Scr"))
async def scr_command_handler(_, m: Message):
    try:
        longitud = 16
        if len(m.command) > 1:
            longitud = int(m.command[1])

        password = generate_password(longitud)

        mensaje = f"🔐 **Contraseña Generada** 🔐\n\n"
        mensaje += f"Contraseña: `{password}`\n\n"
        mensaje += f"Generada por: {m.from_user.mention} 👤"

        await m.reply_text(mensaje, parse_mode="markdown")

    except Exception as e:
        error_message = "¡Ups! Se produjo un error al generar la contraseña. 😓\n\n"
        error_message += f"Error: {e} ❗\n\n"
        error_message += "Por favor, informa este error al propietario del bot."
        await m.reply_text(error_message)

# Resto del código...

print("🚀 ¡El bot está en línea! 🚀")

Bot.run()
