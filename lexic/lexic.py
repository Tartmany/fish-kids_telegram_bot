LEXICON: dict[str, str] = {
    '/start': '<b>Привет!</b>\n\nЯ - бот, от которого вы можете узнать '
              'самую интересную информацию об обитателях аквариумов '
              'Санкт-Петербургского Океанариума.\n\n'
              'Моя информация адаптирована для детей, чтобы каждый маленький '
              'почемучка мог получить ответ на вопрос:\n'
              '"Ой, а кто - это?"\n\nНо, думаю, '
              'и взрослые могут открыть для себя что-нибудь интересное 😉\n\n'
              'Если тебя заинтересует какое-то животное,\n'
              '<b>- набери</b> цифрой номер аквариума, в котором оно живет;\n'
              '<b>- выбери</b> на картинке нужное животное;\n'
              '<b>- нажми</b> кнопку с соответствующей цифрой под фотографией;\n'
              '<b>- читай</b> самый интересный факт о выбранном животном!\n\n'
              'Чтобы вернуться к списку животных аквариума, снова набери номер аквариума\n\n'
              'Чтобы узнать, как выглядит номер аквариума, набери '
              'команду /help.\n\n'
              'Чтобы узнать, кого из обитателей сегодня будут кормить,'
              ' набери команду /feedings.\n\n<b>Приятной прогулки!</b>',
    '/help': '<b>Вот так выглядит номер аквариума</b>',
    '/feedings': 'Расписание кормлений можно посмотреть <a href="океанариум.рф/shows/">здесь</a>',
    '/feedback': '<b>Мы еще не придумали, где хотим собирать отзывы </b> :)',
    'photo_id1': 'AgACAgIAAxkBAAIBCGQeqZlTyJCMrJ_DLpFN8Ij3ulKAAALWxjEbRL35SBkCGSASdNCWAQADAgADcwADLwQ'
    }

LEXICON_ADMIN: dict[str, str] = {
    'add_new_animal': 'Добавить новое животное',
    'add_animal': 'Добавить животное из базы в аквариум',
    'del_animal': 'Убрать животное из аквариума',
    'update_aquarium_photo': 'Поменять фотоколлаж аквариума',
    'update_animal_info': 'Изменить информацию о животном',
    'add_question': 'Добавить вопрос',
    'delete_question': 'Удалить вопрос',
    'add_aquarium': 'Добавить новый аквариум',
    'change_aquarium_number': 'Изменить номер аквариума',
    'load_data': 'Загрузить статистику',
    'delete_update_data': 'Очистить статисктику апдейтов'
    }

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Что умеет этот бот?',
    '/help': 'Как выглядит номер аквариума?',
    '/feedings': 'Расписание кормлений',
    '/feedback': 'Оставьте свой отзыв о боте'
    }
