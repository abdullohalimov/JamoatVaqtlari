from datetime import datetime
import logging
from traceback import print_exc
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from tgbot.services import api
from tgbot.keyboards import factory, inline, reply
from tgbot.keyboards.factory import _
from tgbot.misc.states import UserStates
import pytz
user_router = Router()
lang_decode = {"uz": "name_uz", "de": "name_cyrl", "ru": "name_ru"}

viloyatlar = {
    "uz": {
        "1": "Toshkent shahri",
        "2": "Andijon",
        "3": "Buxoro",
        "4": "Fargʻona",
        "5": "Jizzax",
        "6": "Namangan",
        "7": "Navoiy",
        "8": "Qashqadaryo",
        "9": "Qoraqalpogʻiston",
        "10": "Samarqand",
        "11": "Sirdaryo",
        "12": "Surxondaryo",
        "13": "Toshkent viloyati",
        "14": "Xorazm",
        "99": "Boshqa",
    },
    "de": {
        "1": "Тошкент шаҳри",
        "2": "Андижон",
        "3": "Бухоро",
        "4": "Фарғона",
        "5": "Жиззах",
        "6": "Наманган",
        "7": "Навоий",
        "8": "Қашқадарё",
        "9": "Қорақалпоғистон",
        "10": "Самарқанд",
        "11": "Сирдарё",
        "12": "Сурхондарё",
        "13": "Тошкент вилояти",
        "14": "Хоразм",
        "99": "Бошқа",
    },
    "ru": {},
}

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

weekdays = {
    "uz": {
        0: "Dushanba",
        1: "Seshanba",
        2: "Chorshanba",
        3: "Payshanba",
        4: "Juma",
        5: "Shanba",
        6: "Yakshanba",   
    },
    "de": {
        0: "Душанба",
        1: "Сешанба",
        2: "Чоршанба",
        3: "Пайшанба",
        4: "Жума",
        5: "Шанба",
        6: "Якшанба",
    }
}

pages = {
    1: [1, 2, 3, 4, 5],
    2: [6, 7, 8, 9, 10],
    3: [11, 12, 13, 14, 15],
    4: [16, 17, 18, 19, 20],
    5: [21, 22, 23, 24, 25],
    6: [26, 27, 28, 29, 30],
    7: [31],
}


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(UserStates.menu)
    if data.get("registered", False):
        await message.answer(
            _("🏡 Bosh menyu", locale=data["locale"]),
            reply_markup=reply.main_menu_user(data["locale"]),
        )

    else:
        await message.answer(
            "Assalomu alaykum.\n✅ Yozuvni tanlang:",
            reply_markup=inline.language_keyboard(),
        )
        user = await api.update_or_create_user(
            user_id=message.chat.id, full_name=message.from_user.full_name
        )


@user_router.callback_query(factory.LanguageData.filter())
async def set_language(
    callback_query: CallbackQuery,
    callback_data: factory.LanguageData,
    state: FSMContext,
):
    language_to_locale = {"uz": "uz", "de": "de", "ru": "ru"}
    locale = language_to_locale.get(callback_data.language, "uz")
    await state.update_data(locale=locale, registered=True)
    data = await state.get_data()

    await callback_query.message.answer(
        _("🏡 Bosh menyu", locale=data["locale"]),
        reply_markup=reply.main_menu_user(data["locale"]),
    )
    await state.set_state(UserStates.menu)
    await callback_query.message.delete()

    user = await api.update_or_create_user(
        user_id=callback_query.message.chat.id,
        full_name=callback_query.from_user.full_name,
        lang=callback_data.language,
    )


@user_router.message(
    F.text.in_(["🕌 Jamoat vaqtlari", "🕌 Жамоат вақтлари"]), UserStates.menu
)
async def jamoat(message: Message, state: FSMContext):
    await state.update_data(masjid_action="subscription")
    data = await state.get_data()
    regions = await api.get_regions()
    t = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        _("🏙 Hududni tanlang:", locale=data["locale"]),
        reply_markup=inline.regions_keyboard(regions, data["locale"]),
    )
    await t.delete()


@user_router.callback_query(factory.RegionData.filter())
async def get_districts(
    callback_query: CallbackQuery, callback_data: factory.RegionData, state: FSMContext
):
    data = await state.get_data()
    districts = await api.get_districts(callback_data.region)
    logging.warning(districts)
    await callback_query.message.edit_text(
        _("🏘 Tumanni tanlang:", locale=data["locale"]),
        reply_markup=inline.districts_keyboard(districts, data["locale"]),
    )


@user_router.callback_query(factory.DistrictData.filter())
async def get_masjids(
    callback_query: CallbackQuery,
    callback_data: factory.DistrictData,
    state: FSMContext,
):
    await state.update_data(current_page=1, current_district=callback_data.ditrict)
    await state.set_state(UserStates.select_masjid)
    data = await state.get_data()
    masjidlar = await api.get_masjidlar(callback_data.ditrict)
    has_next = True if (1 * 5) < masjidlar["count"] else False

    logging.warning(masjidlar)
    await callback_query.message.edit_text(
        _("🕌 Masjidni tanlang:", locale=data['locale']),
        reply_markup=inline.masjidlar_keyboard(
            masjidlar["items"], lang=data["locale"], current_page=1, has_next=has_next
        ),
    )


@user_router.callback_query(factory.PagesData.filter(), UserStates.select_masjid)
async def get_masjids(
    callback_query: CallbackQuery, callback_data: factory.PagesData, state: FSMContext
):
    data = await state.get_data()

    if callback_data.action == "next":
        page = int(data["current_page"]) + 1
        masjidlar = await api.get_masjidlar(data["current_district"], page=page)
        has_next = True if ((page) * 5) < masjidlar["count"] else False
        await callback_query.message.edit_text(
        _("🕌 Masjidni tanlang:", locale=data['locale']),
            reply_markup=inline.masjidlar_keyboard(
                masjidlar["items"],
                lang=data["locale"],
                current_page=page,
                has_next=has_next,
            ),
        )

        await state.update_data(current_page=page)

    elif callback_data.action == "prev" and int(data["current_page"]) > 1:
        page = int(data["current_page"]) - 1
        masjidlar = await api.get_masjidlar(data["current_district"], page=page)

        has_next = True if ((page) * 5) < masjidlar["count"] else False

        await callback_query.message.edit_text(
        _("🕌 Masjidni tanlang:", locale=data['locale']),
            reply_markup=inline.masjidlar_keyboard(
                masjidlar["items"], lang=data["locale"], current_page=page
            ),
        )

        await state.update_data(current_page=page)

    await callback_query.answer()


@user_router.callback_query(factory.MasjidData.filter(), UserStates.select_masjid)
async def masjid_info(
    callback_query: CallbackQuery, callback_data: factory.MasjidData, state: FSMContext
):
    await state.update_data(current_masjid=callback_data.masjid, current_page=1)
    data = await state.get_data()
    if data.get("masjid_action", False) == "statistic":
        resp = await api.get_statistics(
            masjid_id=callback_data.masjid,
        )
        if resp["success"]:
            await callback_query.message.edit_text(
                _(
                    """
🕌 <b>{masjid} statistikasi</b>

Obunachilar soni: {subs_count} ta
{district} boʻyicha: {district_count}-oʻrin
{region} boʻyicha: {region_count}-oʻrin
Oʻzbekiston boʻyicha: {global_count}-oʻrin
""",
                    locale=data["locale"],
                ).format(
                    masjid=resp[lang_decode[data["locale"]]],
                    district=resp["district"][lang_decode[data["locale"]]],
                    district_count=resp["statistic"]["district_position"],
                    region=resp["district"]["region"][lang_decode[data["locale"]]],
                    region_count=resp["statistic"]["region_position"],
                    global_count=resp["statistic"]["all_position"],
                    subs_count=resp["subscription_count"],
                ),
                reply_markup=inline.main_menu_inline(data["locale"]),
            )
        else:
            await callback_query.message.edit_text(
                _("Ma'lumotlar topilmadi", locale=data["locale"]),
                reply_markup=inline.main_menu_inline(data["locale"]),
            )
    elif data.get("masjid_action", False) == "subscription":
        masjid = await api.masjid_info(callback_data.masjid)
        logging.warning(masjid)
        masjid_date = datetime.strptime(masjid["last_update"], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Specify the UTC timezone
        utc_timezone = pytz.utc

        # Convert the datetime to the UTC timezone
        formatted_datetime_utc = utc_timezone.localize(masjid_date)

        # Specify the target timezone ("Asia/Tashkent")
        target_timezone = pytz.timezone("Asia/Tashkent")

        # Convert the datetime to the target timezone
        masjid_date_tashkent = formatted_datetime_utc.astimezone(target_timezone)

        day = masjid_date_tashkent.day
        month = months[data['locale']][masjid_date_tashkent.month].lower()
        sana = f"""{day}{'-' if data['locale'] == 'uz' else ' '}{month} {masjid_date_tashkent.strftime("%H:%M")}"""   
        text = _(
            """
🕌 <b>{masjid} jamoat namozi vaqtlari</b>
📍 <b>Manzili:</b> {manzili1}, {manzili2}

🕒 <i>Oxirgi marta {sana} da yangilangan</i>

🏞 Bomdod: <b>{bomdod}</b>
🌇 Peshin: <b>{peshin}</b>
🌆 Asr: <b>{asr}</b>
🌃 Shom: <b>{shom}</b>
🌌 Xufton: <b>{hufton}</b>

@jamoatvaqtlaribot""",
            locale=data["locale"],
        ).format(
            sana=sana,
            masjid=masjid[lang_decode[data["locale"]]],
            manzili1=masjid["district"]["region"][lang_decode[data["locale"]]],
            manzili2=masjid["district"][lang_decode[data["locale"]]],
            bomdod=masjid["bomdod"],
            peshin=masjid["peshin"],
            asr=masjid["asr"],
            shom=masjid["shom"],
            hufton=masjid["hufton"],
        )

        markup = inline.masjid_kb(masjid, lang=data["locale"])
        if str(masjid.get("photo", False)) != "None":
            try:
                # raise Exception
                await callback_query.message.answer_photo(
                    photo=masjid["photo"], caption=text, reply_markup=markup
                )
            except:
                print_exc()
                try:
                    await callback_query.message.answer_photo(
                        photo=api.global_url + masjid["photo_file"],
                        caption=text,
                        reply_markup=markup,
                    )
                except:
                    print_exc()
                    await callback_query.message.edit_text(
                        text=text, reply_markup=markup
                    )
        else:
            await callback_query.message.edit_text(text=text, reply_markup=markup)


@user_router.callback_query(factory.MasjidLocationData.filter())
async def masjid_location(
    callback_query: CallbackQuery,
    callback_data: factory.MasjidLocationData,
    state: FSMContext,
):
    await callback_query.message.answer_location(
        latitude=float(callback_data.lt), longitude=float(callback_data.ln)
    )


@user_router.callback_query(factory.MasjidInfoData.filter())
async def masjid_info(
    callback_query: CallbackQuery,
    callback_data: factory.MasjidInfoData,
    state: FSMContext,
):
    logging.warning(callback_data)
    data = await state.get_data()

    if callback_data.action == "main":
        await user_start(callback_query.message, state)
        await callback_query.message.delete()
        return
    resp = await api.masjid_subscription(
        user_id=callback_query.message.chat.id,
        masjid_id=callback_data.masjid,
        action=callback_data.action,
    )
    if resp["success"]:
        logging.warning(resp)
        masjid = resp["masjid"]
        if callback_data.action == "subscribe":
            await callback_query.message.edit_text(
                _(
                    "✅ {district} {masjid} masjidi jamoat vaqtlariga obuna boʻldingiz",
                    locale=data["locale"],
                ).format(
                    district=masjid["district"][lang_decode[data["locale"]]],
                    masjid=masjid[lang_decode[data["locale"]]],
                )
            )
            await state.set_state(UserStates.menu)
        elif callback_data.action == "unsubscribe":
            await callback_query.message.edit_text(
                _(
                    "☑️ {district} {masjid} masjidi jamoat vaqtlariga obuna bekor qilindi",
                    locale=data["locale"],
                ).format(
                    district=masjid["district"][lang_decode[data["locale"]]],
                    masjid=masjid[lang_decode[data["locale"]]],
                ),
            )
            await state.set_state(UserStates.menu)

        await callback_query.message.answer(
            _("🏡 Bosh menyu", locale=data["locale"]),
            reply_markup=reply.main_menu_user(data["locale"]),
        )
    else:
        await callback_query.answer(text="Xatolik yuz berdi")


@user_router.message(F.text.in_(["✅ Obunalar", "✅ Обуналар"]))
async def masjid_info(message: Message, state: FSMContext):
    data = await state.get_data()
    subs = await api.get_subscriptions(message.chat.id)
    logging.warning(subs)
    await message.answer(_("✅ Obunalar:", locale=data["locale"]))
    text = ""
    for masjid in subs:
        text += f"🕌 {masjid['masjid'][lang_decode[data['locale']]]}\n"
        text += f"📍 {masjid['masjid']['district']['region'][lang_decode[data['locale']]]}, {masjid['masjid']['district'][lang_decode[data['locale']]]}\n"
        text += f"🕓 {masjid['masjid']['bomdod']} | {masjid['masjid']['peshin']} | {masjid['masjid']['asr']} | {masjid['masjid']['shom']} | {masjid['masjid']['hufton']} \n\n"
    await message.answer(text)


@user_router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]), UserStates.menu)
async def statistika(message: Message, state: FSMContext):
    data = await state.get_data()
    subs = await api.get_subscriptions_statistics(message.chat.id)
    logging.warning(subs)
    await message.answer(_("📊 Statistika", locale=data["locale"]))
    text = ""
    for masjid in subs:
        text += _(
            """
🕌 <b>{masjid} statistikasi</b>

Obunachilar soni: {subs_count} ta
{district} boʻyicha: {district_count}-oʻrin
{region} boʻyicha: {region_count}-oʻrin
Oʻzbekiston boʻyicha: {global_count}-oʻrin
""",
            locale=data["locale"],
        ).format(
            subs_count=masjid["masjid"]["subscription_count"],
            masjid=masjid["masjid"][lang_decode[data["locale"]]],
            district=masjid["masjid"]["district"][lang_decode[data["locale"]]],
            district_count=masjid["masjid"]["statistic"]["district_position"],
            region=masjid["masjid"]["district"]["region"][lang_decode[data["locale"]]],
            region_count=masjid["masjid"]["statistic"]["region_position"],
            global_count=masjid["masjid"]["statistic"]["all_position"],
        )

    await message.answer(text, reply_markup=inline.other_masjids_inline(data["locale"]))


@user_router.callback_query(factory.OtherMasjidsFactory.filter())
async def other_masjids(
    callback_query: CallbackQuery,
    callback_data: factory.OtherMasjidsFactory,
    state: FSMContext,
):
    await state.update_data(masjid_action="statistic")

    data = await state.get_data()
    regions = await api.get_regions()
    message = callback_query.message
    t = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await message.edit_text(
        _("🏙 Hududni tanlang:", locale=data["locale"]),
        reply_markup=inline.regions_keyboard(regions, data["locale"]),
    )
    await t.delete()


@user_router.message(F.text.in_(["🇺🇿 Yozuvni oʻzgartirish", "🇺🇿 Ёзувни ўзгартириш"]))
async def change_lang(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        _("✅ Yozuvni tanlang:", locale=data["locale"]),
        reply_markup=inline.language_keyboard(),
    )


@user_router.message(F.text.in_(["🕰 Namoz vaqtlari", "🕰 Намоз вақтлари"]))
async def namoz_vaqti(message: Message, state: FSMContext):
    data = await state.get_data()
    mintaqa = data.get("mintaqa", 27)
    currint_time = datetime.now()
    bugungi_namoz_vaqti = await api.get_today_namoz_vaqti(
        mintaqa=mintaqa, milodiy_oy=currint_time.month, milodiy_kun=currint_time.day
    )
    logging.warning(bugungi_namoz_vaqti)
    vaqtlar = bugungi_namoz_vaqti["vaqtlari"].split("|")
    text = _(
        """
<b>Namoz vaqtlari
Hudud: {hudud}
{sana}</b>

<i>🏙 Tong: <b>{tong}</b> (saharlik tugashi) 
🌅 Quyosh: <b>{quyosh}</b>
🏞 Peshin: <b>{peshin}</b>
🌇 Asr: <b>{asr}</b>
🌆 Shom: <b>{shom}</b> (iftorlik boshlanishi)
🌌 Xufton: <b>{xufton}</b></i>

@jamoatvaqtlaribot
""",
        locale=data["locale"],
    ).format(
        sana=datetime.now().strftime("%d.%m.%Y"),
        hudud=bugungi_namoz_vaqti["mintaqa"][lang_decode[data["locale"]]],
        tong=vaqtlar[0].strip(),
        quyosh=vaqtlar[1].strip(),
        peshin=vaqtlar[2].strip(),
        asr=vaqtlar[3].strip(),
        shom=vaqtlar[4].strip(),
        xufton=vaqtlar[5].strip(),
    )
    t = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text,
        reply_markup=inline.namoz_vaqtlari_inline(
            mintaqa=bugungi_namoz_vaqti["mintaqa"], lang=data["locale"]
        ),
    )
    await t.delete()


@user_router.callback_query(factory.NamozVaqtlariData.filter())
async def namoz_vaqti_callback(
    callback_query: CallbackQuery,
    callback_data: factory.NamozVaqtlariData,
    state: FSMContext,
):
    current_time = datetime.now()
    data = await state.get_data()
    if callback_data.action == "oylik":
        logging.warning(callback_data)
        current_time = datetime.now()
        page = 1
        await state.set_state(UserStates.select_namoz_vaqti)
        for key, value in pages.items():
            if current_time.day in value:
                page = key

        oylik = await api.get_namoz_vaqtlari(
            mintaqa=callback_data.mintaqa, milodiy_oy=current_time.month, page=page
        )
        has_next = True if ((page) * 5) < oylik["count"] else False
        mintaqatext = ""
        dates = []
        for kun in oylik["items"]:
            mintaqatext = kun['mintaqa'][lang_decode[data['locale']]]
            vaqtlar = kun["vaqtlari"].split("|")
            day = kun['milodiy_kun']
            month = months[data['locale']][kun['milodiy_oy']].lower()
            weekday = weekdays[data['locale']][datetime.strptime(f"{current_time.year}-{kun['milodiy_oy']}-{kun['milodiy_kun']}", '%Y-%m-%d').weekday()].lower()
            sana = f"""{day}{'-' if data['locale'] == 'uz' else ' '}{month}, {weekday}"""   
            text = _(
                """📅 <i><b>{sana}</b>
🕒 {tong} | {quyosh} | {peshin} | {asr} | {shom} | {xufton}</i>\n
""",
                locale=data["locale"],
            ).format(
                sana=sana,
                tong=vaqtlar[0].strip(),
                quyosh=vaqtlar[1].strip(),
                peshin=vaqtlar[2].strip(),
                asr=vaqtlar[3].strip(),
                shom=vaqtlar[4].strip(),
                xufton=vaqtlar[5].strip(),
            )
            dates.append(text)

        await callback_query.message.edit_text(
            _(
                """<b>{year}-yil {month} oyi namoz vaqtlari
Hudud: {mintaqa}</b>

Tong | Quyosh | Peshin | Asr | Shom | Xufton\n\n""",
                locale=data["locale"],
            ).format(year=current_time.year, mintaqa=mintaqatext, month=months[data["locale"]][current_time.month].lower())
            + "".join(dates) + "@jamoatvaqtlaribot",
            reply_markup=inline.oylik_namoz_vaqtlari_inline(
                mintaqa=callback_data.mintaqa,
                current_page=page,
                has_next=has_next,
                lang=data["locale"],
            ),
        )
        await state.update_data(
            current_page=page, current_mintaqa=callback_data.mintaqa
        )

    if callback_data.action == "downl":
        await callback_query.message.answer_document(
            f"https://islom.uz/prayertime/pdf/{callback_data.mintaqa}/{current_time.month}"
        )

    if callback_data.action == "changemintaqa":
        await callback_query.message.edit_text(
            _("Hududni oʻzgartirish:", locale=data["locale"]),
            reply_markup=inline.mintaqa_viloyat_inline(
                viloyatlar[data["locale"]], data["locale"]
            ),
        )


@user_router.callback_query(factory.PagesData.filter(), UserStates.select_namoz_vaqti)
async def pages_namoz_vaqtlari(
    callback_query: CallbackQuery, callback_data: factory.PagesData, state: FSMContext
):
    data = await state.get_data()
    current_time = datetime.now()

    if callback_data.action == "next":
        page = int(data["current_page"]) + 1
        oylik = await api.get_namoz_vaqtlari(
            mintaqa=data["current_mintaqa"], milodiy_oy=current_time.month, page=page
        )
        has_next = True if ((page) * 5) < oylik["count"] else False
        mintaqatext = ""
        dates = []
        for kun in oylik["items"]:
            mintaqatext = kun["mintaqa"][lang_decode[data["locale"]]]
            vaqtlar = kun["vaqtlari"].split("|")
            day = kun['milodiy_kun']
            month = months[data['locale']][kun['milodiy_oy']].lower()
            weekday = weekdays[data['locale']][datetime.strptime(f"{current_time.year}-{kun['milodiy_oy']}-{kun['milodiy_kun']}", '%Y-%m-%d').weekday()].lower()
            sana = f"""{day}{'-' if data['locale'] == 'uz' else ' '}{month}, {weekday}"""              
            text = _(
                """📅 <i><b>{sana}</b>
🕒 {tong} | {quyosh} | {peshin} | {asr} | {shom} | {xufton}</i>\n
""",
                locale=data["locale"],
            ).format(
                sana=sana,
                tong=vaqtlar[0].strip(),
                quyosh=vaqtlar[1].strip(),
                peshin=vaqtlar[2].strip(),
                asr=vaqtlar[3].strip(),
                shom=vaqtlar[4].strip(),
                xufton=vaqtlar[5].strip(),
            )
            dates.append(text)

        await callback_query.message.edit_text(
            _(
                """<b>{year}-yil {month} oyi namoz vaqtlari
Hudud: {mintaqa}</b>

Tong | Quyosh | Peshin | Asr | Shom | Xufton\n\n""",
                locale=data["locale"],
            ).format(year=current_time.year, mintaqa=mintaqatext, month=months[data["locale"]][current_time.month].lower())
            + "".join(dates) + "@jamoatvaqtlaribot",
            reply_markup=inline.oylik_namoz_vaqtlari_inline(
                mintaqa=data["current_mintaqa"],
                current_page=page,
                has_next=has_next,
                lang=data["locale"],
            ),
        )

        await state.update_data(current_page=page)

    elif callback_data.action == "prev" and int(data["current_page"]) > 1:
        page = int(data["current_page"]) - 1
        oylik = await api.get_namoz_vaqtlari(
            mintaqa=data["current_mintaqa"], milodiy_oy=current_time.month, page=page
        )
        has_next = True if ((page) * 5) < oylik["count"] else False
        mintaqatext = ""
        dates = []
        for kun in oylik["items"]:
            mintaqatext = kun["mintaqa"][lang_decode[data["locale"]]]
            vaqtlar = kun["vaqtlari"].split("|")
            day = kun['milodiy_kun']
            month = months[data['locale']][kun['milodiy_oy']].lower()
            weekday = weekdays[data['locale']][datetime.strptime(f"{current_time.year}-{kun['milodiy_oy']}-{kun['milodiy_kun']}", '%Y-%m-%d').weekday()].lower()
            sana = f"""{day}{'-' if data['locale'] == 'uz' else ' '}{month}, {weekday}"""            
            text = _(
                """📅 <i><b>{sana}</b>
🕒 {tong} | {quyosh} | {peshin} | {asr} | {shom} | {xufton}</i>\n
""",
                locale=data["locale"],
            ).format(
                sana=sana,
                tong=vaqtlar[0].strip(),
                quyosh=vaqtlar[1].strip(),
                peshin=vaqtlar[2].strip(),
                asr=vaqtlar[3].strip(),
                shom=vaqtlar[4].strip(),
                xufton=vaqtlar[5].strip(),
            )
            dates.append(text)

        await callback_query.message.edit_text(
            _(
                """<b>{year}-yil {month} oyi namoz vaqtlari
Hudud: {mintaqa}</b>

Tong | Quyosh | Peshin | Asr | Shom | Xufton\n\n""",
                locale=data["locale"],
            ).format(year=current_time.year, mintaqa=mintaqatext, month=months[data["locale"]][current_time.month].lower())
            + "".join(dates) + "@jamoatvaqtlaribot",
            reply_markup=inline.oylik_namoz_vaqtlari_inline(
                mintaqa=data["current_mintaqa"],
                current_page=page,
                has_next=has_next,
                lang=data["locale"],
            ),
        )

        await state.update_data(current_page=page)

    await callback_query.answer()


@user_router.callback_query(factory.MintaqaViloyatData.filter())
async def mintaqa_viloyat(
    callback_query: CallbackQuery,
    callback_data: factory.MintaqaViloyatData,
    state: FSMContext,
):
    pass
    data = await state.get_data()

    mintaqalar = await api.get_viloyat_mintaqalari(viloyat_id=callback_data.viloyat_id)
    await callback_query.message.edit_text(
        _("Hududni oʻzgartirish:", locale=data["locale"]),
        reply_markup=inline.mintaqa_inline(mintaqalar, data["locale"]),
    )


@user_router.callback_query(factory.MintaqaData.filter())
async def mintaqa(
    callback_query: CallbackQuery, callback_data: factory.MintaqaData, state: FSMContext
):
    await callback_query.message.delete()
    await state.update_data(mintaqa=callback_data.mintaqa_id)
    await namoz_vaqti(callback_query.message, state)
    # await state.set_state(UserStates.menu)
    # await callback_query.message.answer(
    #         _("🏡 Bosh menyu", locale=data["locale"]),
    #         reply_markup=reply.main_menu_user(data["locale"]),
    #     )
