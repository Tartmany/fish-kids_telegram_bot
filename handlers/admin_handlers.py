from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import pandas as pd

from database.update_db_queries import load_updates, delete_updates
from config_data.config import Config, load_config
from keyboards.admin_kb import create_admin_keyboard


router: Router = Router()
config: Config = load_config()
admins_ids = config.tg_bot.admin_ids


# Этот хэндлер будет срабатывать на если пользователь есть в списке
# админов и он отправил сообщение "Обновить базу"
@router.message(F.from_user.id.in_(admins_ids), Text(startswith='обновить базу', ignore_case=True))
async def admin_answer(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Что будем менять?',
                         reply_markup=create_admin_keyboard())


# Этот хэндлер будет срабатывать на нажатие кнопки "Загрузить статистику"
# и переводить бота в состояние ожидания ввода названия животного
@router.callback_query(Text(text='load_data'))
async def process_load_updates(callback: CallbackQuery):
    results = await load_updates()
    columns = ["update_id", "user_id", "date", "message"]
    df = pd.DataFrame(results, columns=columns)
    df.to_csv('updates_database.csv', encoding='utf-8', index=False)
    await callback.message.answer(text='Статистика выгружена на сервер')


# Этот хэндлер будет срабатывать на нажатие кнопки Очистить статисктику апдейтов"
# и переводить бота в состояние ожидания ввода названия животного
@router.callback_query(Text(text='delete_update_data'))
async def process_delete_updates(callback: CallbackQuery):
    await delete_updates()
    await callback.message.answer(text='Статистика удалена из базы')
