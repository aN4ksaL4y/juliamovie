# developed by Al Fajri (based on python-telegram-bot)

import os
import wikipedia
import random
import logging
import pytz
import time
import requests
import asyncio
from threading import Thread
from prettytable import PrettyTable
from icecream import ic
from julia.conf import allowed_chat, API_KEY
from julia.some_function import send_video, send_movie, search_movie_url
from telegram import *
from telegram.ext import *


logging.basicConfig(level = logging.DEBUG)
maintance = False

def movie(update, context):
	"""

	A Function that respond when (/movie) command appear.
	"""
	chat_id = str(update.message.chat_id)
	urls = [
		'https://malikamovie-database.herokuapp.com/public', 
		'https://malikamovie-database.herokuapp.com/private',
		'https://i-ka.herokuapp.com/get/u_n_d_e_r_s_c_o_r_e_d'
	]
	text = str(update.message.text).lower()

	single_text = [v for v in text.split()]
	if maintance:
		update.message.reply_text('Maintaning..')
	elif not maintance:
		query = ''
		msg = update.message.reply_text("<b>Lagi nyari..</b>", parse_mode = 'HTML')
		if '/movie' in single_text:
			query = text.replace('/movie', '')
			query = query.split()
			query = '-'.join([v for v in query])
			if chat_id in allowed_chat:
					for end in urls:
						T = Thread(target = send_movie, name = end, kwargs = {'query' : query, 'BASE_URL' : end, 'chat_id' : chat_id})
						T.start()
			msg.delete()
		elif '/s' in single_text:
			query = text.replace('/s', '')
			urls = search_movie_url(query)

			__list__ = []
			for url in urls:
				domain = url.split('/')[-2]
				domain = domain.replace('-', ' ').title()
				text = f"-> <a href='{url}'>{domain}</a>"
				__list__.append(text)
			captions = "\n".join([v for v in __list__])

			update.message.reply_text(captions, parse_mode='html')

		else:
			pass
	else:
		pass

def handle_chat(update, context):
	text = str(update.message.text).lower()
	# response = CHAT.chat(text)
	# update.message.reply_text(text=response, reply_markup=None, parse_mode='html')

	ic(text)

def start(update, context):
	HOST = "https://firebasestorage.googleapis.com/v0/b/playlistden.appspot.com"
	animationLink = [
	"/o/gif%2Fmp4(2).mp4?alt=media&token=cbe75a7c-2f6b-44aa-8b4f-f7fe1ee2fc8b", 
	"/o/gif%2Fmp4(3).mp4?alt=media&token=b2c04ef4-29c0-44b8-a8f4-9c7f60f58b7e", 
	"/o/gif%2Fmp4(4).mp4?alt=media&token=cce4a10a-1f7a-4573-b96c-9453d0fdf7dd", 
	"/o/gif%2Fmp4.mp4?alt=media&token=8df08d66-6a85-40ca-8e26-b9e6bfc87c58",
	"/o/gif%2Fmp4(1).mp4?alt=media&token=df156817-284b-4bf3-969c-f0b49fd8ed67"
	]

	BASE_URL = 'https://www.tronalddump.io/random/quote'
	user = update.message.from_user
	username = user.username
	fName = user.first_name
	lName = user.last_name
	if lName == None:
		lName = ""
	ic("Start", fName)
	captions = f"Hai kak <b>{fName} {lName}!</b>\n"
	board = [
	[
	InlineKeyboardButton('Author',url='https://t.me/ini_peninggi_badan'),
	InlineKeyboardButton('Tentang', url='https://malikamovieonline.web.app')
		]
	]
	about = []
	reply = InlineKeyboardMarkup(board,resize_keyboard=True,one_time_keyboard=True)
	link = HOST + random.choice(animationLink)
	msg = update.message.reply_animation(animation=link, reply_markup=reply, caption=captions, parse_mode='html')
	
def remove_joiner(update, context):
	msg_id = update.message.message_id
	is_new_member = update.message.new_chat_members
	chat_id = update.message.chat.id
	bot = context.bot
	if is_new_member:
		print(msg_id, chat_id, "deleted.")
		bot.delete_message(chat_id, msg_id)
		
def error(update, context):
	context_error = context.error
	ic(context_error)

def main():
	updater = Updater(API_KEY, use_context=True)
	dp = updater.dispatcher

	# handler for commands.
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("s",movie))
	dp.add_handler(CommandHandler("movie",movie))
	dp.add_handler(MessageHandler(Filters.text, handle_chat))
	dp.add_handler(MessageHandler(Filters.entity, remove_joiner))
	dp.add_error_handler(error)
	updater.start_polling()
	
	updater.idle()
