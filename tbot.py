import requests
import telebot
import sys
sys.path.insert(0, '../WebServer/')
from layout import users, lvls, dbase
import answers
import json


token = '624990039:AAGTYXZ6cpD-GRCmgKLXDfBhrEz7WUPpUYk'
bot = telebot.TeleBot(token)

ans = answers.Answers()

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    body= message.text
    if users.get_by_tele(message.from_user.id) is not None:
        mes = ans.get_answer(body, message)
        if mes is not None:
            bot.send_message(message.chat.id, mes)
            ans.save()
    else:
        if ' '.join(message.text.split()[:2]) != 'LOG IN':
            bot.send_message(message.chat.id, '''You must log in. Write:
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
            bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
    print('Started')
    bot.polling(none_stop=True)