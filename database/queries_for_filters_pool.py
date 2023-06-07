# Модуль с запросами к базе данных, которые используются в фильтрах

from database.database_class import DataBaseClass


DataBase = DataBaseClass()


# Эта функция отправляет запрос в базу данных и формирует
# список callback всех животных из базы
async def all_animal_cb() -> list:
    result = await DataBase.execute('''SELECT callback FROM animals''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список callback_name всех животных из базы, которым есть
# дополнительные вопросы
async def special_animal_without_answer() -> list:
    result = await DataBase.execute('''SELECT callback_name FROM questions''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список callback_name всех животных из базы, которым есть
# дополнительные вопросы c ответами
async def special_animal_with_answer() -> list:
    result = await DataBase.execute('''SELECT callback_name FROM questions WHERE
                    keyboard IS NOT NULL''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список правильных ответов всех животных из базы, к которым есть
# дополнительные вопросы c ответами
async def yes_answers() -> list:
    result = await DataBase.execute('''SELECT cb_yes FROM questions WHERE
                    keyboard IS NOT NULL''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список неправильных ответов всех животных из базы, к которым есть
# дополнительные вопросы c ответами
async def no_answers() -> list:
    result = await DataBase.execute('''SELECT cb_no FROM questions WHERE
                    keyboard IS NOT NULL''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список неправильных ответов всех животных из базы, к которым есть
# дополнительные вопросы c ответами
async def no_2_answers() -> list:
    result = await DataBase.execute('''SELECT cb_no_2 FROM questions WHERE
                    keyboard IS NOT NULL''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список callback всех животных из базы
async def all_animal_name() -> list:
    result = await DataBase.execute('''SELECT name FROM animals''', fetch=True)
    animal = []
    for i in result:
        animal.append(i[0])
    return animal


# Эта функция отправляет запрос в базу данных и формирует
# список номеров всех аквариумов в базе
async def all_aquarium_numbers() -> list:
    result = await DataBase.execute('''SELECT aq_number FROM aquariums''', fetch=True)
    aquariums = []
    for i in result:
        aquariums.append(str(i[0]))
    return aquariums
