import os
from telebot import *

botToken = "6908895767:AAHo4WwrmW0cNmYztBGi81N6Vq38W4AfMeU"
disks = ["C:/"]
bot = TeleBot(botToken)
curDirectory = "C:/Users/User/PycharmProjects/pythonProjectdata/"

@bot.message_handler(commands=["help"])
def helper(message: types.Message):
    bot.send_message(message.chat.id, "Введите /sys для входа в цикл программы")
    bot.send_message(message.chat.id, "Введите dir для просмотра директории")
    bot.send_message(message.chat.id, "Введите сd для для смены директории")
    bot.send_message(message.chat.id, "Введите get для отправки файла из директории")

@bot.message_handler(commands=["sys"])
def regSys(message: types.Message):
    bot.register_next_step_handler(message, systemExecutor)

def systemExecutor(message: types.Message):
    if message.text == "dir":
        bot.send_message(message.chat.id, str(os.listdir(curDirectory)))
        bot.register_next_step_handler(message, systemExecutor)
    elif message.text == "cd":
        markup = types.ReplyKeyboardMarkup(True)
        for d in os.listdir(curDirectory):
            markup.add(types.KeyboardButton(d))
        markup.add(types.KeyboardButton("Назад"))
        bot.send_message(message.chat.id, "Выберите директорию", reply_markup=markup)
        bot.register_next_step_handler(message, changeDirectoryHandler)
    elif message.text == "get":
        markup = types.ReplyKeyboardMarkup(True)
        for d in os.listdir(curDirectory):
            markup.add(types.KeyboardButton(d))
        markup.add(types.KeyboardButton("Назад"))
        bot.send_message(message.chat.id, "Выберите файл", reply_markup=markup)
        bot.register_next_step_handler(message, getFileHandler)
    else:
        bot.send_message(message.chat.id, "Такой команды нет")
        bot.register_next_step_handler(message, systemExecutor)

def getFileHandler(message: types.Message):
    if "." not in message.text:
        bot.send_message(message.chat.id, "Выбран неправильный файл")
        bot.register_next_step_handler(message, systemExecutor)
    else:
        for d in os.listdir(curDirectory):
            if message.text == d:
                with open(curDirectory + d, "rb") as file:
                    bot.send_document(message.chat.id, file)
                break
        bot.register_next_step_handler(message, systemExecutor)

def changeDirectoryHandler(message: types.Message):
    global curDirectory
    if "." in message.text:
        bot.send_message(message.chat.id,"неправильно выбрана директория")
        bot.register_next_step_handler(message, systemExecutor)
    else:
        for d in os.listdir(curDirectory):
            if message.text == d:
                curDirectory += d + "/"
        if message.text == "Назад":
            if curDirectory.count("/") >= 2:
                curDirectory = curDirectory[:curDirectory.index(curDirectory.split("/")[-2])]
            else:
                markup = types.ReplyKeyboardMarkup()
                for d in disks:
                    markup.add(types.KeyboardButton(d))
                markup.add(types.KeyboardButton("Назад"))
                bot.send_message(message.chat.id, "Выберите диск", reply_markup=markup)
                bot.register_next_step_handler(message, changeDiskHandler)
        bot.register_next_step_handler(message, systemExecutor)

def changeDiskHandler(message: types.Message):
    global curDirectory
    for d in disks:
        if message.text == d:
            curDirectory = d
    bot.register_next_step_handler(message, systemExecutor)

bot.polling(non_stop=True)
