from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import sys
sys.path.insert(0, '../WebServer/')
from layout import users, lvls, dbase
import answers
import json
import logging

ans = answers.Answers()
keyboard = [['Помощь','/shop'],['/close']]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
remove_kb = ReplyKeyboardRemove()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='data.log')
logger = logging.getLogger(__name__)

def inline_keyboard(update, context):
    inline_buttons = [[InlineKeyboardButton("Рейтинг: 1кк/шт.", callback_data='купить рейтинг'),
                 InlineKeyboardButton("Меч", callback_data='купить меч')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    inline_markup = InlineKeyboardMarkup(inline_buttons)
    update.message.reply_text('Магазин:', reply_markup= inline_markup)

def inline_button_answer(update, context):
    query = update.callback_query
    answer = chating(update,None, get_ans=True, ready_message=query.data)
    chat_id = update.callback_query.message.chat.id
    query.answer(answer)
    ans.save()


def chating(update, bot, get_ans = False, ready_message = None):
    message = update['message']
    if ready_message is None:
        body = message.text
    else:
        message = update.callback_query.message
        body = ready_message
    if get_ans is False:
        mes = ans.get_answer(body, message)
        if users.get_by_tele(message.from_user.id) is not None:
            if mes is not None and len(mes.split()) >= 1:
                if mes.split()[0] != 'file':
                    update.message.reply_text(mes)
                    ans.save()
                elif len(mes.split()) > 1 and mes.split()[0] == 'file':
                    if mes.split()[1] == 'audio':
                        audio = open('speeched.mp3', mode='rb')
                        update.message.reply_audio(audio)
                        audio.close()

                    elif mes.split('|')[0].split()[1] == 'image':
                        image = open('drew.png', mode='rb')
                        update.message.reply_photo(image, mes.split('|')[1])
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
                print(email, password)
                answer = users.update_telegram_id(email, password, message.from_user.id)
                users.update_telegram_id(email, password, message.from_user.id)
                update.message.reply_text(answer)
    else:
        return ans.get_answer(body, message, use_inline=True)


def close_kb(update, bot):
    update.message.reply_text('Готово.', reply_markup = remove_kb)

def show_keyboard(update, bot):
    update.message.reply_text("Готово.",
                              reply_markup=markup)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater('624990039:AAGTYXZ6cpD-GRCmgKLXDfBhrEz7WUPpUYk', use_context=True)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, chating)
    keyboard_handler = CommandHandler('keyboard', show_keyboard)
    inline_keyboard_handler = CommandHandler('shop', inline_keyboard)
    callback_query_handler = CallbackQueryHandler(inline_button_answer)
    close_keyboard = CommandHandler('close', close_kb)

    dp.add_handler(text_handler)
    dp.add_handler(keyboard_handler)
    dp.add_handler(inline_keyboard_handler)
    dp.add_handler(callback_query_handler)
    updater.dispatcher.add_error_handler(error)
    dp.add_handler(close_keyboard)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    print('Started')
    main()