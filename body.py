from aiogram import Bot, Dispatcher, types, executor

from json import *

from env import TOKEN

from User_class import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

COMAND = """
/start
"""
User = Person()

bot = Bot(token= TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

@dp.message_handler(commands= ["help"], state= '*')
async def echo(message: types.Message):
    await message.answer(text = COMAND)

@dp.message_handler(commands= ["get_score"], state= '*')
async def echo(message: types.Message):
    await message.answer(User.get_score())

@dp.message_handler(commands= ["change_time"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 7:00)")
    await state.set_state("q1")

@dp.message_handler(commands= ["start"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Привет это обычный бот, который обязательно поможет тебе выучить фразовые глаголы в английском языке.")
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 7:00)")
    await state.set_state("q1")
    

@dp.message_handler(state= "q1")
async def set_age(message: types.Message, state: FSMContext):
    time_out = message.text
    h, m = time_out.split(":")
    if h.isdigit() and m.isdigit():
            await state.update_data({"night_time": time_out, "score": 0})
            await message.answer(text = "Теперь напиши время, когда ты просыпаешся(например 22:00)")
            await state.set_state("q2")
    else:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 7:00)", parse_mode = "HTML")
    
@dp.message_handler(state= "q2")
async def set_age(message: types.Message, state: FSMContext):
    time_on = message.text
    h, m = time_on.split(":")
    time_out = state.get_data('night_time')
    if User != '' and h.isdigit() and m.isdigit():
        User.change_time([h, m])
    elif h.isdigit() and m.isdigit():
        await state.update_data({"morning_time": time_on})
        User = Person.set_data(message.from_user.full_name, [h, m], list(map(int, time_out.split(":"))), 0)
        await message.answer(text = "Всё, ты закончил регистрацию")
        await state.set_state("q3")
    else:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 22:00)", parse_mode = "HTML")
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)