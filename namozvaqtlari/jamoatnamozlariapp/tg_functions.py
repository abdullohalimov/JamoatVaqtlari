import logging
from telebot import TeleBot

# from .models import Masjid

bot = TeleBot("6392713399:AAEzbhQZo42QusOW7hlVUhI-jS06gJhYpdY", parse_mode="HTML")


text_uz = ""
text_cyrl = ""


def get_photo_id(photo_file):

    ph = bot.send_photo(chat_id=-1002099528963, photo=photo_file)
    bot.reply_to(ph, "Rasm IDsi: " + ph.photo[-1].file_id)

    logging.warning(ph)

    return ph.photo[-1].file_id

def send_new_masjid_times(masjid, subscriptions):
    old, new = masjid
    text = f"""
 {new.district.region.name_uz}, {new.district.name_uz}, {new.name_uz} jamoat vaqtlari oʻzgardi.

🏞 Bomdod: {new.bomdod}
🌇 Peshin: {new.peshin}
🌆 Asr: {new.asr}
🌃 Shom: {new.shom}
🌌 Xufton: {new.hufton}
"""

    for sub in subscriptions:

        bot.send_message(chat_id=sub.user.user_id, text=text)
    
def send_region_change_times(users, region, type):
    region = f"{region.district.region.name_uz}, {region.district.name_uz}" if type == "district" else region.region.name_uz

    text = f"""
 {region} jamoat vaqtlari oʻzgardi.

🏞 Bomdod: {region.bomdod}
🌇 Peshin: {region.peshin}
🌆 Asr: {region.asr}
🌃 Shom: {region.shom}
🌌 Xufton: {region.hufton}
"""
    
    for sub in users:
        bot.send_message(chat_id=sub.user.user_id, text=text)