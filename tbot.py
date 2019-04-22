import telebot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import sys
sys.path.insert(0, '../WebServer/')
from layout import users, lvls, dbase
import answers
import json

ans = answers.Answers()
keyboard = [['Помощь']]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
def chating(bot, update):
    message = update.message
    body = message.text
    if users.get_by_tele(message.from_user.id) is not None:
        mes = ans.get_answer(body, message)
        if len(mes.split()) >= 1:
            if mes is not None and mes.split()[0] != 'file':
                print(1)
                update.message.reply_text(mes)
                ans.save()
            elif len(mes.split()) > 1:
                if mes is not None and mes.split()[1] == 'audio':
                    audio = open('speeched.mp3', mode='rb')
                    update.message.reply_audio(audio)
                    audio.close()

                elif mes is not None and mes.split('|')[0].split()[1] == 'image':
                    image = open('drew.png', mode='rb')
                    update.message.reply_photo(image, 'Вот граф '+mes.split('|')[1])
                    image.close()

    else:
        if ' '.join(message.text.split()[:2]) != 'LOG IN':
            update.message.reply_text('''You must log in. Write:
        LOG IN
        your@email
        your_password''')
        else:
            body = message.text.split('\n')[1:]
            email = body[0]
            password = '\n'.join(body[1:])
            print(email,password)
            answer = users.update_telegram_id(email,password, message.from_user.id)
            users.update_telegram_id(email, password, message.from_user.id)
            update.message.reply_text(answer)

def show_keyboard(bot,update):
    update.message.reply_text("Готово.",
                              reply_markup=markup)

def main():
    updater = Updater('')

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, chating)
    keyboard_handler = CommandHandler('клава', show_keyboard)

    dp.add_handler(text_handler)
    dp.add_handler(keyboard_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    print('Started')
    main()