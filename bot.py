from dotenv import load_dotenv
import os
import telebot
from telebot import types

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

bot.set_my_commands (
    [types.BotCommand("start" , "firs message"),
    types.BotCommand("photo" , "photos"),
    types.BotCommand("sound" , "sounds"),
    types.BotCommand("link" , "ссылОЧКА"),
    types.BotCommand("update" , "обновление списка команд")]
)

@bot.message_handler(commands=['link'])
def send_link(message):
    text = '<a href="https://karp.neocities.org/"> мой сайт </a>'
    bot.send_message(message.chat.id , text , parse_mode = "HTML")

@bot.message_handler(commands=['update'])
def bot_update(message):
    bot.delete_my_commands()
    bot.set_my_commands(
    [types.BotCommand("start" , "firs message"),
    types.BotCommand("photo" , "photos"),
    types.BotCommand("sound" , "sounds"),
    types.BotCommand("link" , "ссылОЧКА")]
    )
    bot.send_message(message.chat.id , "обновлено")


menu_mark = types.ReplyKeyboardMarkup(resize_keyboard = True)
menu_mark.row('фото' , 'звуки')
menu_mark.row('ссылка' , 'обновить список')



@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "📌 *Информация о ТГ БОТЕ:*\n\n"
        "1. Команда photo отправляет выбор фотографий\n"
        "2. Команда sound отправляет выбор звуков\n"
        "Спасибо за внимание!"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown' , reply_markup=menu_mark)


@bot.message_handler(func = lambda message: True)
def button_call(message):
    if message.text == 'фото':
        send_photo(message)
    elif message.text == 'ссылка':
        send_link(message)
    elif message.text == 'звуки':
        send_audio(message)
    elif message.text == 'обновить список':
        bot_update(message)


@bot.message_handler(commands=['photo'])
def send_photo(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Картинка 1", callback_data='photo1')
    btn2 = types.InlineKeyboardButton("Картинка 2", callback_data='photo2')
    btn3 = types.InlineKeyboardButton("Картинка 3", callback_data='photo3')
    btn4 = types.InlineKeyboardButton("Картинка 4", callback_data='photo4')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, 'Какую картинку ты хочешь?:', reply_markup=markup)

@bot.message_handler(commands=['sound'])
def send_audio(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Звук 1", callback_data='audio1')
    btn2 = types.InlineKeyboardButton("Звук 2", callback_data='audio2')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Какой звук ты хочешь?:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'photo1':
        with open('images/good.jpg', 'rb') as files:
            bot.send_photo(call.message.chat.id, files, caption="Вы выбрали опцию 1!")
            voice = open('ogg/tr.ogg', 'rb')
            bot.send_voice(call.message.chat.id, voice)
            voice.close()
    elif call.data == 'photo2':
        with open('images/tral.jpg', 'rb') as files:
            bot.send_photo(call.message.chat.id, files, caption="Вы выбрали опцию 2!")
            voice = open('ogg/tr.ogg', 'rb')
            bot.send_voice(call.message.chat.id, voice)
            voice.close()
    elif call.data == 'audio1':
        voice = open('ogg/tr.ogg', 'rb')
        bot.send_voice(call.message.chat.id, voice)
        voice.close()

bot.polling()