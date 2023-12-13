import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from tgbot.services import api
from tgbot.keyboards import factory, inline, reply
from tgbot.keyboards.factory import _
from tgbot.misc.states import UserStates

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("registered", False):
        await message.answer(
            _("Bosh menyu", locale=data["locale"]),
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
        _("Bosh menyu", locale=data["locale"]),
        reply_markup=reply.main_menu_user(data["locale"]),
    )
    await state.set_state(UserStates.menu)


@user_router.message(
    F.text.in_(["Jamoat vaqtlari", "Jamoat vaqtlari"]), UserStates.menu
)
async def jamoat(message: Message, state: FSMContext):
    data = await state.get_data()
    regions = await api.get_regions(data["locale"])
    await message.answer(
        _("Hududni  tanlang:", locale=data["locale"]),
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
        _("Tumanni  tanlang:", locale=data["locale"]),
        reply_markup=inline.districts_keyboard(districts, data["locale"]),
    )


@user_router.callback_query(factory.DistrictData.filter())
async def get_masjids(
    callback_query: CallbackQuery,
    callback_data: factory.DistrictData,
    state: FSMContext,
):
    await state.update_data(current_page=1, current_district=callback_data.ditrict)
    data = await state.get_data()
    masjidlar = await api.get_masjidlar(callback_data.ditrict)
    has_next = True if (1 * 5) < masjidlar["count"] else False

    logging.warning(masjidlar)
    await callback_query.message.edit_text(
        "Masjidni tanlang:",
        reply_markup=inline.masjidlar_keyboard(
            masjidlar["items"], lang=data["locale"], current_page=1, has_next=has_next
        ),
    )


@user_router.callback_query(factory.PagesData.filter())
async def get_masjids(
    callback_query: CallbackQuery, callback_data: factory.PagesData, state: FSMContext
):
    data = await state.get_data()

    if callback_data.action == "next":
        page = int(data["current_page"]) + 1
        masjidlar = await api.get_masjidlar(data["current_district"], page=page)
        has_next = True if ((page ) * 5) < masjidlar["count"] else False
        await callback_query.message.edit_text(
            "Masjidni tanlang:",
            reply_markup=inline.masjidlar_keyboard(
                masjidlar["items"], lang=data["locale"], current_page=page, has_next=has_next
            ),
        )

        await state.update_data(current_page=page)

    elif callback_data.action == "prev" and int(data["current_page"]) > 1:
        page = int(data["current_page"]) - 1
        masjidlar = await api.get_masjidlar(data["current_district"], page=page)

        has_next = True if ((page) * 5) < masjidlar["count"] else False


        await callback_query.message.edit_text(
            "Masjidni tanlang:",
            reply_markup=inline.masjidlar_keyboard(
                masjidlar["items"], lang=data["locale"], current_page=page
            ),
        )

        await state.update_data(current_page=page)

    await callback_query.answer()

@user_router.callback_query(factory.MasjidData.filter())
async def get_masjid(
    callback_query: CallbackQuery, callback_data: factory.MasjidData, state: FSMContext
):
    data = await state.get_data()