import telebot
from PIL import Image

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)


class Img:
    variables_count = 5
    variables_img = {i: f'{i}.png' for i in range(variables_count)}
    px_in_px = 20

    def __init__(self, image_src='img_1.png', paper=(40, 34), sens=0.65):
        self.image_src = image_src
        self.image = Image.open(image_src)
        self.paper_size = (paper[0] * 3, paper[1] * 3)  # *3 потому что каждая клетка разбивается на 9
        self.sens = sens
        self.variables = {i: int(i * (255 / self.variables_count * self.sens)) for i in
                          range(self.variables_count)}

    def reconstruct(self) -> None:
        """
        This function converts an ordinary image into images of a format convenient for drawing on a notebook.
        """
        self.image = self.image.resize(  # Уменьшаю размер изображения
            (int(self.image.size[0] * (self.paper_size[temp_bool := self.image.size[1] > self.image.size[0]] /
                                       self.image.size[temp_bool])),
             int(self.image.size[1] * (self.paper_size[temp_bool] /
                                       self.image.size[temp_bool]))),
            resample=Image.BOX)
        background = Image.new('RGB', (self.image.size[0] * 20, self.image.size[1] * 20))  # создаю фон
        background.paste((255, 255, 255), [0, 0, background.size[0], background.size[1]])
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                point: Image = None  # и в фон вставляю картинки с разной узором (, а также, соответственно, яркостью)
                for number_of_variables in range(self.variables_count - 1, -1, -1):
                    if sum(self.image.getpixel((i, j))) / 3 > self.variables[number_of_variables]:
                        point = Image.open(self.variables_img[number_of_variables])
                        break
                background.paste(point, (i * 20, j * 20))
        background.show()
        background.save('out.jpg')


x = Img()
x.reconstruct()
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
