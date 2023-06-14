from aiogram import types

async def send_words(message: types.Message, last_word_number, mistake_words = []):
    sending_words = mistake_words
    with open('lisst_of_words.txt') as file:
        file = file.readlines()
        f = [i for i in file.split()]
    index = await f.index(last_word_number)+1
    while len(sending_words)!= 5 or index != len(f):
        sending_words += [f[index]]
        index+=1
    await message.answer()

#async def 