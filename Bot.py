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
    # Agregar la lógica para manejar el comando /bin aquí
    pass

@Bot.on_message(filters.command("cck"))
async def cck(_, m: Message):
    # Agregar la lógica para manejar el comando /cck aquí
    pass

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
