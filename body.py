from aiogram import Bot, Dispatcher, types, executor

from env import TOKEN

import aioschedule 
from apscheduler.schedulers.background import BackgroundScheduler

import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import datetime

from send_words import make, check

today_result = [0, 0, 0, 0, 0]

mistake_words = []

last_word = 'back off - отстраниться, пойти на попятный, отступить'

COMAND = """
/start
/get_score
/change_time
"""

scheduler = BackgroundScheduler()

bot = Bot(token= TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
scheduler.add_job(make, trigger = "interval", args = [bot, ], )

async def scheduler_morning(state: FSMContext):
    data = state.get_data()
    if datetime.datetime.now() > data["time_on"]:
        global today_result
        list = aioschedule.every().day.do(make, last_word, mistake_words)
        state.update_data({'today_words':list})
        last_word = list[4]
        today_result = [0, 0, 0, 0, 0]

async def scheduler_night(state: FSMContext):
    data = state.get_data()
    h , m = map(int, data["time_out"].split(":"))
    if data["time_out"]>15:
        if datetime.datetime.now().time().hour >= h and datetime.datetime.now().time().minute >= m:
            data = state.get_data()
            for i in range(5):
                if today_result[i] < 3:
                    mistake_words += data["today_words"]
    else:
        if datetime.datetime.now().time().hour >= h and datetime.datetime.now().time().minute >= m and datetime.datetime.now().time()<15:
            data = state.get_data()
            for i in range(5):
                if today_result[i] < 3:
                    mistake_words += data["today_words"]

    
async def scheduler(state: FSMContext):
    data = state.get_data()
    if datetime.datetime.now() > data["time_out"]:
        list = aioschedule.every().day.do(make, bot, last_word)
        state.update_data({'today_words':list})
        last_word = list[4]

@dp.message_handler(commands= ["help"], state= '*')
async def echo(message: types.Message):
    await message.answer(text = COMAND)

@dp.message_handler(commands= ["get_score"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"your score: {data['score']}")

@dp.message_handler(commands= ["change_time"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 22:00)")
    await state.set_state("q1")

@dp.message_handler(commands= ["start"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Привет это обычный бот, который обязательно поможет тебе выучить фразовые глаголы в английском языке.")
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 22:00)")
    await state.update_data({'user': message.from_user.full_name})
    await state.set_state("q1")
    

@dp.message_handler(state= "q1")
async def set_age(message: types.Message, state: FSMContext):
    time_out = message.text
    try:
        await state.update_data({"night_time": time_out})
        await message.answer(text = "Теперь напиши время, когда ты просыпаешся(например 7:00)")
        await state.set_state("q2")
    except Exception:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 7:00)", parse_mode = "HTML")
    
@dp.message_handler(state= "q2")
async def set_age(message: types.Message, state: FSMContext):
    time_on = str(message.text)
    data = await state.get_data()
    try:
        await state.update_data({"morning_time": time_on})
        await message.answer(text = "Всё, ты закончил регистрацию")
        await state.set_state("q3")
        if 'score' not in data.keys():
            await state.update_data({"score": 0})
    except Exception:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 22:00)", parse_mode = "HTML")
    print(await state.get_data())

@dp.message_handler(state = 'q3')
async def echo(message: types.Message, state: FSMContext):
    text = message.text.split('\n')
    if text[0] == '':
        global today_result
        data = await state.get_data()
        score = data["score"]
        result = check()
        for i in range(5):
            res = result[i]
            if i:
                score+=1
                today_result[i]+1
            else:
                score -= 1







if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)