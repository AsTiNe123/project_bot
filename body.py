from aiogram import Bot, Dispatcher, types, executor


from env import TOKEN

from User_class import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import datetime

COMAND = """
/start
"""
bot = Bot(token= TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

@dp.message_handler(commands= ["help"], state= '*')
async def echo(message: types.Message):
    await message.answer(text = COMAND)

@dp.message_handler(commands= ["get_score"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(data['user'].get_score())

@dp.message_handler(commands= ["change_time"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 7:00)")
    await state.set_state("q1")

@dp.message_handler(commands= ["start"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Привет это обычный бот, который обязательно поможет тебе выучить фразовые глаголы в английском языке.")
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 7:00)")
    await state.update_data({'user': Person()})
    await state.set_state("q1")
    

@dp.message_handler(state= "q1")
async def set_age(message: types.Message, state: FSMContext):
    time_out = message.text
    h, m = time_out.split(":")
    if h.isdigit() and m.isdigit():
            await state.update_data({"night_time": time_out})
            await message.answer(text = "Теперь напиши время, когда ты просыпаешся(например 22:00)")
            await state.set_state("q2")
    else:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 7:00)", parse_mode = "HTML")
    
@dp.message_handler(state= "q2")
async def set_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = data['user']
    time_on = str(message.text)
    #try:
    time_dt_on = datetime.datetime.strptime(time_on, "%H:%M").time()
    time_out = data['night_time']
    time_dt_out = datetime.datetime.strptime(time_out, "%H:%M").time()
    if not user.nole():
        user.change_time(time_dt_on, time_dt_out)   
    else:
        await state.update_data({"morning_time": time_on})
        user.set_data(message.from_user.full_name, time_dt_on, time_dt_out)
        await message.answer(text = "Всё, ты закончил регистрацию")
        await state.set_state("q3")
    #except Exception:
     #   print()
    #    await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 22:00)", parse_mode = "HTML")
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)