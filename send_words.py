from aiogram import types

def make(last_word:str, mistake_words:list ):
    sending_words = mistake_words
    with open('list_of_words.txt', "r", encoding= "utf-8") as file:
        file = file.readlines()
        f = [i[:len(i)-1] for i in file]

    
    index = f.index(last_word)+1
    while len(sending_words) <5 and index != len(f):
        sending_words.append(f[index])
        index+=1
    return sending_words

def check(answers, today_words):
    result = []
    answer = answers[0]
    liter = "qwertyuiopasdfghjklzxcvbnm"
    if answer[0] not in liter:
        for i in range(5):
            word = today_words[i]
            word = tuple(word.split(" - ")[1].split(", "))
            answer = tuple(answers[i].split(", "))
            
            if set(word) == set(answer):
                result.append(1)
            else:
                result.append(0)
    else:
        for i in range(5):
            word = today_words[i]
            word = tuple(word.split(" - ")[0].split(", "))
            answer = tuple(answers[i].split(", "))
            print(set(word), set(answer), sep = "rgwh")
            if set(word) == set(answer):
                
                result.append(1)
            else:
                result.append(0)
    return result

async def rules(message: types.Message):
    example_send = "Переведи слова:\nburst out \ncome across\nknock down\nlet down\nlook after"
    example_answer = "вспыхнуть, воскликнуть\nповстречаться, натолкнуться\nсбить, свалить, снести\nпускать, ослабить, разочаровать\nухаживать, присмотреть, проследить"
    await message.answer("<b><i>Инструкция</i></b>", parse_mode = "HTML")
    await message.answer("Каждый день и каждый час, когда ты не спишь, этот бот тебе будет отправлять слова который ты должен перевести. Ведётся счёт слов которые ты перевёл неправильно, и если ты смог перевести фразовый глагол только 2 раза за целый день тебе придётся учить это слово и на следующий день. За Правильный ответ тебе даётся 1 балл, за неправильный вычитается 1 балл, за пропуск задания вычитается 2 балла. Ты можешь посмотреть сколько у тебя баллов с помощью команды /get_score.")
    await message.answer(f"тебе будут приходить сообщения такого типа(русский и английские слова для перевода будут чередоваться):\n{example_send}")
    await message.answer(f"тебе нужно ввести команду /answer и после этого на отдельных строчках написать все переводы(варианты перевода записывать в разном порядке), а если ты не знаешь перевод напиши '-'. Вот пример:\n{example_answer}")
