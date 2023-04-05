from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_aquarium_keyboard(width: int, animals: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру
    for button in range(len(animals)):
        buttons.append(InlineKeyboardButton(
            text=f'{button+1}',
            callback_data=animals[button]))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


def create_animal_keyboard(answers: list, callbacks: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    # Наполняем клавиатуру
    for button in range(len(answers)-1):
        if answers[button + 1] == 'правильно':
            buttons.append(InlineKeyboardButton(
                text=f'{answers[button]}',
                callback_data=callbacks[0]))
        elif answers[button + 1] == 'неправильно':
            buttons.append(InlineKeyboardButton(
                text=f'{answers[button]}',
                callback_data=callbacks[1]))
    kb_builder.row(*buttons, width=int(len(answers)/2))
    return kb_builder.as_markup()
