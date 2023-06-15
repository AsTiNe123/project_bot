from aiogram import Bot, Dispatcher, types, executor

import asyncio

from contextlib import suppress

import datetime

from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from env import TOKEN

import scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from Func import make, check, rules

from keybords import answer


COMAND = """
/start
/get_score
/change_time
/answer
/rules
"""

scheduler = AsyncIOScheduler()

bot = Bot(token= TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()

async def skipping_task(message: types.Message, sleep_time: int, state:FSMContext):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        data = state.get_data()
        if data["state"] == 1:
            data = await state.get_data()
            score = int(data['score'])-2
            await state.update_data({'score' : score})
            await message.edit_text("Ты пропустирл задание и из-за этого потерял 2 очка")


async def start_scheduler(tt, state: FSMContext):
    if not tt:
        data = await state.get_data()
        morning_time: datetime.time = data["morning_time"]
        night_time: datetime.time = data["night_time"]
        scheduler.add_job(scheduler_morning, 
                          trigger = 'cron', 
                          hour=morning_time.hour, 
                          minute=morning_time.minute, 
                          args= [state])
        scheduler.add_job(send_words, 
                          trigger = 'cron', 
                          hour=f"{morning_time.hour}-{night_time.hour}/2", 
                          minute=f"{int(morning_time.minute)+1}{int(morning_time.minute)+10}/0.5", 
                          args= [state])
        scheduler.add_job(scheduler_night, 
                          trigger = "cron", 
                          hour=night_time.hour, 
                          minute=night_time.minute,
                          args= [state])
        scheduler.start()




async def scheduler_morning(state: FSMContext):
    data = await state.get_data()
    list_of_words = make(str(data['last_word']),data['mistake_words'])
    await state.update_data({'today_words':list_of_words})
    await state.update_data({'last_word':list_of_words[4]})
    await state.update_data({'today_result':{list_of_words[0]:0, list_of_words[1]:0, list_of_words[2]:0, list_of_words[3]:0, list_of_words[4]:0}})
    list_of_words2 = "\n".join(list_of_words)
    await bot.send_message(data["chat_id"], "сегодня мы учим слова:\n"+list_of_words2)

async def send_words(state: FSMContext):
    data = await state.get_data()
    today_result = data["today_result"]
    words = data["today_words"]
    words = set(tuple(words))
    today_result2 = {}
    for i in words:
        today_result2[i] = today_result[i]
    await state.update_data({"today_words":words, "today_result":today_result2})
    words_end = "Переведи слова:\n"
    if data['state'] == 'Eng':
        for i in words:
            word = str(i.split(" - ")[0])
            words_end = words_end + word + "\n"
            await state.update_data({'state': "Rus"})
    else:
        for i in words:
            word = str(i.split(" - ")[1])
            words_end = words_end + word + " - \n"
            await state.update_data({'state': "Eng"})
    msg = await bot.send_message(data["chat_id"], words_end)
    asyncio.create_task(skipping_task(msg, 45, state))
    await state.update_data({'state': 1})
    
    await state.set_data("q4")

async def scheduler_night(state: FSMContext):
    data = await state.get_data()
    mistake_words = []
    today_result:dict = data["today_result"]
    for i in range(5):
        if today_result.values()[i] < 3:
            mistake_words.append(''.join(data["today_words"][i]))
    else:
        await state.update_data({'mistake_words':mistake_words})


@dp.message_handler(commands= ["help"], state= '*')
async def help(message: types.Message):
    await message.answer(text = COMAND)


@dp.message_handler(commands= ["rules"], state= '*')
async def get_rules(message: types.Message):
    await rules(message)

@dp.message_handler(commands= ["get_score"], state= '*')
async def score(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"your score: {data['score']}")

@dp.message_handler(commands= ["change_time"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 22:00)")
    await state.set_state("q1")


@dp.message_handler(commands= ["start"], state= '*')
async def echo(message: types.Message, state: FSMContext):
    await message.answer(text = "Привет это обычный бот, который обязательно поможет тебе выучить фразовые глаголы в английском языке.", reply_markup=answer)
    await message.answer(text = "Во сколько ты примерно ложишса спать(например 22:00)")
    await state.update_data({'user': message.from_user.full_name, 'chat_id': message.from_user.id})
    await state.set_state("q1")


@dp.message_handler(state= "q1")
async def night_time(message: types.Message, state: FSMContext):
    night_time = message.text
    try:
        night_time = datetime.time(*map(int, night_time.split(":")))
        await state.update_data({"night_time": night_time})
        await message.answer(text = "Теперь напиши время, когда ты просыпаешся(например 7:00)")
        await state.set_state("q2")
    except Exception:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 22:00)", parse_mode = "HTML")
    
@dp.message_handler(state= "q2")
async def morning_time(message: types.Message, state: FSMContext):
    morning_time = message.text
    try:
        morning_time = datetime.time(*map(int, morning_time.split(":")))
        await state.update_data({"morning_time": morning_time})
        data = await state.get_data()
        
        if 'score' not in data.keys():
            await state.update_data({"score": 0})
        if 'state' not in data.keys():
            await state.update_data({'state': 0})
        await start_scheduler(0, state)
        await state.update_data({'last_word':'0'})
        await state.update_data({'today_result':{'0':0, '0':0, '0':0, '0':0,'0':0}})
        await state.update_data({'mistake_words':[]})
        await state.update_data({'state':"Eng"})
        night_time = data["night_time"]
        if datetime.datetime.now().time() > morning_time and datetime.datetime.now().time()< night_time:
            await scheduler_morning(state)
        await rules(message)    
        await message.answer(text = "Всё, ты закончил регистрацию")     
        await state.set_state("q4") 
    except:
        await message.answer(text = "Ты не правильно ввёл время(<i><b>ПРИМЕР</b></i> 7:00)", parse_mode = "HTML")

@dp.message_handler(state = 'q4')
async def echo(message: types.Message, state: FSMContext):
    answer = message.text.split('\n')
    asyncio.create_task(delete_message(message, 45))
    while len(answer)<5:
        answer.append('-')
    data = await state.get_data()
    today_result:dict = data["today_result"]
    today_words = data["today_words"]
    score = data["score"]
    result = check(answer[:], today_words)
    to_send = ''
    for i in range(5):
        res = result[i]
        if res:
            score+=1
            today_result[today_words[i]]+1
            to_send += "правильно\n" 
        else:
            score -= 1
            to_send += "неправильно\n" 
    await state.update_data({"today_result": today_result})
    ms = await message.answer("твои результаты:\n"+to_send)
    asyncio.create_task(delete_message(ms, 45))
    await state.update_data({'state': 0})

@dp.message_handler(state = '*')
async def ketboard(message: types.Message, state: FSMContext):
    if message.text == "Инструкция":
        await rules(message)
    elif message.text == "Список команд":
        await help(message)
    elif message.text == "Мой счёт":
        await score(message)
    elif message.text == "Слова сегодня":
        data = await state.get_data()
        list_of_words = data["today_words"]
        list_of_words2 = "/n".join(list_of_words)
        await bot.send_message(data["chat_id"], "сегодня мы учим слова:\n"+list_of_words2)


    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)