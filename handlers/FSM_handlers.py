from aiogram import F, Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize, Audio)
from states.states import (FSMAnimalForm, FSMInsertAnimalAquarium,
                           FSMDelAnimalAquarium, FSMNewAquarium,
                           FSMChangeAquariumNumber, FSMAquariumPhotoChange,
                           FSCMQuestionInsert, FSMUpdateAnimal,
                           FSMDeleteQuestion)

import database

from filters.filters import AnimalInAnimalsMessage, AnimalInAnimalNames, AnimalInQuestionsMessage


router: Router = Router()


# Этот хэндлер будет срабатывать на нажатие кнопки "Добавить новое животное"
# и переводить бота в состояние ожидания ввода названия животного
@router.callback_query(Text(text='add_new_animal'), StateFilter(default_state))
async def process_callback_animal_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите название животного с заглавной буквы')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMAnimalForm.fill_name)


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте текст "Обновить базу"')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте текст "Обновить базу"')


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMAnimalForm.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите текст о животном')
    # Устанавливаем состояние ожидания ввода текста о животном
    await state.set_state(FSMAnimalForm.fill_description)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMAnimalForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на название животного!\n\n'
                              'Пожалуйста, введите название животного\n\n'
                              'Если вы хотите прервать процесс - '
                              'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если введено описание животного
# и переводить в состояние написания callback для животного
@router.message(StateFilter(FSMAnimalForm.fill_description))
async def process_description_sent(message: Message, state: FSMContext):
    # Cохраняем описание в хранилище по ключу "description"
    await state.update_data(description=message.text)
    await message.answer(text='Спасибо!\n\nВведите название животного в английской транскрипции. '
                              'Вместо пробелов используйте "_" нижнее подчеркивание')
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMAnimalForm.fill_callback)


# Этот хэндлер будет ловить введенное на транслите название
# и переводить в состояние отправки фото
@router.message(StateFilter(FSMAnimalForm.fill_callback))
async def process_callback_sent(message: Message, state: FSMContext):
    # Cохраняем callback (callback.data нажатой кнопки) в хранилище,
    # по ключу "callback"
    await state.update_data(callback=message.text)
    await message.answer(text='Спасибо! А теперь загрузите, '
                              'пожалуйста, фото животного')
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMAnimalForm.upload_photo_animal)


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора номера аквариума
@router.message(StateFilter(FSMAnimalForm.upload_photo_animal),
                F.photo[-1].as_('largest_photo'))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    # Cохраняем данные фото file_id в хранилище
    # по ключу"photo_id"
    await state.update_data(photo_id=largest_photo.file_id)
    await message.answer(text='Спасибо!\n\nУкажите цифрами номер аквариума,'
                              'в котором обитает это животное')
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FSMAnimalForm.fill_aquarium_number)


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMAnimalForm.upload_photo_animal))
async def warning_not_photo(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'фото.\n\nЕсли вы хотите прервать '
                              'процесс - отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если введен номер аквариума
# и отправлять полученные данные в базу
@router.message(StateFilter(FSMAnimalForm.fill_aquarium_number),
                F.text.isdigit())
async def process_aq_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    await state.update_data(aq_number=int(message.text))
    animal_dict = await state.get_data()
    # Завершаем машину состояний
    animal = (animal_dict["name"],
              animal_dict["description"],
              animal_dict["photo_id"],
              animal_dict["callback"]
              )
    await database.insert_animals(animal)
    animal_id = await database.animal_db()
    aq_an = (int(animal_id),
             animal_dict["aq_number"])
    await database.insert_aq_an(aq_an)

    await state.clear()

    # Отправляем в чат сообщение об успешном окончании операций
    await message.answer(text='Животное внесено в базу\n\n')


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMAnimalForm.fill_aquarium_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Поменять фотоколлаж аквариума"
# и переводить бота в состояние ожидания ввода номера аквариума
@router.callback_query(Text(text='update_aquarium_photo'), StateFilter(default_state))
async def process_callback_update_aq_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите номер аквариума')
    # Устанавливаем состояние ожидания ввода номера аквариума
    await state.set_state(FSMAquariumPhotoChange.fill_aquarium_number)


# Этот хэндлер будет срабатывать, если введен номер аквариума
# и переводить в состояние получения фото аквариума
@router.message(StateFilter(FSMAquariumPhotoChange.fill_aquarium_number),
                F.text.isdigit())
async def process_aq_number(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    await state.update_data(aq_number=int(message.text))
    await message.answer(text='Спасибо!\n\nА теперь загрузите, '
                              'пожалуйста, фотоколлаж аквариума.')
    await state.set_state(FSMAquariumPhotoChange.upload_photo)


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMAquariumPhotoChange.fill_aquarium_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора номера аквариума
@router.message(StateFilter(FSMAquariumPhotoChange.upload_photo),
                F.photo[-1].as_('largest_photo'))
async def process_photo_sent_aq(message: Message,
                                state: FSMContext,
                                largest_photo: PhotoSize):
    # Cохраняем данные фото file_id в хранилище
    # по ключу "photo_id"
    await state.update_data(photo_id=largest_photo.file_id)
    aq_photo_dict = await state.get_data()
    # Завершаем машину состояний
    aq_photo = (aq_photo_dict["photo_id"],
                aq_photo_dict["aq_number"])
    await database.update_aquarium_photo(aq_photo)

    await state.clear()
    await message.answer(text='Фотоколлаж аквариума обновлен')


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMAquariumPhotoChange.upload_photo))
async def warning_not_photo(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'фото.\n\nЕсли вы хотите прервать '
                              'процесс - отправьте команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Добавить вопрос"
# и переводить бота в состояние ожидания ввода названия животного
@router.callback_query(Text(text='add_question'), StateFilter(default_state))
async def process_callback_add_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите название животного на транслите для которого '
                                       'Вы хотите добавить вопрос')
    # Устанавливаем состояние ожидания ввода номера аквариума
    await state.set_state(FSCMQuestionInsert.fill_animal_callback)


# Этот хендлер срабатывает, если корректно введено транслит название животного,
# записывает его и переводит в состояние ожидания вопроса
@router.message(StateFilter(FSCMQuestionInsert.fill_animal_callback),
                AnimalInAnimalsMessage())
async def process_callback_take(message: Message, state: FSMContext):
    # Cохраняем callback в хранилище по ключу "callback_name"
    await state.update_data(callback_name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь пришлите ваш вопрос.')
    # Устанавливаем состояние ожидания вопроса
    await state.set_state(FSCMQuestionInsert.fill_question)


# Этот хэндлер будет срабатывать, если во время введения трнслит названия
# животного будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSCMQuestionInsert.fill_animal_callback))
async def warning_not_callback(message: Message):
    await message.answer(text='Введите название животного на транслите '
                              'из тех, которые имеются в базе данных.\n\n'
                              'Если вы хотите прервать заполнение анкеты '
                              '- отправьте команду /cancel')


# Этот хендлер срабатывает, если корректно введен вопрос о животном,
# записывает его и спрашивает, есть ли варианты ответа у этого вопроса
@router.message(StateFilter(FSCMQuestionInsert.fill_question))
async def process_callback_take(message: Message, state: FSMContext):
    # Cохраняем вопрос в хранилище по ключу "question"
    await state.update_data(question=message.text)
    # Создаем объекты инлайн-кнопок
    yes_button = InlineKeyboardButton(text='Да',
                                      callback_data='yes_question')
    no_button = InlineKeyboardButton(text='Нет',
                                     callback_data='no_question')
    # Добавляем кнопки в клавиатуру
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(text='Спасибо!\n\nНужны ли варианты ответов к этому вопросу?',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания вопроса
    await state.set_state(FSCMQuestionInsert.fill_answer_choice)


# Этот хэндлер будет срабатывать на нажатие кнопки "Нет" при вопросе будут ли ответы
# записывать данные в БД и выходить из машины состояний
@router.callback_query(Text(text='no_question'),
                       StateFilter(FSCMQuestionInsert.fill_answer_choice))
async def process_no_answers_end(callback: CallbackQuery, state: FSMContext):
    qt_dict = await state.get_data()
    # Завершаем машину состояний
    an_id = await database.animal_id_by_callback(qt_dict["callback_name"])
    qt = (int(an_id), qt_dict["callback_name"],
          qt_dict["question"])
    await database.add_question_without_answers(qt)

    await state.clear()
    await callback.message.answer(text='Вопрос внесен в базу')


# Этот хэндлер будет срабатывать на нажатие кнопки "Да" при вопросе будут ли ответы
# и запрашивать варианты ответов
@router.callback_query(Text(text='yes_question'),
                       StateFilter(FSCMQuestionInsert.fill_answer_choice))
async def process_yes_answers(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Спасибо! Теперь необходимо записать варианты '
                                       'ответа в следующем формате: '
                                       '<b>"Ответ1:неправильно:Ответ2:правильно"</b> и т.д.\n'
                                       'Порядок ответов не важен. Количество тоже. '
                                       'Главное, чтобы после каждого '
                                       'было написано правильно/неправильно.\nРазделитель везде ":" '
                                       'В конце разделитель не ставим.\nКак минимум один правильный '
                                       'ответ должен быть обязательно.\n'
                                       'Если у вас два варианта ответа, оба правильные, но с разными '
                                       'сообщениями, которые возвращаются пользавателю, назначьте один '
                                       'ответ неправильным')
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSCMQuestionInsert.fill_answer)


# Этот хендлер срабатывает, если введены варианты ответов о животном,
# записывает их, и переводит машину в сотсояние ожидания правильного ответа
@router.message(StateFilter(FSCMQuestionInsert.fill_answer),
                lambda x: x.text and 'правильно' in x.text.split(':')
                and not len(x.text.split(':')) % 2)
async def process_answers_take(message: Message, state: FSMContext):
    # Cохраняем варианты ответа в хранилище по ключу "answer"
    await state.update_data(answer=message.text)
    await message.answer(text='Спасибо!\n\nВведите текст, который появится, '
                              'если посетитель правильно ответил на вопрос')
    # Устанавливаем состояние ожидания вопроса
    await state.set_state(FSCMQuestionInsert.fill_correct_answer)


# Этот хендлер срабатывает, если варианты ответов о животном,
# введены некорретно
@router.message(StateFilter(FSCMQuestionInsert.fill_answer))
async def process_wrong_answers(message: Message):
    await message.answer(text='Варианты ответов написаны некорректно. '
                              'Введите, пожалуйста, варианты ответов по образцу выше')


# Этот хендлер срабатывает, если введен правильный ответ,
# записывает его и просит callback для кнопки правильного ответа
@router.message(StateFilter(FSCMQuestionInsert.fill_correct_answer))
async def process_correct_answers_take(message: Message, state: FSMContext):
    # Cохраняем правильный ответ в хранилище по ключу "yes_answer"
    await state.update_data(yes_answer=message.text)
    await message.answer(text='Спасибо!\n\nТеперь введите транслит текст в формате:'
                              '"yes_&ltтранслит имя животного, которое было дано на первом шаге&gt" ')
    # Устанавливаем состояние ожидания текста для callback
    await state.set_state(FSCMQuestionInsert.fill_correct_callback)


# Этот хендлер срабатывает, если введен текст для yes_callback,
# записывает его и спрашивает, есть ли неправильные ответы
@router.message(StateFilter(FSCMQuestionInsert.fill_correct_callback))
async def process_correct_callback_take(message: Message, state: FSMContext):
    # Cохраняем yes_callback в хранилище
    await state.update_data(yes_callback=message.text)
    # Создаем объекты инлайн-кнопок
    yes_button = InlineKeyboardButton(text='Да',
                                      callback_data='yes_wrong_answer')
    no_button = InlineKeyboardButton(text='Нет',
                                     callback_data='no_wrong_answer')
    # Добавляем кнопки в клавиатуру (две в одном ряду)
    keyboard: list[list[InlineKeyboardButton]] = [[yes_button, no_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(text='Спасибо!\n\nЕсть ли неправильные варианты '
                              'ответов к этому вопросу?',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора
    await state.set_state(FSCMQuestionInsert.fill_wrong_answer_choice)


# Этот хэндлер будет срабатывать на нажатие кнопки "Нет" при вопросе будут ли
# неправильные варианты ответа, записывать данные в БД и выходить из машины состояний
@router.callback_query(Text(text='no_wrong_answer'),
                       StateFilter(FSCMQuestionInsert.fill_wrong_answer_choice))
async def process_no_wrong_answers_end(callback: CallbackQuery, state: FSMContext):
    qt_dict = await state.get_data()
    # Завершаем машину состояний
    an_id = await database.animal_id_by_callback(qt_dict["callback_name"])
    qt = (int(an_id), qt_dict["callback_name"],
          qt_dict["question"], qt_dict["answer"],
          qt_dict["yes_answer"], qt_dict["yes_callback"])

    await database.add_question_with_one_answer(qt)

    await state.clear()
    await callback.message.answer(text='Вопрос внесен в базу')


# Этот хэндлер будет срабатывать на нажатие кнопки "Да" при вопросе будут ли
# неправильные ответы на вопрос и спрашивать этот неправильный ответ
@router.callback_query(Text(text='yes_wrong_answer'),
                       StateFilter(FSCMQuestionInsert.fill_wrong_answer_choice))
async def process_yes_wrong_answers(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Тогда введите сообщение, которое будет получать пользователь, '
                                       'если ответит неправильно')
    # Устанавливаем состояние ожидания послания на неправильный ответ
    await state.set_state(FSCMQuestionInsert.fill_wrong_answer)


# Этот хендлер срабатывает, если введен неправильный ответ,
# записывает его и просит callback для кнопки правильного ответа
@router.message(StateFilter(FSCMQuestionInsert.fill_wrong_answer))
async def process_correct_answers_take(message: Message, state: FSMContext):
    # Cохраняем правильный ответ в хранилище по ключу "no_answer"
    await state.update_data(no_answer=message.text)
    await message.answer(text='Спасибо!\n\nОсталось ввести транслит текст в формате:'
                              '"no_&ltтранслит имя животного, которое было дано на первом шаге&gt" ')
    # Устанавливаем состояние ожидания текста для callback
    await state.set_state(FSCMQuestionInsert.fill_wrong_callback)


# Этот хэндлер будет срабатывать на ввод no_callback,
# записывать данные в БД и выходить из машины состояний
@router.message(StateFilter(FSCMQuestionInsert.fill_wrong_callback))
async def process_question_end(message: Message, state: FSMContext):
    await state.update_data(no_callback=message.text)
    qt_dict = await state.get_data()
    # Завершаем машину состояний
    an_id = await database.animal_id_by_callback(qt_dict["callback_name"])
    qt = (int(an_id), qt_dict["callback_name"],
          qt_dict["question"], qt_dict["answer"],
          qt_dict["yes_answer"], qt_dict["yes_callback"],
          qt_dict["no_answer"], qt_dict["no_callback"])

    await database.add_question(qt)

    await state.clear()
    await message.answer(text='Вопрос внесен в базу')


# Этот хэндлер будет срабатывать на нажатие кнопки "Удалить животное из аквариума"
# и переводить бота в состояние ожидания ввода номера аквариума
@router.callback_query(Text(text='del_animal'), StateFilter(default_state))
async def process_callback_del_animal(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите цифрой номер аквариума, из которого '
                                       'необходимо удалить животного')
    # Устанавливаем состояние ожидания ввода номера аквариума
    await state.set_state(FSMDelAnimalAquarium.fill_aquarium_number)


# Этот хэндлер будет срабатывать, если введен номер аквариума
# и отправлять полученные данные в базу, запрашивать название животного
@router.message(StateFilter(FSMDelAnimalAquarium.fill_aquarium_number),
                F.text.isdigit())
async def process_aq_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    await state.update_data(aq_number=int(message.text))
    await message.answer(text='Спасибо!\n\nВведите название животного с заглавной буквы')
    # Устанавливаем состояние ожидания названия животного
    await state.set_state(FSMDelAnimalAquarium.fill_animal)


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMDelAnimalAquarium.fill_aquarium_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать, если введно правильное название животного
# и отправлять полученные данные в базу, удалять животного из аквариума
# и выходить из машины состояний
@router.message(StateFilter(FSMDelAnimalAquarium.fill_animal),
                AnimalInAnimalNames())
async def process_animal_name_sent(message: Message, state: FSMContext):
    # Cохраняем данные о животном по ключу "animal_name"
    await state.update_data(animal_name=message.text)
    del_dict = await state.get_data()
    # Завершаем машину состояний
    an_id = await database.animal_id_by_name(del_dict["animal_name"])
    dl = (int(del_dict["aq_number"]), int(an_id))

    await database.del_animal_from_aq(dl)

    await state.clear()
    await message.answer(text='Животное удалено из базы')


# Этот хэндлер будет срабатывать, если во время введения названия животного
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMDelAnimalAquarium.fill_animal))
async def warning_not_name(message: Message):
    await message.answer(text='Пожалуйста, введите название животного из базы '
                              'с заглавной буквы.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Добавить животное из базы в аквариум"
# и переводить бота в состояние ожидания ввода номера аквариума
@router.callback_query(Text(text='add_animal'), StateFilter(default_state))
async def process_callback_add_animal(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите цифрой номер аквариума, в который '
                                       'необходимо добавить животного')
    # Устанавливаем состояние ожидания ввода номера аквариума
    await state.set_state(FSMInsertAnimalAquarium.fill_aquarium_number)


# Этот хэндлер будет срабатывать, если введен номер аквариума
# и отправлять полученные данные в базу, запрашивать название животного
@router.message(StateFilter(FSMInsertAnimalAquarium.fill_aquarium_number),
                F.text.isdigit())
async def process_aq_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    await state.update_data(aq_number=int(message.text))
    await message.answer(text='Спасибо!\n\nВведите название животного с большой буквы')
    # Устанавливаем состояние ожидания названия животного
    await state.set_state(FSMInsertAnimalAquarium.fill_animal)


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMInsertAnimalAquarium.fill_aquarium_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать, если введно правильное название животного
# и отправлять полученные данные в базу, удалять животного из аквариума
# и выходить из машины состояний
@router.message(StateFilter(FSMInsertAnimalAquarium.fill_animal),
                AnimalInAnimalNames())
async def process_animal_name_sent(message: Message, state: FSMContext):
    # Cохраняем данные о животном по ключу "animal_name"
    await state.update_data(animal_name=message.text)
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    an_id = await database.animal_id_by_name(ins_dict["animal_name"])
    ins = (int(an_id), int(ins_dict["aq_number"]))

    await database.ins_animal_into_aq(ins)

    await state.clear()
    await message.answer(text='Животное добавлено в аквариум')


# Этот хэндлер будет срабатывать, если во время введения названия животного
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMInsertAnimalAquarium.fill_animal))
async def warning_not_name(message: Message):
    await message.answer(text='Пожалуйста, введите название животного из базы '
                              'с заглавной буквы.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Изменить информацию о животном"
# и переводить бота в состояние ожидания ввода номера аквариума
@router.callback_query(Text(text='update_animal_info'), StateFilter(default_state))
async def process_callback_update_animal(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите с заглавной буквы название животного, '
                                       'информацияю о котором Вы хотите изменить')
    # Устанавливаем состояние ожидания ввода номера аквариума
    await state.set_state(FSMUpdateAnimal.fill_animal_name)


# Этот хэндлер будет срабатывать, если введно правильное название животного
# и отправлять полученные данные в базу, удалять животного из аквариума
# и выходить из машины состояний
@router.message(StateFilter(FSMUpdateAnimal.fill_animal_name),
                AnimalInAnimalNames())
async def process_animal_name_sent(message: Message, state: FSMContext):
    # Cохраняем данные о животном по ключу "animal_name"
    await state.update_data(animal_name=message.text)
    # Создаем объекты инлайн-кнопок
    name_button = InlineKeyboardButton(text='Название',
                                       callback_data='update_name')
    description_button = InlineKeyboardButton(text='Описание',
                                              callback_data='update_description')
    photo_button = InlineKeyboardButton(text='Фотографию',
                                        callback_data='update_photo')
    audio_button = InlineKeyboardButton(text='Аудио',
                                        callback_data='update_audio')
    # Добавляем кнопки в клавиатуру
    keyboard: list[list[InlineKeyboardButton]] = [[name_button], [description_button],
                                                  [photo_button], [audio_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(text='Что будем менять?',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания вопроса
    await state.set_state(FSMUpdateAnimal.fill_answer_choice)


# Этот хэндлер будет срабатывать, если во время введения названия животного
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMUpdateAnimal.fill_animal_name))
async def warning_not_name(message: Message):
    await message.answer(text='Пожалуйста, введите название животного из базы '
                              'с большой буквы.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Название" при вопросе будут
# что будем менять. И переводить в состояние ожидания нового названия.
@router.callback_query(Text(text='update_name'),
                       StateFilter(FSMUpdateAnimal.fill_answer_choice))
async def process_update_name_answers(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите новое название животного с заглавной буквы')
    # Устанавливаем состояние ожидания нового названия животного
    await state.set_state(FSMUpdateAnimal.fill_name)


# Этот хэндлер будет срабатывать, если введно новое название животного
# и отправлять полученные данные в базу, и выходить из машины состояний
@router.message(StateFilter(FSMUpdateAnimal.fill_name))
async def process_new_animal_name_sent(message: Message, state: FSMContext):
    # Cохраняем данные о животном по ключу "new_animal_name"
    await state.update_data(new_animal_name=message.text)
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    an_id = await database.animal_id_by_name(ins_dict["animal_name"])
    ins = (int(an_id), ins_dict["new_animal_name"])

    await database.update_animal_name(ins)

    await state.clear()
    await message.answer(text='Название животного обновлено')


# Этот хэндлер будет срабатывать на нажатие кнопки "Описание" при вопросе будут
# что будем менять. И переводить в состояние ожидания нового названия.
@router.callback_query(Text(text='update_description'),
                       StateFilter(FSMUpdateAnimal.fill_answer_choice))
async def process_update_description_answers(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите новое описание животного')
    # Устанавливаем состояние ожидания нового названия животного
    await state.set_state(FSMUpdateAnimal.fill_description)


# Этот хэндлер будет срабатывать, если введно новое описание животного,
# отправлять полученные данные в базу, и выходить из машины состояний
@router.message(StateFilter(FSMUpdateAnimal.fill_description))
async def process_new_animal_description_sent(message: Message, state: FSMContext):
    # Cохраняем данные о животном по ключу "new_animal_name"
    await state.update_data(new_description=message.text)
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    ins = (ins_dict["animal_name"], ins_dict["new_description"])

    await database.update_animal_description(ins)

    await state.clear()
    await message.answer(text='Описание животного обновлено')


# Этот хэндлер будет срабатывать на нажатие кнопки "Фотографию" при вопросе будут
# что будем менять. И переводить в состояние ожидания нового названия.
@router.callback_query(Text(text='update_photo'),
                       StateFilter(FSMUpdateAnimal.fill_answer_choice))
async def process_yes_wrong_answers(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Отправьте новую фотографию')
    # Устанавливаем состояние ожидания новой фотографии
    await state.set_state(FSMUpdateAnimal.upload_photo)


# Этот хэндлер будет срабатывать, если прислана фотография
# и отправлять полученные данные в базу, и выходить из машины состояний
@router.message(StateFilter(FSMUpdateAnimal.upload_photo), F.photo[-1].as_('largest_photo'))
async def process_update_photo_sent(message: Message,
                                    state: FSMContext,
                                    largest_photo: PhotoSize):
    # Cохраняем данные фото file_id в хранилище
    # по ключу "photo_id"
    await state.update_data(photo_id=largest_photo.file_id)
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    ins = (ins_dict["animal_name"], ins_dict["photo_id"])

    await database.update_animal_photo(ins)

    await state.clear()
    await message.answer(text='Фотография животного обновлена')


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMUpdateAnimal.upload_photo))
async def warning_not_photo(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'фото.\n\nЕсли вы хотите прервать '
                              'процесс - отправьте команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Аудио" при вопросе будут
# что будем менять. И переводить в состояние ожидания нового названия.
@router.callback_query(Text(text='update_audio'),
                       StateFilter(FSMUpdateAnimal.fill_answer_choice))
async def process_yes_wrong_answers(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Отправьте аудиозапись')
    # Устанавливаем состояние ожидания новой фотографии
    await state.set_state(FSMUpdateAnimal.upload_audio)


# Этот хэндлер будет срабатывать, если прислана фотография
# и отправлять полученные данные в базу, и выходить из машины состояний
@router.message(StateFilter(FSMUpdateAnimal.upload_photo), F.audio.as_('audio'))
async def process_update_photo_sent(message: Message,
                                    state: FSMContext,
                                    audio: Audio):
    # Cохраняем данные аудио file_id в хранилище
    # по ключу "audio_id"
    await state.update_data(audio_id=audio.file_id)
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    ins = (ins_dict["animal_name"], ins_dict["audio_id"])

    await database.update_animal_audio(ins)

    await state.clear()
    await message.answer(text='Аудио животного обновлено')


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMUpdateAnimal.upload_audio))
async def warning_not_audio(message: Message):
    await message.answer(text='Пожалуйста, на этом шаге отправьте '
                              'аудиозапись.\n\nЕсли вы хотите прервать '
                              'процесс - отправьте команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Добавить аквариум"
# и переводить бота в состояние ожидания ввода номера аквариума
@router.callback_query(Text(text='add_aquarium'), StateFilter(default_state))
async def process_callback_add_animal(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите цифрой номер нового аквариума. '
                                       'Он не должен пересекаться со старыми')
    # Устанавливаем состояние ожидания ввода номера аквариума
    await state.set_state(FSMNewAquarium.fill_aquarium_number)


# Этот хэндлер будет срабатывать, если введен номер аквариума
# и отправлять полученные данные в базу, запрашивать название животного
@router.message(StateFilter(FSMNewAquarium.fill_aquarium_number),
                F.text.isdigit())
async def process_aq_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    await state.update_data(aq_number=int(message.text))
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    ins = (ins_dict["aq_number"])
    await database.insert_new_aquarium(ins)

    await state.clear()
    await message.answer(text='Новый аквариум добавлен. Фотоколлаж к нему'
                              'можно жобавить по кнопке "Поменять фотоколлаж аквариума"')


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMNewAquarium.fill_aquarium_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Изменить номер аквариума"
# и переводить бота в состояние ожидания ввода id аквариума
@router.callback_query(Text(text='change_aquarium_number'), StateFilter(default_state))
async def process_callback_add_animal(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите цифрой id аквариума. '
                                       '<b>Внимание!</b> Это изначальный номер аквариума,'
                                       ' который добавлялся в таблицу при создании')
    # Устанавливаем состояние ожидания ввода id аквариума
    await state.set_state(FSMChangeAquariumNumber.fill_aquarium_id)


# Этот хэндлер будет срабатывать, если введен id аквариума
# и отправлять полученные данные в словарь, запрашивать старый номер аквариума
@router.message(StateFilter(FSMChangeAquariumNumber.fill_aquarium_id),
                F.text.isdigit())
async def process_aq_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_id"
    await state.update_data(aq_id=int(message.text))
    await message.answer(text='Теперь введите цифрами старый номер аквариума')
    # Устанавливаем состояние ожидания ввода старого номера аквариума
    await state.set_state(FSMChangeAquariumNumber.fill_old_number)


# Этот хэндлер будет срабатывать, если во время введения id аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMChangeAquariumNumber.fill_aquarium_id))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать, если введен старый номер аквариума,
# получать по нему список животных и добавлять его в словарь
@router.message(StateFilter(FSMChangeAquariumNumber.fill_old_number),
                F.text.isdigit())
async def process_old_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    animals = await database.animal_ids_from_aquarium(int(message.text))
    await state.update_data(animals=animals)
    await message.answer(text='Теперь введите цифрами новый номер аквариума')
    # Устанавливаем состояние ожидания ввода id аквариума
    await state.set_state(FSMChangeAquariumNumber.fill_new_number)


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMChangeAquariumNumber.fill_old_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать, если введен номер аквариума
# и отправлять полученные данные в базу
@router.message(StateFilter(FSMChangeAquariumNumber.fill_new_number),
                F.text.isdigit())
async def process_new_number_sent(message: Message, state: FSMContext):
    # Cохраняем данные о номере аквариума по ключу "aq_number"
    await state.update_data(aq_number=int(message.text))
    ins_dict = await state.get_data()
    # Завершаем машину состояний
    ins = (ins_dict["aq_id"], ins_dict["aq_number"])
    await database.change_aquarium_number(ins)
    num = ins_dict["aq_number"]
    animals = ins_dict["animals"]
    an_num = []
    for i in animals:
        animal = (num, i)
        an_num.append(animal)
    await database.change_aq_number_for_animals(an_num)

    await state.clear()
    await message.answer(text='Номер аквариума изменен')


# Этот хэндлер будет срабатывать, если во время введения номера аквариума
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMChangeAquariumNumber.fill_new_number))
async def warning_not_number(message: Message):
    await message.answer(text='Пожалуйста, введите номер аквариума '
                              'цифрами.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки "Удалить вопрос"
# и переводить бота в состояние ожидания ввода названия животного
@router.callback_query(Text(text='delete_question'), StateFilter(default_state))
async def process_callback_add_animal(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите транслит название животного, '
                                       'вопрос о котором необходимо удалить')
    # Устанавливаем состояние ожидания ввода call_back животного
    await state.set_state(FSMDeleteQuestion.fill_animal_name)


# Этот хэндлер будет срабатывать, если введно правильное транслит название животного,
# удалять вопрос из базы данных и выходить из машины состояний
@router.message(StateFilter(FSMDeleteQuestion.fill_animal_name),
                AnimalInQuestionsMessage())
async def process_animal_name_sent(message: Message, state: FSMContext):
    # Cохраняем данные о животном по ключу "animal_name"
    await state.update_data(callback_name=message.text)
    del_dict = await state.get_data()
    # Завершаем машину состояний
    cb_n = (del_dict["callback_name"])

    await database.del_question_from_aq(cb_n)

    await state.clear()
    await message.answer(text='Вопрос удален из базы')


# Этот хэндлер будет срабатывать, если во время введения транслит названия животного
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMDeleteQuestion.fill_animal_name))
async def warning_not_name(message: Message):
    await message.answer(text='Пожалуйста, введите транслит название животного '
                              'из базы.\n\nЕсли вы хотите '
                              'прервать процесс - отправьте '
                              'команду /cancel')
