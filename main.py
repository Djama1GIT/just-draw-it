import telebot
from PIL import Image

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)


class Img:
    def __init__(self, image_src=None):
        self.image_src = image_src
        self.image = Image.open('img_1.png')
        self.default_paper_size = (40 * 3, 34 * 3)
        self.px_in_px = 20
        self.paper_size = (self.default_paper_size[0] * self.px_in_px, self.default_paper_size[1] * self.px_in_px)
        self.sens = 1
        self.variables_count = 5
        self.variables = {i: tuple([int(i * (255 / self.variables_count) * self.sens)] * 3) for i in
                          range(self.variables_count)}
        self.variables_img = {self.variables[i]: f'{i}.png' for i in range(len(self.variables))}

    def re(self):
        # нужно укорочать:
        # создаю фон,
        # изменяю размер изображения,
        # прохожусь по каждому пикселю и устанавливаю соответствующий цвет,
        # изменяю размер фона,
        # делаю бекап основного изображения,
        # изменяю размер основного изображения,
        # и на основное изображение исходя из бекапа накладываю фотки,
        # накладываю изображение на фон.

        # нужно прийти к:
        # создаю фон, согласно изображению,
        # определяю размер изображения и прохожусь по зонам,
        # согласно яркости зоны вставляю в фон нужное изображение

        background = Image.new('RGB', self.default_paper_size)
        background.paste((255, 255, 255), [0, 0, background.size[0], background.size[1]])  # создаю фон
        self.image = self.image.resize(  # изменяю размер изображения
            (int(self.image.size[0] * (self.default_paper_size[temp_bool := self.image.size[1] > self.image.size[0]] /
                                       self.image.size[temp_bool])),
             int(self.image.size[1] * (self.default_paper_size[temp_bool] /
                                       self.image.size[temp_bool]))),
            resample=Image.BOX)
        for left in range(self.image.size[0]):
            for up in range(self.image.size[1]):  # прохожусь по каждому пикселю и устанавливаю соответствующий цвет
                self.image.putpixel((left, up), self.variables[
                    min(self.variables_count - 1,
                        round(self.sens * sum(self.image.getpixel((left, up))) / 3 / (
                                255 / (self.variables_count - 1))))])
        background = background.resize(self.paper_size, resample=Image.NONE)  # изменяю размер фона
        original_image = self.image  # бекап основного изображения
        if self.image.size[1] > self.image.size[0]:
            temp_sizes = (self.image.size[0] * int((self.paper_size[1] / self.image.size[1])), self.paper_size[1])
        else:
            temp_sizes = (self.paper_size[0], self.image.size[1] * int((self.paper_size[0] / self.image.size[0])))
        self.image = self.image.resize(temp_sizes, resample=Image.NONE)  # изменяю размер основного изображения
        for i in range(original_image.size[0]):
            for j in range(original_image.size[1]):  # и на основное изображение исходя из бекапа накладываю фотки
                self.image.paste(
                    Image.open(self.variables_img[self.variables[
                        round(sum(original_image.getpixel((i, j))) / 3 / (255 / (self.variables_count - 1)))]]),
                    (i * 20, j * 20))
        if self.image.size[1] > self.image.size[0]:  # накладываю изображение на фон
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
