# Модуль с хэндлерами, которые реагируют на апдейты от пользователей
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.users_kb import create_aquarium_keyboard, create_animal_keyboard
import database
from lexic.lexic import LEXICON
import filters


flagmsg = {"throttling_key": "lastmsg",
           "save_update": "save_update"}
flagcb = {"throttling_key": "lastcb",
          "save_update": "save_update"}
flagmsg_save = {"save_update": "save_update"}
flagcb_save = {"save_update": "save_update"}
router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart(), flags=flagmsg)
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю фотографию с номером аквариума
@router.message(Command(commands='help'), flags=flagmsg)
async def process_help_command(message: Message):
    await message.answer_photo(
        photo=LEXICON['photo_id1'],
        caption=LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю фотографию с номером аквариума
@router.message(Command(commands='feedings'), flags=flagmsg)
async def process_feedings_command(message: Message):
    feedings_button: InlineKeyboardButton = InlineKeyboardButton(
        text='расписание',
        url='https://океанариум.рф/shows/')
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[feedings_button]])
    await message.answer(text='Показательные кормления',
                         reply_markup=keyboard)


# Этот хэндлер будет срабатывать на команду "/feedback"
# и перенаправлять пользователя на страницу, где можно оставить отзыв
@router.message(Command(commands='feedback'), flags=flagmsg)
async def process_feedback_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду на отправку пользователем
# номера аквариума от 1 до 60 и выдвать пользователю коллаж из фотографий
# обитателей аквариума и клавиатуру с кнопками-цифрами для выбора обитателя
@router.message(filters.NumberInAquariumNumbers(),
                lambda x: x.text and x.text.isdigit(), flags=flagmsg)
async def aquarium_number_answer(message: Message):
    photo_result = await database.photo_collage(message.text)
    animal_result = await database.buttons_for_keyboard(message.text)
    await message.answer_photo(photo_result,
                               reply_markup=create_aquarium_keyboard(2, animal_result))


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с номерами животных,
# у которых есть дополнительные вопросы c ответами
@router.callback_query(filters.AnimalInQuestionWithAnswer(), flags=flagcb)
async def photo_text_question_answer(callback: CallbackQuery):
    animal = await database.animal_from_db(callback.data)
    question = await database.question_from_db(callback.data)
    answers = await database.answers_from_db(callback.data)
    callbacks = await database.keyboard_from_db_questions(callback.data)
    await callback.message.answer_photo(photo=animal[2],
                                        caption=animal[0])
    if animal[3]:
        await callback.message.answer_audio(audio=animal[3])
    await callback.message.answer(text=animal[1])
    await callback.message.answer(text=question,
                                  reply_markup=create_animal_keyboard(answers, callbacks))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с номерами животных,
# у которых есть дополнительные вопросы без ответов
@router.callback_query(filters.AnimalInQuestions(), flags=flagcb)
async def photo_text_question(callback: CallbackQuery):
    animal = await database.animal_from_db(callback.data)
    question = await database.question_from_db(callback.data)

    await callback.message.answer_photo(photo=animal[2],
                                        caption=animal[0])
    await callback.message.answer(text=animal[1])
    await callback.message.answer(text=question)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с номерами животных,
# не вошедших в первые две категории
@router.callback_query(filters.AnimalInAnimals(), flags=flagcb)
async def photo_and_text(callback: CallbackQuery):
    animal = await database.animal_from_db(callback.data)
    await callback.message.answer_photo(photo=animal[2],
                                        caption=animal[0])
    await callback.message.answer(text=animal[1])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с правильными ответами
# для животных, у которых есть вопросы с ответами
@router.callback_query(filters.AnswerInYesAnswers(), flags=flagcb_save)
async def correct_answer(callback: CallbackQuery):
    answer = await database.answer_yes_from_db(callback.data)
    await callback.message.answer(text=answer)
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с неправильными ответами
# для животных, у которых есть вопросы с ответами
@router.callback_query(filters.AnswerInNoAnswers(), flags=flagcb_save)
async def wrong_answer(callback: CallbackQuery):
    answer = await database.answer_no_from_db(callback.data)
    await callback.message.answer(text=answer)
    await callback.answer()
