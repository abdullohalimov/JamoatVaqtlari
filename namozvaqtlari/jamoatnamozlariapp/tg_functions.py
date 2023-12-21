import logging
from telebot import TeleBot

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
    # bot.send_message(chat_id=-1002099528963, text=message)
    pass