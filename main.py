import telebot
from PIL import Image, ImageDraw, ImageFont

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)

default_paper_size = (40, 34)
px_in_px = 40
threshold = 100


class Img:
    def __init__(self, image_src=None):
        self.image_src = image_src
        self.image = Image.open('pic.jpg')

    def re(self):
        self.image = self.image.resize(default_paper_size, resample=Image.NONE)
        for left in range(self.image.size[0]):
            for up in range(self.image.size[1]):
                self.image.putpixel((left, up),
                                    (0, 0, 0) if sum(self.image.getpixel((left, up))) // 3 < threshold else (255, 255, 255))
        self.image = self.image.resize((default_paper_size[0] * px_in_px, default_paper_size[1] * px_in_px),
                                       resample=Image.NONE)
        self.image.save('out.jpg')
        self.image.show()


x = Img()
x.re()


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


@bot.message_handler(content_types=['text'])
def _other(message):
    bot.send_message(message.chat.id, 'Я вас не понимаю. Помощь - /help')
    # find(message.text.upper())
    # with open('out.png', 'rb') as photo:
    #     bot.send_photo(message.chat.id, photo)


bot.polling()
