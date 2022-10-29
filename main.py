import telebot
from PIL import Image, ImageDraw, ImageFont

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def _start(message):
    msg = """
    Скорее отправляй фото!\nХочешь узнать как будет происходить процесс рисования? Используй команду /help
    """
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['help'])
def _help(message):
    msg = """
    123
    """
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text'])
def _other(message):
    bot.send_message(message.chat.id, 'Я вас не понимаю. Помощь - /help')
    # find(message.text.upper())
    # with open('out.png', 'rb') as photo:
    #     bot.send_photo(message.chat.id, photo)


bot.polling()
