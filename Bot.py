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

def luhn_algorithm(card_number):
    card_number = card_number.replace(" ", "")  # Elimina los espacios en blanco
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
                print(datos)  # Agregamos esta línea para imprimir la respuesta JSON completa
                try:
                    nombre_banco = datos.get("bank_name", "No disponible")
                    marca_tarjeta = datos.get("scheme", "No disponible")
                    pais = datos.get("country", "No disponible")
                    tipo = datos.get("type", "No disponible")
                    bin_numero = datos.get("bin", "No disponible")
                    mencion_de = m.from_user.mention
                    caption = f"""
Nombre del banco: {nombre_banco}
Marca de la tarjeta: {marca_tarjeta}
País: {pais}
Tipo: {tipo}
Número Bin: {bin_numero}

Verificado por: {mencion_de}
Bot creado por: {mencion_de}
Código fuente del bot: [GitHub](https://github.com/ImDenuwan/Bin-Checker-Bot)
"""
                    await mafia.edit_text(caption, disable_web_page_preview=True)
                except KeyError as e:
                    await mafia.edit_text(f"Error: {e}\n\nRespuesta: {respuesta.text}")
            else:
                await mafia.edit_text("Bin inválido o se produjo un error.")
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
