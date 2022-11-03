import telebot
from PIL import Image, ImageDraw, ImageFont

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)

default_paper_size = (40 * 3, 34 * 3)
px_in_px = 20
paper_size = (default_paper_size[0] * px_in_px, default_paper_size[1] * px_in_px)
threshold = 35  # нужно сделать автоматическое определение чувствительности через среднюю яркость на фото


class Img:
    def __init__(self, image_src=None):
        self.image_src = image_src
        self.image = Image.open('img_1.png')
        # if self.image.size[1] > self.image.size[0]:
        #     global default_paper_size
        #     default_paper_size = (default_paper_size[1], default_paper_size[0])

    def re(self):
        background = Image.new('RGB', default_paper_size)
        background.paste((255, 255, 255), [0, 0, background.size[0], background.size[1]])
        if self.image.size[1] > self.image.size[0]:
            self.image = self.image.resize(
                (int(self.image.size[0] * (default_paper_size[1] / self.image.size[1])),
                 int(self.image.size[1] * (default_paper_size[1] / self.image.size[1]))),
                resample=Image.BOX)
        else:
            self.image = self.image.resize(
                (int(self.image.size[0] * (default_paper_size[0] / self.image.size[0])),
                 int(self.image.size[1] * (default_paper_size[0] / self.image.size[0]))),
                resample=Image.BOX)
        for left in range(self.image.size[0]):
            for up in range(self.image.size[1]):
                self.image.putpixel((left, up),
                                    (0, 0, 0) if sum(self.image.getpixel((left, up))) // 3 < threshold else (
                                        255, 255, 255))
        for left in range(1, self.image.size[0] - 1):
            for up in range(1, self.image.size[1] - 1):
                if self.image.getpixel((left, up)) == (0, 0, 0):
                    if self.image.getpixel((left - 1, up)) == (255, 255, 255) \
                            and self.image.getpixel((left + 1, up)) == (255, 255, 255) \
                            and self.image.getpixel((left, up - 1)) == (255, 255, 255) \
                            and self.image.getpixel((left, up + 1)) == (255, 255, 255):
                        self.image.putpixel((left, up), (255, 255, 255))
        if self.image.size[1] > self.image.size[0]:
            background.paste(self.image, ((background.size[0] - self.image.size[0]) // 2, 0))
        else:
            background.paste(self.image, (0, (background.size[1] - self.image.size[1]) // 2))
        background = background.resize(paper_size, resample=Image.NONE)
        background.save('out.jpg')
        background.show()


x = Img()
x.re()
#
#
# @bot.message_handler(commands=['start'])
# def _start(message):
#     msg = """
#     Скорее отправляй фото!
# Хочешь узнать как будет происходить процесс рисования? Используй команду /help
#     """
#     bot.send_message(message.chat.id, msg)
#
#
# @bot.message_handler(commands=['help'])
# def _help(message):
#     msg = """
#     Итак. Всё на самом деле просто!
# Ты отправляешь мне фото - я предлагаю варианты рисования - ты выбираешь понравившийся и мы вместе рисуем! Готово!
#     """
#     bot.send_message(message.chat.id, msg)
#
#
# @bot.message_handler(content_types=['text'])
# def _other(message):
#     bot.send_message(message.chat.id, 'Я вас не понимаю. Помощь - /help')
#     # find(message.text.upper())
#     # with open('out.png', 'rb') as photo:
#     #     bot.send_photo(message.chat.id, photo)
#
#
# bot.polling()
