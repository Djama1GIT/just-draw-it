import telebot
from PIL import Image, ImageDraw, ImageFont

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)

default_paper_size = (40 * 3, 34 * 3)
px_in_px = 20
paper_size = (default_paper_size[0] * px_in_px, default_paper_size[1] * px_in_px)
sens = 1
variables = {
    0: (int(0 * sens), int(0 * sens), int(0 * sens)),
    1: (int(64 * sens), int(64 * sens), int(64 * sens)),  # .
    2: (int(127 * sens), int(127 * sens), int(127 * sens)),  # +
    3: (int(191 * sens), int(191 * sens), int(191 * sens)),  # •
    4: (int(255 * sens), int(255 * sens), int(255 * sens)),
}
variables_img = {
    variables[0]: '0.png',
    variables[1]: '1.png',
    variables[2]: '2.png',
    variables[3]: '3.png',
    variables[4]: '4.png',
}


class Img:
    def __init__(self, image_src=None):
        self.image_src = image_src
        self.image = Image.open('img_1.png')

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
                                    variables[round(sum(self.image.getpixel((left, up))) / 3 / 63.75)])
        background = background.resize(paper_size, resample=Image.NONE)
        original_image = self.image
        if self.image.size[1] > self.image.size[0]:
            self.image = self.image.resize(
                (self.image.size[0] * int((paper_size[1] / self.image.size[1])), paper_size[1]),
                resample=Image.NONE)
        else:
            self.image = self.image.resize(
                (paper_size[0], self.image.size[1] * int((paper_size[0] / self.image.size[0]))),
                resample=Image.NONE)
        for i in range(original_image.size[0]):
            for j in range(original_image.size[1]):
                self.image.paste(
                    Image.open(variables_img[variables[round(sum(original_image.getpixel((i, j))) / 3 / 63.75)]]),
                    (i * 20, j * 20))
        if self.image.size[1] > self.image.size[0]:
            background.paste(self.image, ((background.size[0] - self.image.size[0]) // 2, 0))
        else:
            background.paste(self.image, (0, (background.size[1] - self.image.size[1]) // 2))
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
