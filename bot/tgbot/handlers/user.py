from datetime import datetime
import logging
from traceback import print_exc
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from tgbot.services import api
from tgbot.keyboards import factory, inline, reply
from tgbot.keyboards.factory import _
from tgbot.misc.states import UserStates

user_router = Router()
lang_decode = {"uz": "name_uz", "de": "name_cyrl", "ru": "name_ru"}

viloyatlar = {
    "uz": {
        "1": "Toshkent",
        "2": "Andijon",
        "99": "Boshqa",
    },
    "de": {
        "1": "Тошкент",
        "2": "Андижон",
        "99": "Бошка",
    },
    "ru": {},
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
        user = await api.update_or_create_user(
            user_id=message.chat.id, full_name=message.from_user.full_name
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


@user_router.message(
    F.text.in_(["🕌 Jamoat vaqtlari", "🕌 Жамоат вақтлари"]), UserStates.menu
)
async def jamoat(message: Message, state: FSMContext):
    data = await state.get_data()
    regions = await api.get_regions(data["locale"])
    await message.answer(
        _("🏙 Hududni  tanlang:", locale=data["locale"]),
        reply_markup=inline.regions_keyboard(regions),
    )


@user_router.callback_query(factory.RegionData.filter())
async def get_districts(
    callback_query: CallbackQuery, callback_data: factory.RegionData, state: FSMContext
):
    data = await state.get_data()
    districts = await api.get_districts(callback_data.region)
    logging.warning(districts)
    await callback_query.message.edit_text(
        _("🏘 Tumanni  tanlang:", locale=data["locale"]),
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
        "🕌 Masjidni tanlang:",
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
            "🕌 Masjidni tanlang:",
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
            "🕌 Masjidni tanlang:",
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
    masjid = await api.masjid_info(callback_data.masjid)
    logging.warning(masjid)
    text = f"""
🕌 Masjid: {masjid[lang_decode[data["locale"]]]}
📍 Manzili: {masjid['district']['region'][lang_decode[data["locale"]]]}, {masjid['district'][lang_decode[data["locale"]]]}

🕒 Vaqtlari:
🏞 Bomdod: {masjid['bomdod']}
🌇 Peshin: {masjid['peshin']}
🌆 Asr: {masjid['asr']}
🌃 Shom: {masjid['shom']}
🌌 Xufton: {masjid['hufton']}
"""

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
                await callback_query.message.edit_text(text=text, reply_markup=markup)
    else:
        await callback_query.message.edit_text(text=text, reply_markup=markup)

    await callback_query.message.delete()


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
        if callback_data.action == "subscribe":
            await callback_query.answer(text="Obuna bo'ldingiz")
        elif callback_data.action == "unsubscribe":
            await callback_query.answer(text="Obunani bekor qildingiz")
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


@user_router.message(F.text.in_(["🇺🇿 Yozuvni o'zgartirish", "🇺🇿 Ёзувни ўзгартириш"]))
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
<b>Bugungi namoz vaqtlari:</b>

<i>🏙 Tong: <b>{tong}</b> (saharlik tugashi) 
🌅 Quyosh: <b>{quyosh}</b>
🏞 Peshin: <b>{peshin}</b>
🌇 Asr: <b>{asr}</b>
🌆 Shom: <b>{shom}</b> (iftorlik boshlanishi)
🌌 Xufton: <b>{xufton}</b></i>
""".format(
            tong=vaqtlar[0],
            quyosh=vaqtlar[1],
            peshin=vaqtlar[2],
            asr=vaqtlar[3],
            shom=vaqtlar[4],
            xufton=vaqtlar[5],
        ),
        locale=data["locale"],
    )

    await message.answer(
        text,
        reply_markup=inline.namoz_vaqtlari_inline(
            mintaqa=bugungi_namoz_vaqti["mintaqa"], lang=data["locale"]
        ),
    )


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
        
        dates = []
        for kun in oylik["items"]:
            vaqtlar = kun["vaqtlari"].split("|")
            sana = f"{current_time.year}.{kun['milodiy_oy']}.{kun['milodiy_kun']}"
            text = _(
                """<i>Sana: <b>{sana}</b>
🏙 Tong: <b>{tong}</b> (saharlik tugashi)
🌅 Quyosh: <b>{quyosh}</b>
🏞 Peshin: <b>{peshin}</b>
🌇 Asr: <b>{asr}</b>
🌆 Shom: <b>{shom}</b> (iftorlik boshlanishi)
🌌 Xufton: <b>{xufton}</b></i>
                     
""".format(
                    sana=sana,
                    tong=vaqtlar[0],
                    quyosh=vaqtlar[1],
                    peshin=vaqtlar[2],
                    asr=vaqtlar[3],
                    shom=vaqtlar[4],
                    xufton=vaqtlar[5],
                ),
                locale=data["locale"],
            )
            dates.append(text)

        await callback_query.message.edit_text(
            _("Ushbu oy namoz vaqtlari:\n\n", locale=data["locale"]) + "".join(dates),
            reply_markup=inline.oylik_namoz_vaqtlari_inline(
                mintaqa=callback_data.mintaqa,
                current_page=page,
                has_next=has_next,
                lang=data["locale"],
            ),
        )
        await state.update_data(current_page=page, current_mintaqa=callback_data.mintaqa)

    if callback_data.action == "downl":
        await callback_query.message.answer_document(f"https://islom.uz/prayertime/pdf/{callback_data.mintaqa}/{current_time.month}")

    if callback_data.action == "changemintaqa":
        await callback_query.message.edit_text(_("Mintaqani o'zgartirish:", locale=data["locale"]), reply_markup=inline.mintaqa_viloyat_inline(viloyatlar[data["locale"]], data["locale"]))

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

        dates = []
        for kun in oylik["items"]:
            vaqtlar = kun["vaqtlari"].split("|")
            sana = f"{current_time.year}.{kun['milodiy_oy']}.{kun['milodiy_kun']}"
            text = _(
                """<i>Sana: <b>{sana}</b>
🏙 Tong: <b>{tong}</b> (saharlik tugashi)
🌅 Quyosh: <b>{quyosh}</b>
🏞 Peshin: <b>{peshin}</b>
🌇 Asr: <b>{asr}</b>
🌆 Shom: <b>{shom}</b> (iftorlik boshlanishi)
🌌 Xufton: <b>{xufton}</b></i>
                     
""".format(
                    sana=sana,
                    tong=vaqtlar[0],
                    quyosh=vaqtlar[1],
                    peshin=vaqtlar[2],
                    asr=vaqtlar[3],
                    shom=vaqtlar[4],
                    xufton=vaqtlar[5],
                ),
                locale=data["locale"],
            )
            dates.append(text)


        

        await callback_query.message.edit_text(
            _("Ushbu oy namoz vaqtlari:\n\n", locale=data["locale"]) + "".join(dates),
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

        dates = []
        for kun in oylik["items"]:
            vaqtlar = kun["vaqtlari"].split("|")
            sana = f"{current_time.year}.{kun['milodiy_oy']}.{kun['milodiy_kun']}"
            text = _(
                """<i>Sana: <b>{sana}</b>
🏙 Tong: <b>{tong}</b> (saharlik tugashi)
🌅 Quyosh: <b>{quyosh}</b>
🏞 Peshin: <b>{peshin}</b>
🌇 Asr: <b>{asr}</b>
🌆 Shom: <b>{shom}</b> (iftorlik boshlanishi)
🌌 Xufton: <b>{xufton}</b></i>
                     
""".format(
                    sana=sana,
                    tong=vaqtlar[0],
                    quyosh=vaqtlar[1],
                    peshin=vaqtlar[2],
                    asr=vaqtlar[3],
                    shom=vaqtlar[4],
                    xufton=vaqtlar[5],
                ),
                locale=data["locale"],
            )
            dates.append(text)


        

        await callback_query.message.edit_text(
            _("Ushbu oy namoz vaqtlari:\n\n", locale=data["locale"]) + "".join(dates),
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
    callback_query: CallbackQuery, callback_data: factory.MintaqaViloyatData, state: FSMContext
):
    pass
    data = await state.get_data()
    
    mintaqalar = await api.get_viloyat_mintaqalari(viloyat_id=callback_data.viloyat_id)
    await callback_query.message.edit_text(
        _("Mintaqani o'zgartirish:", locale=data["locale"]), reply_markup=inline.mintaqa_inline(mintaqalar, data["locale"])
    )

@user_router.callback_query(factory.MintaqaData.filter())
async def mintaqa(
    callback_query: CallbackQuery, callback_data: factory.MintaqaData, state: FSMContext
):
    await callback_query.message.delete(    )
    await state.update_data(mintaqa=callback_data.mintaqa_id)
    await namoz_vaqti(callback_query.message, state)
    # await state.set_state(UserStates.menu)
    # await callback_query.message.answer(
    #         _("🏡 Bosh menyu", locale=data["locale"]),
    #         reply_markup=reply.main_menu_user(data["locale"]),
    #     ) 
