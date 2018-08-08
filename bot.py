import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import KeyboardButton
from telegram.ext import MessageHandler, Filters

import logging
import parser
from parser import getNearestAtms
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

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="This bot will help you find the nearest ATM to your location\n Type /help in order to get information about the commands")

def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Commands:\n /start - Get welcome message \n /link - Get nearest LINK ATMs \n /banelco - Get nearest BANELCO ATMs \n ""\n This bot only shows the 3 nearest ATMs within 500metre radius \n ""\n This bot requieres access to your location" )

def link_atms(bot, update, chat_data):
	chat_data['red'] = 'LINK'
	get_location(bot, update)



def banelco_atms(bot, update, chat_data):
	chat_data['red'] = 'BANELCO'
	get_location(bot, update)



def location(bot, update, chat_data):
	if not'red' in chat_data or chat_data['red']=='NONE':
		bot.send_message(chat_id=update.message.chat_id, text="To get the nearest ATMs type /banelco or /link")
	else:
		bankingNetwork = chat_data['red']
		chat_data['red'] = 'NONE'
		listOfAtms = getNearestAtms(update.message.location, bankingNetwork)
		if len(listOfAtms) == 0:
			bot.send_message(chat_id=update.message.chat_id, text="There are no nearby ATMs")
		else:
			msg = "Nearby " + chat_data['red'] + " ATMs \n"
			msg += listOfAtms
			bot.send_message(chat_id=update.message.chat_id, text=msg)

	

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command. \n Type \help to get a list of possible commands.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


link_handler = CommandHandler('link', link_atms, pass_chat_data=True)
dispatcher.add_handler(link_handler)

banelco_handler = CommandHandler('banelco', banelco_atms, pass_chat_data=True)
dispatcher.add_handler(banelco_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


location_handler = MessageHandler(Filters.location, location, pass_chat_data=True)
dispatcher.add_handler(location_handler)



updater.start_polling()