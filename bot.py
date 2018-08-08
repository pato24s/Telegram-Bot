import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import KeyboardButton
from telegram.ext import MessageHandler, Filters

import logging
bot_token = '697931558:AAFTBIorcFD5l6n2kFI-lHGALTD_jlamDA4'

updater = Updater(token=bot_token)

bot = telegram.Bot(token=bot_token)

dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_location(bot, update):
	location_keyboard = KeyboardButton(text="send location",  request_location=True)           #creating location button object
	custom_keyboard = [[ location_keyboard]] #creating keyboard object
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)                                                                                  
	update.message.reply_text("This bot requires to know your location before continuing", reply_markup=reply_markup)
	# updates = bot.get_updates(offset=1)
	# print (updates)

def start(bot, update):
	print("Aaaaaaaaaaa")
	get_location(bot,update)
	#bot.send_message(chat_id=update.message.chat_id, text="aloooh")



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def link_atms(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Cajeros Link más cercanos:")

link_handler = CommandHandler('link', link_atms)
dispatcher.add_handler(link_handler)


def banelco_atms(bot, update):
	get_location(bot, update)
	bot.send_message(chat_id=update.message.chat_id, text="Cajeros Banelco más cercanos")

banelco_handler = CommandHandler('banelco', banelco_atms)
dispatcher.add_handler(banelco_handler)


def location(bot, update):
	print ("EEEEEe")
	print(update.message.location)


def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)



updater.start_polling()