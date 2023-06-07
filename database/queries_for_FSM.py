from database.database_class import DataBaseClass

DataBase = DataBaseClass()


async def insert_animals(animal: tuple) -> int:
    return await DataBase.execute(f'''INSERT INTO animals (name, description, photo_id, callback) \
    VALUES {animal}''', execute=True)


async def insert_aq_an(aq_aq: tuple) -> int:
    return await DataBase.execute(f'''INSERT INTO aquarium_animals(animal_id, aq_number) \
    VALUES {aq_aq}''', execute=True)


async def update_aquarium_photo(an_aq: tuple) -> int:
    return await DataBase.execute('''UPDATE aquariums \
    SET photo_id= $1 WHERE aq_number= $2''',
                                  *an_aq, execute=True)


async def animal_db() -> str:
    animal = await DataBase.execute('''SELECT MAX(animal_id) FROM animals''',
                                    fetchval=True)
    return animal


async def add_question_without_answers(qt: tuple) -> int:
    return await DataBase.execute('''INSERT INTO questions \
    (animal_id, callback_name, question) \
    VALUES($1, $2, $3)''', *qt, execute=True)


async def add_question_with_one_answer(qt: tuple) -> int:
    return await DataBase.execute('''INSERT INTO questions \
    (animal_id, callback_name, question, keyboard, answer_yes, cb_yes) \
    VALUES($1, $2, $3, $4, $5, $6)''', *qt, execute=True)


async def add_question_with_two_answer(qt: tuple) -> int:
    return await DataBase.execute('''INSERT INTO questions \
    (animal_id, callback_name, question, keyboard, answer_yes, cb_yes, answer_no, cb_no) \
    VALUES($1, $2, $3, $4, $5, $6, $7, $8)''', *qt, execute=True)


async def add_question(qt: tuple) -> int:
    return await DataBase.execute('''INSERT INTO questions \
    (animal_id, callback_name, question, keyboard, answer_yes, cb_yes, answer_no, cb_no, answer_no_2, cb_no_2) \
    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)''', *qt, execute=True)


async def animal_id_by_callback(cb: str) -> str:
    animal = await DataBase.execute('''SELECT animal_id FROM animals\
     WHERE callback= $1''', cb, fetchval=True)
    return animal


async def animal_id_by_name(cb: str) -> str:
    animal = await DataBase.execute('''SELECT animal_id FROM animals\
     WHERE name= $1''', cb, fetchval=True)
    return animal


async def del_animal_from_aq(dl: tuple) -> int:
    animal = await DataBase.execute('''DELETE FROM aquarium_animals\
     WHERE aq_number= $1 AND animal_id = $2''', *dl, execute=True)
    return animal


async def ins_animal_into_aq(ins: tuple) -> int:
    animal = await DataBase.execute('''INSERT INTO aquarium_animals \
     (animal_id, aq_number) VALUES($1, $2)''', *ins, execute=True)
    return animal


async def update_animal_name(ins: tuple) -> int:
    return await DataBase.execute('''UPDATE animals \
    SET name= $2 WHERE animal_id= $1''',
                                  *ins, execute=True)


async def update_animal_description(ins: tuple) -> int:
    return await DataBase.execute('''UPDATE animals \
    SET description= $2 WHERE callback= $1''',
                                  *ins, execute=True)


async def update_animal_photo(ins: tuple) -> int:
    return await DataBase.execute('''UPDATE animals \
    SET photo_id= $2 WHERE callback= $1''',
                                  *ins, execute=True)


async def update_animal_audio(ins: tuple) -> int:
    return await DataBase.execute('''UPDATE animals \
    SET audio_id= $2 WHERE callback= $1''',
                                  *ins, execute=True)


async def insert_new_aquarium(aq_aq: tuple) -> int:
    return await DataBase.execute(f'''INSERT INTO aquariums(aq_number) \
    VALUES ($1)''', *aq_aq, execute=True)


async def change_aquarium_number(ins: tuple) -> int:
    return await DataBase.execute('''UPDATE aquariums \
    SET aq_number= $2 WHERE aq_id= $1''',
                                  *ins, execute=True)


async def animal_ids_from_aquarium(cb: int) -> list:
    ups = await DataBase.execute('''SELECT animal_id FROM aquarium_animals\
     WHERE aq_number= $1''', cb, fetch=True)
    animal = []
    for i in ups:
        animal.append(i[0])
    return animal


async def change_aq_number_for_animals(animals: list) -> None:
    return await DataBase.execute(f'''UPDATE aquarium_animals \
    SET aq_number= $1 WHERE animal_id= $2''', animals, executemany=True)


async def del_question_from_aq(cb_n: tuple) -> int:
    return await DataBase.execute('''DELETE FROM questions\
     WHERE callback_name= $1''', cb_n, execute=True)

