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
                InlineKeyboardButton("🔒 Generar Contraseña Segura", callback_data="generate_password"),
                InlineKeyboardButton("💳 Verificar Bin", callback_data="verify_bin"),
            ],
            [
                InlineKeyboardButton("🏆 Pasar A Premium", url="https://t.me/NtEasyMoney")
            ],
        ]
    )

    mensaje = (
        f"👋 ¡Hola, {mencion_usuario}!\n\n"
        "¡Bienvenido a NtEasyBot! 🤖💼\n\n"
        "🔍 Explora nuestras funciones:\n\n"
        "1. Verifica si un Bin es válido o inválido utilizando /bin [número].\n"
        "2. Genera contraseñas seguras con /Scr [longitud].\n\n"
        "🌟 ¡Disfruta de una experiencia Premium para acceder a funciones exclusivas!\n\n"
        "¿Necesitas ayuda? Usa /ayuda."
    )

    await m.reply_text(mensaje, reply_markup=teclado)


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
                    mensaje += "[Admin 🏆](https://t.me/NtEasyMoney) 👈 Haste Premium"

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
        msg = await m.reply_text("💳 Por favor, proporciona una tarjeta de crédito.\nEjemplo: /cck 403121xxxxxxxxxx xx xx xxx")
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

class GetGenerate:
    def __init__(self, count=1, credit_type="Visa"):
        self.count = count
        self.credit_type = credit_type
        self.jdata = {"amex": ['34', '37'], "discover": ['65', '6011'],
                      "mastercard": ['51', '52', '53', '54', '55'], "visa": ['4']}
        self.info_card = {}
        self.ready_card = {}
        self.beautiful_card = None

    def cardInfo(self, card_list):
        for card_number in card_list:
            self.info_card.update({card_number: CardValidator(card_number).cardInfo()})

        return self.info_card

    def beautifulCard(self, card_list):
        if type([]) == type(card_list):
            self.beautiful_card = []
            for card_ids in card_list:
                out = []
                template_base = ""
                card_ids = str(card_ids)
                while card_ids:
                    out.append(card_ids[-4:])
                    card_ids = card_ids[:-4]
                    template_base = ' '.join(out[::-1])
                self.beautiful_card.append(template_base)
        elif type({}) == type(card_list):
            self.beautiful_card = {}
            for idList in card_list:
                card_ids = card_list[idList]['card']
                out = []
                template_base = ""
                while card_ids:
                    out.append(card_ids[-4:])
                    card_ids = card_ids[:-4]
                    template_base = ' '.join(out[::-1])
                jValue = {idList: {"card": template_base,
                                   "data": card_list[idList]['data'],
                                   "csv": card_list[idList]['csv']}}
                self.beautiful_card.update(jValue)
        return self.beautiful_card

    def getCard(self, beautiful_card=None, bank_info=None):
        if self.credit_type.lower() == "visa":
            for x in range(self.count):
                card_id = random.choice(self.jdata['visa'])
                if random.randint(0, 1):
                    while 1:
                        card_number = f"{card_id}{random.randint(111111111111, 999999999999)}"
                        if CardValidator(card_number).luhnValidator():
                            data_value = int(datetime.now().strftime("%y")) + random.randint(2, 6)
                            json_value = {x: {"card": f"{card_number}",
                                              "data": f"0{random.randint(1, 10)}/{data_value}",
                                              "csv": random.randint(111, 999)}}
                            self.ready_card.update(json_value)
                            break
                else:
                    while 1:
                        card_number = f"{card_id}{random.randint(111111111111111, 999999999999999)}"
                        if CardValidator(card_number).luhnValidator():
                            data_value = int(datetime.now().strftime("%y")) + random.randint(2, 6)
                            json_value = {x: {"card": f"{card_number}",
                                              "data": f"0{random.randint(1, 10)}/{data_value}",
                                              "csv": random.randint(111, 999)}}
                            self.ready_card.update(json_value)
                            break

            if beautiful_card:
                self.beautiful_card = GetGenerate().beautifulCard(self.ready_card)
            if bank_info:
                jsonInfoBank = {}
                for card_id in self.ready_card:
                    ready_info = CardValidator(self.ready_card[card_id]['card']).cardInfo()
                    jsonInfoBank.update({card_id: {"value": self.ready_card[card_id], "info": ready_info}})
                self.ready_card = jsonInfoBank

            return self.ready_card

# Resto del código...

class CardValidator:
    def __init__(self, card_number):
        self.card_number = str(card_number)
        self.len_card = len(str(card_number))
        self.luhn_valid = None
        self.card_info = {}
        self.jdata = {'AMEX': ['34', '37'], 'Discover': ['65', '6011'],
                      'MasterCard': ['51', '52', '53', '54', '55'], 'Visa': ['4']}
        self.type_card = 'Unknown'

    def luhnValidator(self):
        double = 0
        total = 0

        digits = str(self.card_number)

        for i in range(len(digits) - 1, -1, -1):
            for c in str((double + 1) * int(digits[i])):
                total += int(c)
            double = (double + 1) % 2

        self.luhn_valid = (total % 10) == 0
        return self.luhn_valid

    def cardType(self):
        # AMEX
        if self.len_card == 15 and self.card_number[:2] in self.jdata['AMEX']:
            self.type_card = 'AMEX'

        # MasterCard, Visa, and Discover
        elif self.len_card == 16:
            # MasterCard
            if self.card_number[:2] in self.jdata['MasterCard']:
                self.type_card = 'MasterCard'

            # Discover
            elif self.card_number[:2] in self.jdata['Discover'] or self.card_number[:4] in self.jdata['Discover']:
                self.type_card = 'Discover'

            # Visa
            elif self.card_number[:1] in self.jdata['Visa']:
                self.type_card = 'Visa'

        # VISA
        elif self.len_card == 13 and self.card_number[:1] in self.jdata['Visa']:
            self.type_card = 'Visa'

        return self.type_card

    def cardInfo(self):
        req = requests.get(f"https://lookup.binlist.net/{self.card_number.replace(' ', '')[:6]}")
        if req.status_code == 200:
            j_req = req.json()
            try:
                self.card_info.update({"type": j_req['type']})
            except:
                ...
            self.card_info.update({
                "country": j_req['country']['name'],
                "currency": j_req['country']['currency'],
                "short": j_req['country']['alpha2'],
            })
            if j_req['bank']:
                for ids in ['name', 'phone', 'url']:
                    try:
                        self.card_info.update({
                            f"bank_{ids}": j_req['bank'][ids],
                        })
                    except:
                        ...
        else:
            return None

        return self.card_info

# Resto del código...

@Bot.on_message(filters.command("ccg"))
async def ccg(_, m: Message):
    try:
        count = 1  # Cambia este valor para generar más tarjetas si es necesario
        credit_type = "Visa"  # Puedes cambiar esto si deseas otro tipo de tarjeta
        generate_instance = GetGenerate(count, credit_type)

        card_info = generate_instance.cardInfo(generate_instance.ready_card)
        beautiful_card = generate_instance.beautifulCard(generate_instance.ready_card)

        mensaje = "🔢 **Información de la Tarjeta Generada** 🔢\n\n"
        mensaje += f"Datos de la tarjeta: {card_info}\n\n"
        mensaje += f"Tarjeta hermosa: {beautiful_card}\n\n"
        mensaje += f"Generado por: {m.from_user.mention} 👤"

        await m.reply_text(mensaje, parse_mode="markdown")
    except Exception as e:
        await m.reply_text(f"¡Ups! Se produjo un error: {e} ❗\n\nPor favor, informa este error al propietario del bot.")


print("🚀 ¡El bot está en línea! 🚀")

Bot.run()
