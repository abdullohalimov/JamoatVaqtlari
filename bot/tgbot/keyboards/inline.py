from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from tgbot.keyboards import factory
from tgbot.keyboards.factory import _

lang_decode = {"uz": "name_uz", "de": "name_cyrl", "ru": "name_ru"}


def language_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="🇺🇿 Lotin", callback_data=factory.LanguageData(language="uz").pack()
        ),
        InlineKeyboardButton(
            text="🇺🇿 Кирилл", callback_data=factory.LanguageData(language="de").pack()
        ),
        # InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
    )

    return keyboard.as_markup()


def regions_keyboard(regions_list, lang="uz") -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for region in regions_list:
        keyboard.row(
            InlineKeyboardButton(
                text=region[lang_decode[lang]],
                callback_data=factory.RegionData(region=region["pk"]).pack(),
            )
        )

    keyboard.adjust(2)

    return keyboard.as_markup()


def districts_keyboard(districts_list, lang="uz") -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for district in districts_list:
        keyboard.row(
            InlineKeyboardButton(
                text=district[lang_decode[lang]],
                callback_data=factory.DistrictData(
                    ditrict=district["pk"], region=district["region"]["pk"]
                ).pack(),
            )
        )

    keyboard.adjust(2)

    return keyboard.as_markup()


def masjidlar_keyboard(
    masjid_list, lang="uz", current_page=1, has_next=True
) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    for masjid in masjid_list:
        keyboard.row(
            InlineKeyboardButton(
                text=masjid[lang_decode[lang]],
                callback_data=factory.MasjidData(
                    masjid=masjid["pk"],
                ).pack(),
            )
        )

    keyboard.adjust(1)

    keyboard.row(
        InlineKeyboardButton(
            text=_("{icon} Orqaga".format(
                icon='⬅️' if current_page > 1 else '⏸'
            ), locale=lang),
            callback_data=factory.PagesData(page=current_page, action="prev").pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=f"{current_page}",
            callback_data=factory.PagesData(page=current_page, action="page").pack(),
        ),
        InlineKeyboardButton(
            text=_("{icon} Keyingi", locale=lang).format(
                icon='➡️' if has_next else '⏸'
            ),
            callback_data=factory.PagesData(
                page=current_page, action="next" if has_next else "stop"
            ).pack(),
        ),
    )

    return keyboard.as_markup()


def masjid_kb(masjid_info, lang="uz") -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=_("✅ Obuna bo'lish", locale=lang), callback_data=factory.MasjidInfoData(masjid=masjid_info['pk'], action="subscribe").pack()
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_("❌ Obunani bekor qilish", locale=lang), callback_data=factory.MasjidInfoData(masjid=masjid_info['pk'], action="unsubscribe").pack()
        )
    )
    if str(masjid_info['location']) != "None":
        try:
            lt, ln = masjid_info['location'].split(",")[:2]
            lt, ln = float(lt), float(ln)
            keyboard.row(
            InlineKeyboardButton(
                text=_("🗺 Xaritada ko'rish", locale=lang),  callback_data=factory.MasjidLocationData(ln=ln, lt=lt).pack()
            )
        )
        except:
            pass
    keyboard.row(
        InlineKeyboardButton(
            text=_("🏡 Bosh menyu", locale=lang), callback_data=factory.MasjidInfoData(masjid=masjid_info['pk'], action="main").pack()
        )
    )

    return keyboard.as_markup()


