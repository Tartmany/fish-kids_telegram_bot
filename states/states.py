from aiogram.filters.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний при
# добавлении нового животного в базу
class FSMAnimalForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()        # Состояние ожидания ввода имени
    fill_description = State()         # Состояние ожидания ввода описания
    fill_callback = State()      # Состояние ожидания воовда названия для callback
    upload_photo_animal = State()     # Состояние ожидания загрузки фото животного
    fill_aquarium_number = State() # Состояние ожидания ввода номера аквариума


class FSMAquariumPhotoChange(StatesGroup):
    fill_aquarium_number = State()
    upload_photo = State()


class FSMInsertAnimalAquarium(StatesGroup):
    fill_aquarium_number = State()
    fill_animal = State()


class FSMDelAnimalAquarium(StatesGroup):
    fill_aquarium_number = State()
    fill_animal = State()


class FSMNewAquarium(StatesGroup):
    fill_aquarium_number = State()


class FSMChangeAquariumNumber(StatesGroup):
    fill_aquarium_id = State()
    fill_old_number = State()
    fill_new_number = State()


class FSCMQuestionInsert(StatesGroup):
    fill_animal_callback = State()
    fill_question = State()
    fill_answer_choice = State()
    fill_answer = State()
    fill_correct_answer = State()
    fill_correct_callback = State()
    fill_wrong_answer_choice = State()
    fill_wrong_answer = State()
    fill_wrong_callback = State()


class FSMUpdateAnimal(StatesGroup):
    fill_animal_name = State()
    fill_answer_choice = State()
    fill_description = State()
    upload_photo = State()
    fill_name = State()
    upload_audio = State()


class FSMDeleteQuestion(StatesGroup):
    fill_animal_name = State()
