from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexic.lexic import LEXICON_ADMIN


# Функция, генерирующая клавиатуру для страницы книги
def create_admin_keyboard() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру
    for k, v in LEXICON_ADMIN.items():
        buttons.append(InlineKeyboardButton(
            text=v,
            callback_data=k))
    kb_builder.row(*buttons, width=1)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
