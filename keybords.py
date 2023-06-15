from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

help= KeyboardButton("Инструкция")
comand = KeyboardButton("Список команд")
score = KeyboardButton("Мой счёт")
today_words = KeyboardButton("Слова сегодня")



answer = ReplyKeyboardMarkup(resize_keyboard = True).row(help, comand, score, today_words)