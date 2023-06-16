from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

help= KeyboardButton("Инструкция")
comand = KeyboardButton("Список команд")
score = KeyboardButton("Мой счёт")
today_words = KeyboardButton("Слова сегодня")
today_result = KeyboardButton("Мой сегодняшний результат")



answer = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 4).add(help, comand, score, today_words, today_result)
