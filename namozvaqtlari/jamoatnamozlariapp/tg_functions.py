from datetime import datetime
import logging
import os
from telebot import TeleBot
from telebot.types import InputFile
from UzTransliterator import UzTransliterator
# from .models import Masjid

bot = TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


text_uz = ""
text_cyrl = ""

months = {
    "uz": {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentyabr",
        10: "Oktyabr",
        11: "Noyabr",
        12: "Dekabr",
    },
    "de": {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь",
    },
}

def send_text(text):

    bot.send_message(chat_id=-1002111788540, text=text)

def send_backup(backup):
    try:
        bot.send_document(chat_id=-1002111788540, document=InputFile(backup), caption="#jamoatvaqtlari DB File | " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    except:
        bot.send_message(chat_id=1357813137, text="Error sending backup file | JamoatVaqtlariBot | " + datetime.now().strftime("%Y-%m-%d %H:%M"))

def get_photo_id(photo_file):

    ph = bot.send_photo(chat_id=-1002099528963, photo=photo_file)
    bot.reply_to(ph, "Rasm IDsi: " + ph.photo[-1].file_id)

    return ph.photo[-1].file_id

def send_new_masjid_times(masjid, subscriptions):
    obj = UzTransliterator.UzTransliterator()
    old, new = masjid
    current_time = datetime.now()

    sendtext = f"""
 {new.district.region.name_uz}|||{new.district.name_uz} {new.name_uz} jamoat vaqtlari oʻzgardi.

 🕒 {current_time.day} {months['uz'][current_time.month].lower()}, {current_time.strftime("%H:%M")}

🏞 Bomdod: {new.bomdod}
🌇 Peshin: {new.peshin}
🌆 Asr: {new.asr}
🌃 Shom: {new.shom}
🌌 Xufton: {new.hufton}"""

    for sub in subscriptions:
        text = sendtext
        try:
            if sub.user.lang == "de":
                bot.send_message(chat_id=sub.user.user_id, text=obj.transliterate(text, from_="lat", to="cyr").replace("|||", " ") + "\n\n@jamoatvaqtlaribot")
            elif sub.user.lang == "uz":
                bot.send_message(chat_id=sub.user.user_id, text=text.replace("|||", "-") + "\n\n@jamoatvaqtlaribot")
        except:
            pass
    
def send_region_change_times(users, region, type):
    region_text = f"{region.district.region.name_uz} {region.district.name_uz}" if type == "district" else region.region.name_uz
    obj = UzTransliterator.UzTransliterator()
    current_time = datetime.now()
    sendtext = f"""
 🕌 {region_text} masjidlari jamoat vaqtlari oʻzgardi.

🕒 {current_time.day}|||{months['uz'][current_time.month].lower()}, {current_time.strftime("%H:%M")}

🏞 Bomdod: {region.bomdod}
🌇 Peshin: {region.peshin}
🌆 Asr: {region.asr}
🌃 Shom: {region.shom}
🌌 Xufton: {region.xufton}"""
    
    for sub in users:
        text = sendtext

        try:
            if sub.user.lang == "de":
                bot.send_message(chat_id=sub.user.user_id, text=obj.transliterate(text, from_="lat", to="cyr").replace("|||", " ") + "\n\n@jamoatvaqtlaribot")
            elif sub.user.lang == "uz":
                bot.send_message(chat_id=sub.user.user_id, text=text.replace("|||", "-") + "\n\n@jamoatvaqtlaribot")

        except:
            pass