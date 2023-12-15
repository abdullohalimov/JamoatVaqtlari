from typing import Any
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.i18n import I18n



i18n = I18n(path="locales", default_locale="uz", domain="messages")

_ = i18n.gettext


class LanguageData(CallbackData, prefix="language"):
    language: Any

class RegionData(CallbackData, prefix="region"):
    region: Any

class DistrictData(CallbackData, prefix="district"):
    ditrict: Any
    region: Any

class MasjidData(CallbackData, prefix="masjid"):
    masjid: Any

class PagesData(CallbackData, prefix="page"):
    page: Any
    action: Any

class MasjidInfoData(CallbackData, prefix="masjidinfo"):
    masjid: Any
    action: Any

class MasjidLocationData(CallbackData, prefix="masjidloc"):
    ln: Any
    lt: Any