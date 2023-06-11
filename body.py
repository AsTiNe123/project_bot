from aiogram import Bot, Dispatcher, types, executor

from json import *

from env import TOKEN

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

COMAND = """
/start
"""


bot = Bot(token= TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

@dp.message_handler(commands= ["help"], state= '*')
async def echo(message: types.Message):
    await message.answer(text = COMAND)

@dp.message_handler(commands= ["start"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Привет это обычный бот, который обязательно поможет тебе выучить фразовые глаголы в английском языке.\n Как тебя зовут")
    await state.set_state("q1")

@dp.message_handler(state= "q1")
async def set_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name, "score": 0})
    await state.set_state("q2")

    await message.answer(text = "Сколько во сколько ты примерно ложишса спать")

@dp.message_handler(state= "q2")
async def set_age(message: types.Message, state: FSMContext):
    time = message.text
    if age.isdigit():
            await state.update_data({"night_time": time, "score": 0})
            await message.answer(text = "Теперь напиши время, когда ты просыпаешся")
            await state.set_state("q3")
    else:
        await message.answer(text = "Это не число. Попробуй ещё раз.")
    await message.answer(text = "Всё ты закон")
    
@dp.message_handler(state= "q3")
async def set_age(message: types.Message, state: FSMContext):
    time = message.text
    if age.isdigit():
            await state.update_data({"morning_time": time})
            await message.answer(text = "Теперь напиши время, когда ты просыпаешся")
            await state.set_state("q3")
    else:
        await message.answer(text = "Это не число. Попробуй ещё раз.")
    await message.answer(text = "Всё ты закон")