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
from julia.some_function import send_video, send_movie
from telegram import *
from telegram.ext import *


logging.basicConfig(level = logging.DEBUG)
maintance = False

def movie(update, context):
	"""
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
		if '/movie' in single_text:
			query = text.replace('/movie', '')
			query = query.split()
			query = '-'.join([v for v in query])
		elif '/s' in single_text:
			query = text.replace('/s', '')
			query = query.split()
			query = '-'.join([v for v in query])

		msg = update.message.reply_text("<b>Lagi nyari..</b>", parse_mode = 'HTML')
		if chat_id in allowed_chat:
			for end in urls:
				T = Thread(target = send_movie, name = end, kwargs = {'query' : query, 'BASE_URL' : end, 'chat_id' : chat_id})
				T.start()

		else:
			pass
		msg.delete()
	else:
		pass
def button(update: Update, context) -> None:
	query = update.callback_query
	query.answer()
	if query.data.split("^")[0] == "judul":
		chat_id = query.data.split("^")[2]
		message_id = int(query.data.split("^")[1])
		current_id.append(message_id)
		ic(current_id)
		query.delete_message()
		
	elif query.data == "pin":
		query.pin_message()

	elif query.data.split('^')[0] == "peek":
		title = query.data.split('^')[2]
		title = title.replace("&", "")
		chat_id = query.data.split('^')[1]
		query.delete_message()
		def create_task(title: str="", chat_id: int=None):
			async def theAgent():
				task = asyncio.create_task(AGENT(title, chat_id))
				await task
			asyncio.run(theAgent())
		T = Thread(target = create_task, name = title, kwargs = {"title" : title, "chat_id" : int(chat_id)})
		T.start()

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

def feed(update, context):
	HOST = "https://www.cnnindonesia.com"
	SUB = '/terpopuler'
	req = requests.get(HOST + SUB)
	soup = BeautifulSoup(req.text,'html.parser')
	aTag = soup.find_all("a")
	for a in aTag:
		href = a.get("href")
		link = href.split('/')
		if len(link) > 5:
			if (link[3]) == 'accounts':
				pass
			else:
				CATEGORY = link[3]
				SUB_4 = link[4]
				SUB_5 = link[5]
				TITLE = SUB_5.replace('-', ' ').upper()
				URL = (HOST +"/"+ SUB_4 +"/"+ SUB_5)
				REQ = requests.get(URL)
				SOUP = BeautifulSoup(REQ.text, 'html.parser')
				img = SOUP.find_all("img")
				HOST_AKCDN = 'akcdn.detik.net.id'
				list = ["", "", "", "", "", "", ""]
				count=0
				for imgTag in img:
					src = imgTag.get("src")
					alt = imgTag.get("alt").upper()
					list[count] = alt
					count+=1
					if not '' in list:
						ic(list)
						BoldText = f"<i>CNN Indonesia</i> |  |\n\n<b>- {list[1]}\n\n- {list[2]}</b>\n\n❝  <i>{list[3]}</i>  ❞\n\n- <b>{list[4]}\n\n- {list[5]}</b>"
						board = [
									[
									InlineKeyboardButton("MORE",url=HOST + SUB)]
									]
						button = InlineKeyboardMarkup(board,resize_keyboard=True,one_time_keyboard=True)
						update.message.reply_photo(photo=src, reply_markup=button, caption=BoldText, parse_mode='html')
					else:
						pass
				break
		else:
			pass
			
def feedTwo(update, context):
	chat_id = update.message.chat_id
	req = requests.get("https://newsapi.org/v2/top-headlines?country=id&apiKey=1c21e0843089413693b572ea8bd26ceb")
	LIST = ["", "", "", "", ""]
	LISTS = []
	for i in range(len(req.json()["articles"])):
		SUMBER = req.json()["articles"][i]["source"]["name"]
		JUDUL = req.json()["articles"][i]["title"]
		URL = req.json()["articles"][i]["url"]
		try:
			shit_ = [SUMBER, JUDUL, URL]
			LIST[i] = shit_
			if "" in LIST:
				i +=1
			else:
				pass
		except:
			pass
			
	for list_ in LIST:
		source_ = list_[0]
		feed_ = list_[1]
		link_ = list_[2]
		result = f"<i>{source_.split('.')[0]}</i>\n\n<b>{feed_.upper()}</b> | {source_.upper()}<a href='{link_}'> | </a>"
		LISTS.append(result)
	DATA = "\n\n".join([val for val in LISTS])
	send_text(DATA, chat_id)
	
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
	dp.add_handler(CallbackQueryHandler(button))
	dp.add_handler(CommandHandler("s",movie))
	dp.add_handler(CommandHandler("movie",movie))
	dp.add_handler(CommandHandler("feed",feed))
	dp.add_handler(CommandHandler("feeds",feedTwo))
	dp.add_handler(MessageHandler(Filters.text, handle_chat))
	dp.add_handler(MessageHandler(Filters.entity, remove_joiner))
	dp.add_error_handler(error)
	updater.start_polling()
	
	updater.idle()
