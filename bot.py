from threading import Thread
import os
import sys
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from my_token import *
from my_functions import *


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hallo, hier ist der Tingeltangelbot.\nIch habe noch keine Funktion, aber ich freue mich, dass du mit mir chatten möchtest.")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def menu_callback(update, context):
    some_strings = ["Dip", "Klops", "MUANTI"]
    button_list = [telegram.InlineKeyboardButton(s, callback_data=s) for s in some_strings]
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(chat_id=update.effective_chat.id, text="Und?", reply_markup=reply_markup)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def menu_actions(update, context):
    query = update.callback_query
    if query.data == 'Klops':
        bot.send_sticker(chat_id=update.effective_chat.id, sticker='CAACAgIAAxkBAANSXm6kSVIrMGb3nYza8xUaAofguYwAAg8AAyu-QRarA2oDdEAg0RgE')
    reply = 'Ja, stimmt. {}'.format(query.data)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

def restart(update, context):
    update.message.reply_text('Moment, ich starte neu...')
    Thread(target=stop_and_restart).start()

bot = telegram.Bot(token=TOKEN)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

menu_handler = CommandHandler('menu', menu_callback)
dispatcher.add_handler(menu_handler)
dispatcher.add_handler(CallbackQueryHandler(menu_actions))

dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(username=MY_USERNAME)))

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()