# Модуль с запросами к базе данных, которые используются в хэндлерах
from database.database_class import DataBaseClass


DataBase = DataBaseClass()


# Эта функция по номеру аквариума, полученному от пользователя,
# отправляет запрос в базу данных и формирует список с callback
# каждого обитателя аквариума для создания клавиатуры
async def buttons_for_keyboard(aq_nb: str) -> list:
    result = await DataBase.execute('''SELECT callback FROM animals \
                         INNER JOIN aquarium_animals USING(animal_id) \
                         WHERE aq_number = $1 \
                         ORDER BY animal_id''', int(aq_nb), fetch=True)
    button_list = []
    for i in result:
        button_list.append(i[0])
    return button_list


# Эта функция по номеру аквариума, полученному от пользователя,
# отправляет запрос в базу данных иформирует список с photo_id
# аквариума, для получения коллажа с обитателями
async def photo_collage(aq_nb: str) -> str:
    result = await DataBase.execute('''SELECT photo_id FROM aquariums \
                         WHERE aq_number = $1''', int(aq_nb), fetchval=True)

    return result


# Эта функция по callback, полученному от пользователя,
# отправляет запрос в базу данных и формирует список с
# названием, описанием и photo_id выбранного животного
async def animal_from_db(cb: str) -> list:
    result = await DataBase.execute('''SELECT name, description, photo_id, audio_id FROM animals \
                         WHERE callback= $1 \
                         ORDER BY name''', cb, fetchrow=True)
    animal = []
    for x in result:
        animal.append(x)
    return animal


# Эта функция отправляет запрос в базу данных по callback.data
# и формирует список ответов для кнопок клавиатуры
# для животного с дополнительными вопросами и ответами
async def answers_from_db(cb: str) -> list:
    result = await DataBase.execute('''SELECT keyboard FROM questions \
                             WHERE callback_name= $1''', cb, fetchval=True)
    animal = result.split(':')
    return animal


# Эта функция отправляет запрос в базу данных по callback.data
# и формирует список ответов для кнопок клавиатуры
# для животного с дополнительными вопросами и ответами
async def keyboard_from_db_questions(cb: str) -> list:
    result = await DataBase.execute('''SELECT cb_yes, cb_no, cb_no_2 FROM questions \
                             WHERE callback_name= $1 ''', cb, fetchrow=True)
    animal = []
    for i in result:
        animal.append(i)
    return animal


# Эта функция отправляет запрос в базу данных по callback.data
# и возвращает положительный ответ на вопрос
# для животного с дополнительными вопросами и ответами
async def answer_yes_from_db(cb: str) -> str:
    result = await DataBase.execute('''SELECT answer_yes FROM questions \
                             WHERE cb_yes= $1''', cb, fetchval=True)
    return result


# Эта функция отправляет запрос в базу данных по callback.data
# и возвращает неправильный ответ на вопрос
# для животного с дополнительными вопросами и ответами
async def answer_no_from_db(cb: str) -> str:
    result = await DataBase.execute('''SELECT answer_no FROM questions \
                             WHERE cb_no= $1''', cb, fetchval=True)
    return result


# Эта функция отправляет запрос в базу данных по callback.data
# и возвращает второй неправильный ответ на вопрос
# для животного с дополнительными вопросами и ответами
async def answer_no_2_from_db(cb: str) -> str:
    result = await DataBase.execute('''SELECT answer_no_2 FROM questions \
                             WHERE cb_no_2= $1''', cb, fetchval=True)
    return result


# Эта функция отправляет запрос в базу данных по callback.data
# и возвращает вопрос
# для животного с дополнительными вопросами
async def question_from_db(cb: str) -> str:
    result = await DataBase.execute('''SELECT question FROM questions \
                             WHERE callback_name= $1''', cb, fetchval=True)
    return result
