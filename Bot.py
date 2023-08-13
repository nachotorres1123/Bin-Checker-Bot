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
        f"Hola, {mencion_usuario}\nPuedo verificar si un Bin es válido o inválido.\n\nPara ver más, usa el comando /ayuda.",
        reply_markup=teclado,
    )

@Bot.on_message(filters.command("ayuda"))
async def ayuda(_, m: Message):
    await m.reply_text(
        "/inicio - Verificar si el bot está activo.\n/ayuda - Ver el menú de ayuda.\n/bin [consulta] - Verificar si un Bin es válido o inválido.\n/datos - Obtener datos de una URL."
    )

@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("¡Por favor, proporciona un Bin!\nEjemplo: /bin 401658")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("Procesando...")
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
                    nombre_banco = datos["bank"]["name"]
                    marca_tarjeta = datos["scheme"]
                    mencion_de = m.from_user.mention
                    caption = f"""
Nombre del banco: {nombre_banco}\nMarca de la tarjeta: {marca_tarjeta}\n\nVerificado por: {mencion_de}\nBot creado por: {mencion_de}\nCódigo fuente del bot: [GitHub](https://github.com/ImDenuwan/Bin-Checker-Bot)
"""
                    await mafia.edit_text(caption, disable_web_page_preview=True)  # Changed to edit_text
                except KeyError as e:
                    await mafia.edit_text(f"Error: {e}\n\nRespuesta: {respuesta.text}")  # Changed to edit_text
            else:
                await mafia.edit_text("Bin inválido o se produjo un error.")  # Changed to edit_text
            
        except Exception as e:
            await m.reply_text(f"¡Ups! Se produjo un error:\n{e}\n\nPor favor, informa este error al propietario del bot.")

@Bot.on_message(filters.command("datos"))  # Nuevo comando para obtener datos
async def obtener_datos(_, m: Message):
    try:
        url = "https://api.apilayer.com/bincheck/{codigo_bin}"
        datos_payload = {}
        cabeceras = {
            "apikey": "G6wqRUaOVzlvwlvavzHeefh2j1exTjse"
        }
        
        respuesta = requests.get(url, headers=cabeceras, data=datos_payload)
        
        codigo_estado = respuesta.status_code
        resultado = respuesta.text
        
        if codigo_estado == 200:
            await m.reply_text(f"Código de estado: {codigo_estado}\n\nResultado:\n{resultado}")
        else:
            await m.reply_text(f"No se pudo obtener los datos. Código de estado: {codigo_estado}")
            
    except Exception as e:
        await m.reply_text(f"Se produjo un error:\n{e}")

print("¡El bot está en línea!")

Bot.run()
