import telebot
import os
from os import path
from time import sleep
from shutil import move

goods = []

token = "819805772:AAG85F-lqpGVR2BwAhJMPkByk_-6QXQmlZ4"
bot = telebot.TeleBot(token)

img_id = ''
price = ''
seller = False
listID = 4


def save(message):
    print('запуск сохранения')
    global img_id, listID

    file_info = bot.get_file(img_id)  # name + price

    goods_id = str(listID)
    goods_username = str(message.from_user.username)
    goods_price = str(message.text)

    path = 'D:/praktikaBot/goods/' + goods_id + '_' + goods_username + '_' + goods_price + ".jpg"
    file_info = bot.get_file(img_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file, )

    print('сохранение успешно')


def logic_photo(message):
    global seller
    bot.send_message(message.from_user.id, 'Хороший арбуз')
    bot.send_message(message.from_user.id, 'Сколько за него хочешь')

    global img_id
    print("ожидание цены")
    img_id = message.photo[0].file_id
    print(img_id)
    seller = False


def logic_text(message):
    global img_id, seller

    if "продать арбуз" in message.text or "продам арбуз" in message.text:
        bot.send_message(message.from_user.id, 'Отправь фото арбуза которвй хочешь мне продать')
        seller = False

    else:
        if "арбуз" in message.text:
            bot.send_message(message.from_user.id, 'Какой арбуз хочешь')

            print("Ответ отправлен")

            directory = 'D:/praktikaBot/goods'
            all_files_in_directory = os.listdir(directory)
            print(all_files_in_directory)

            for file in all_files_in_directory:
                img = open(directory + '/' + file, 'rb')
                bot.send_photo(message.from_user.id, img)
                price = path.splitext(file)[0].split('_')
                print(path.splitext(file)[0])
                bot.send_message(message.from_user.id, price[0] + ') ' + price[2] + " руб.")
                img.close()

            bot.send_message(message.from_user.id, "Выбирай")
            seller = True

    if message.text.isdigit() and seller == False:
        if img_id != '':
            if int(message.text) < 501 and int(message.text) > 100:

                print("Цена принята")

                bot.send_message(message.from_user.id, 'Хорошо, теперь неси его сюда')

                if bot.send_location(message.from_user.id, 56.458961, 84.945821):
                    print('Локация отправлена')
                else:
                    print('ошибка отправки')

                save(message)
            else:
                print("Ошибка: большая цена")
                bot.send_message(message.from_user.id, 'Не, так не пойдёт')
        else:
            print("Ошибка: нет фото")
            bot.send_message(message.from_user.id, 'Ты не отправлял мне арбуз')

    if message.text.isdigit() and seller:

        directory = 'D:/praktikaBot/goods'
        all_files_in_directory = os.listdir(directory)
        print(all_files_in_directory)

        print('Проверка на существование')

        for file in all_files_in_directory:
            img = open(directory + '/' + file, 'rb')
            id = path.splitext(file)[0].split('_')
            if message.text == id[0]:
                img.close()
                move(directory + '/' + file, 'D:/praktikaBot/reserved_goods')

        bot.send_message(message.from_user.id, 'Я придержу для тебя этот арбуз')
        bot.send_message(message.from_user.id, 'забрать его можешь здесь')
        bot.send_location(message.from_user.id, 56.458961, 84.945821)

        seller = False
