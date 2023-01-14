import telebot
from PIL import Image
import io

with open('token.txt') as _token:
    token = _token.readline()
bot = telebot.TeleBot(token)


class Img:
    number_of_point_types = 5
    point_types = {i: f'{i}.png' for i in range(number_of_point_types)}
    px_in_point = 20

    def __init__(self, image_data: bytes, paper: tuple[int, int], sensitivity: float | int):
        self.image = Image.open(io.BytesIO(image_data))
        self.paper_size = (paper[0] * 3, paper[1] * 3)  # *3 потому что каждая клетка разбивается на 9
        self.sensitivity = sensitivity
        self.points = {i: int(i * (255 / self.number_of_point_types * self.sensitivity)) for i in
                       range(self.number_of_point_types)}

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

        reconstructed_image = Image.new('RGB', (  # создаю фон
            self.image.size[0] * self.px_in_point, self.image.size[1] * self.px_in_point))

        for x_coord in range(self.image.size[0]):
            for y_coord in range(self.image.size[1]):
                for point_type in range(self.number_of_point_types - 1, -1, -1):
                    if sum(self.image.getpixel((x_coord, y_coord))) / 3 > self.points[point_type]:
                        reconstructed_image.paste(Image.open(self.point_types[point_type]),
                                                  (x_coord * self.px_in_point, y_coord * self.px_in_point))
                        break  # и в фон вставляю картинки с разным узором (, а также, соответственно, яркостью)

        # reconstructed_image.show()
        reconstructed_image.save('out.png')


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
    Img(photo, (40, 34), 1.1).reconstruct()
    with open('out.png', "rb") as _new_photo:
        bot.send_photo(message.chat.id, _new_photo)


def _other(message):
    bot.send_message(message.chat.id, 'Я вас не понимаю. Помощь - /help')
    # find(message.text.upper())
    # with open('out.png', 'rb') as photo:
    #     bot.send_photo(message.chat.id, photo)


bot.polling()
