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
    body = message.text
    if users.get_by_tele(message.from_user.id) is not None:
        mes = ans.get_answer(body, message)
        if mes is not None and mes.split()[0] != 'file':
            bot.send_message(message.chat.id, mes)
            ans.save()

        elif mes is not None and mes.split()[1] == 'audio':
            audio = open('speeched.mp3', mode='rb')
            bot.send_audio(message.chat.id, audio)
            audio.close()

        elif mes is not None and mes.split('|')[0].split()[1] == 'image':
            image = open(mes.split('|')[1], mode='rb')
            bot.send_photo(message.chat.id, image, mes.split('|')[2])
            image.close()

        print('{\n'+users.get_by_tele(message.from_user.id)[1], str(users.get_by_tele(message.from_user.id)[0]) + ' / '+str(users.get_by_tele(message.from_user.id)[6])+': ' + str(body) + '\n\nBot: ' + str(mes)+'\n}\n')

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
            try:
                answer = users.update_telegram_id(email,password, message.from_user.id)
                users.update_telegram_id(email, password, message.from_user.id)
            except IndexError:
                answer = 'Wrong email or password'

            bot.send_message(message.chat.id, answer)



if __name__ == '__main__':
    print('Started')
    bot.polling(none_stop=True)