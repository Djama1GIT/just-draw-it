import datetime

import telebot
from image_reconstructor import Img
import db

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)

try:
    @bot.message_handler(commands=['start'])
    def _start(message):
        msg = """
        Скорее отправляй фото!
    Хочешь узнать как будет происходить процесс рисования? Используй команду /help
        """
        bot.send_message(message.chat.id, msg)


    @bot.message_handler(commands=['help'])
    def _help(message):
        msg = """
        Итак. Всё на самом деле просто!
    Ты отправляешь мне фото - я предлагаю варианты рисования - ты выбираешь понравившийся и мы вместе рисуем! Готово!
        """
        bot.send_message(message.chat.id, msg)


    @bot.message_handler(content_types=['photo'])
    def _photo(message):
        photo = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
        Img(photo, message.photo[-1].file_id, (40, 34), 1.1).reconstruct()
        with open(f'temp/{message.photo[-1].file_id}.png', "rb") as _new_photo:
            bot.send_photo(message.chat.id, _new_photo)


    def _other(message):
        bot.send_message(message.chat.id, 'Я вас не понимаю. Помощь - /help')


    if __name__ == '__main__':
        bot.polling(none_stop=True)
except Exception as e:
    with open('log.txt', 'a') as log:
        err = f'[{datetime.datetime.now()}] BOT Error {e} | Arguments: {e.args}\n'
        print(err)
        log.write(err)
finally:
    if __name__ == '__main__':
        bot.polling(none_stop=True)