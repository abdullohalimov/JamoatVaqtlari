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
    await message.answer("Assalomu alaykum.\n✅ Yozuvni tanlang:", reply_markup=inline.language_keyboard())
    test = await api.update_or_create_user(user_id=message.chat.id, full_name=message.from_user.full_name)

@user_router.callback_query(factory.LanguageData.filter())
async def set_language(callback_query: CallbackQuery, callback_data: factory.LanguageData, state: FSMContext):
    if callback_data.language == "uz":
        await state.update_data(locale="uz")
    elif callback_data.language == "de":
        await state.update_data(locale="de")
    elif callback_data.language == "ru":
        await state.update_data(locale="ru")
    data = await state.get_data()
    await callback_query.message.answer(_("Bosh menyu", locale=data['locale']), reply_markup=reply.main_menu_user(data['locale']))
    await state.set_state(UserStates.menu)

@user_router.message(F.text.in_(["Jamoat vaqtlari", "Jamoat vaqtlari"]), UserStates.menu)
async def jamoat(message: Message, state: FSMContext):
    data = await state.get_data()
    regions = await api.get_regions(data['locale'])
    await message.answer(_("Masjidingizni tanlang:", locale=data['locale']), reply_markup=inline.regions_keyboard(regions))
