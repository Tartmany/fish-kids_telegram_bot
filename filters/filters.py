# Модуль с фильтрами для хэндлеров
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
import database


class AnimalInQuestionWithAnswer(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        all_animal = await database.special_animal_with_answer()
        return callback.data in all_animal


class AnimalInQuestions(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        all_animal = await database.special_animal_without_answer()
        return callback.data in all_animal


class AnimalInAnimals(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        all_animal = await database.all_animal_cb()
        return callback.data in all_animal


class AnswerInYesAnswers(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        all_animal = await database.yes_answers()
        return callback.data in all_animal


class AnswerInNoAnswers(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        all_animal = await database.no_answers()
        return callback.data in all_animal


class AnimalInAnimalsMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        all_animal = await database.all_animal_cb()
        return message.text in all_animal


class AnimalInAnimalNames(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        all_animal = await database.all_animal_name()
        return message.text in all_animal


class NumberInAquariumNumbers(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        all_aquariums = await database.all_aquarium_numbers()
        return message.text in all_aquariums


class AnimalInQuestionsMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        all_animal = await database.special_animal_without_answer()
        return message.text in all_animal
