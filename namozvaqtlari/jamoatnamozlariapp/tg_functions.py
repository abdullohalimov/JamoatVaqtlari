from datetime import datetime
import logging
import os
from telebot import TeleBot
from telebot.types import InputFile

# from .models import Masjid

bot = TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


text_uz = ""
text_cyrl = ""

def send_text(text):

    bot.send_message(chat_id=-1002111788540, text=text)

def send_backup(backup):
    
    bot.send_document(chat_id=-1002111788540, document=InputFile(backup), caption="#jamoatvaqtlari DB File | " + datetime.now().strftime("%Y-%m-%d %H:%M"))

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
        try:
            bot.send_message(chat_id=sub.user.user_id, text=text)
        except:
            pass
    
def send_region_change_times(users, region, type):
    region_text = f"{region.district.region.name_uz}, {region.district.name_uz}" if type == "district" else region.region.name_uz

    text = f"""
 🕌 {region_text} masjidlari jamoat vaqtlari oʻzgardi.

🏞 Bomdod: {region.bomdod}
🌇 Peshin: {region.peshin}
🌆 Asr: {region.asr}
🌃 Shom: {region.shom}
🌌 Xufton: {region.xufton}
"""
    
    for sub in users:
        try:
            bot.send_message(chat_id=sub.user.user_id, text=text)
        except:
            pass