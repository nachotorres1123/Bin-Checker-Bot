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

@Bot.on_message(filters.private)
async def check_access(_, m: Message):
    user_id = m.from_user.id
    if user_id in admin_users:
        return  # Si el usuario es un administrador, permite el acceso completo
    if m.text and m.text.startswith("/access "):
        provided_key = m.text.split(None, 1)[1]
        if provided_key == config.ACCESS_KEY:
            admin_users.append(user_id)
            await m.reply_text("🔓 Acceso concedido. ¡Ahora tienes acceso de administrador!")
        else:
            await m.reply_text("🚫 Clave de acceso incorrecta. Acceso denegado.")
    elif not m.text.startswith(("/start", "/access")):
        await m.reply_text("🚫 Acceso denegado. Proporciona la clave de acceso utilizando el comando /access [clave].")

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
                    "🔍 Código fuente", url="https://github.com/ImDenuwan/Bin-Checker-Bot"
                )
            ],
        ]
    )
    await m.reply_text(
        f"Hola, {mencion_usuario} 👋\nPuedo verificar si un Bin es válido o inválido, y generar contraseñas seguras.\n\nPara ver más, usa el comando /ayuda.",
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
        "🌐 /datos - Obtener datos de una URL.\n"
        "🔑 /access [clave] - Proporcionar acceso de administrador utilizando la clave."
    )

@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("📝 ¡Por favor, proporciona un Bin!\nEjemplo: /bin 401658")
        await sleep(15)
        await msg.delete()
    else:
        # Código para el comando /bin
        pass

@Bot.on_message(filters.command("cck"))
async def cck(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("💳 ¡Por favor, proporciona una tarjeta de crédito!\nEjemplo: /cck 4111111111111111")
        await sleep(15)
        await msg.delete()
    else:
        # Código para el comando /cck
        pass

@Bot.on_message(filters.command("Scr"))
async def scr(_, m: Message):
    try:
        longitud = 12
        if len(m.command) > 1:
            longitud = int(m.command[1])
        
        password = generate_password(longitud)

        mensaje = f"🔐 Contraseña generada: `{password}`\n\nGenerada por: {m.from_user.mention} 👤"
        await m.reply_text(mensaje, parse_mode="markdown")

    except Exception as e:
        await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")

# Resto del código...

print("🚀 ¡El bot está en línea! 🚀")

Bot.run()
