from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from tgbot.keyboards import factory


def language_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🇺🇿 Lotin", callback_data=factory.LanguageData(language="uz").pack()),
        InlineKeyboardButton(text="🇺🇿 Крилл", callback_data=factory.LanguageData(language="de").pack()),
        # InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
    )

    return keyboard.as_markup()

def regions_keyboard(regions_list: dict) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for key, value in regions_list.items():
        keyboard.row(
            InlineKeyboardButton(text=value, callback_data=factory.RegionData(region=key).pack())
        )

    keyboard.adjust(2)
    

    return keyboard.as_markup()