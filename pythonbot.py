import telebot
from telebot import types
from telebot import apihelper
from time import sleep

apihelper.proxy = {'https': "socks5://46.209.63.75:44550"}

TOKEN = '867546698:AAGqEIa_80wJPBwezLDTVHGYV75WVlEo4Pk'

BUY_RANDOM_MOVIE = 'Купить случайное видео'
BUY_RANDOM_PHOTO = 'Купить случайное фото'
BUY_RANDOM_PACK = 'Купить случайный пак'

clear_keyboard = types.ReplyKeyboardRemove()

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup.add(BUY_RANDOM_MOVIE)
markup.add(BUY_RANDOM_PHOTO)
markup.add(BUY_RANDOM_PACK)

confirm = types.ReplyKeyboardMarkup(one_time_keyboard=True)
confirm.add("Да", "Нет")

choice = ''
quantity = 0

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def _start(message):  # Название функции не играет никакой роли, в принципе
    if message.text == '/start':
        bot.send_message(message.chat.id, "Выберите, что вы хотите приобрести: ", reply_markup=markup)
        bot.register_next_step_handler(message, get_choice)


def get_choice(message):
    global choice
    choice = message.text
    bot.send_message(message.chat.id, "Выберите количество: ", reply_markup=clear_keyboard)
    bot.register_next_step_handler(message, get_quantity)


def get_quantity(message):
    global quantity
    try:
        quantity = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка ')
    finally:
        print_buy_info(message)


def print_buy_info(message):
    global choice
    global quantity
    msg = f"Вы выбрали:\n{choice} в количестве {quantity} штук\nВерно?"
    bot.send_message(message.chat.id, msg, reply_markup=confirm)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as E:
            print(E.args)
            sleep(2)
            # break
