import telebot
import logicka
import os

token = "819805772:AAG85F-lqpGVR2BwAhJMPkByk_-6QXQmlZ4"
bot = telebot.TeleBot(token)


def log(message):
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от " + message.from_user.username + " Текст: " + message.text)
    print("")


@bot.message_handler(commands=['help'])
def handle_command(message):
    print("Пришла команда")
    bot.send_message(message.from_user.id, "Если потерялся то я продаю арбузы ")
    bot.send_message(message.from_user.id, "Если хочешь купить арбуз напиши мне "
                                           "'хочу арбуз' или если хочешь продать арбуз мне, пиши 'продать арбуз'")


@bot.message_handler(commands=['start'])
def handle_command(massege):
    person = massege.from_user.first_name

    drygani = dict(crushT='Максимка', Kraydonov='Гелп', Onmoni='Денчик', Fourwordsallcaps="Артемка")

    if massege.from_user.username in drygani:
        person = drygani[massege.from_user.username]

    bot.send_message(massege.from_user.id, "Здарова " + person)


@bot.message_handler(content_types=["photo"])
def handle_text(message):
    print('пришла картинка')
    print(message)
    logicka.logic_photo(message)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    print("Пришло сообщение")
    log(message)
    logicka.logic_text(message)




bot.polling(none_stop=True, interval=0)
