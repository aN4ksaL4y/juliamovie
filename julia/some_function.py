import base64
import requests
import random

from icecream import ic
from julia.conf import API_KEY, LANDING_PAGE, current_movie_provider, movie_domain
from julia.translate import google_translator as Translator
from julia.goo import search
from threading import Thread

class MetaData:
	data = {}
	def __init__(self, query: str="", route: str=""):
		self.query= query
		self.route= route
		self.api_key= 'UIEJKL-PYXWEK-LXSSOA-HGTBXG-ARQ'
		self.api_url = f"https://grambuilders.tech/{self.route}"
		self.params={"query":self.query}
	def TheMovieDataBase(self):
		try:
			r= requests.get(self.api_url,headers={"X-API-KEY": self.api_key},params=self.params)
			assert r.status_code== 200, ""
			results = [v for v in r.json()["result"]]
			self.data["results"] = results

			# ic(self.data)o
			return self.data
		except Exception as e:
			return e

def fetch_movie_url(url: str='', query: str=''):
	keyword = f"site:{url} intext:{query}"

	try:
		r = search(keyword)
		return r
	except:
		return None

def search_movie_url(query: str=''):
	urls = []

	url = random.choice(movie_domain)
	urls = fetch_movie_url(url = url, query = query)
	return urls

def get_filename(belakang):
	fname = base64.b64encode(
		bytes(time.ctime(),
		encoding='utf-8'))
	filename = fname.decode('utf-8') + belakang
	return filename

def send_photo(out_file, chat_id):
	files = {'photo': open(out_file, 'rb')}
	message = ('https://api.telegram.org/bot'+ API_KEY+ '/sendPhoto?chat_id=' + chat_id)
	send = requests.post(message, files = files)
	return send.status_code

def send_text(TEXT, chat_id):
	req = requests.post(
		'https://api.telegram.org/bot' + API_KEY + '/sendMessage' +'?chat_id='+ chat_id + '&text=' + TEXT + '&parse_mode=HTML'
	)

	return req.status_code

def send_video(file_id, chat_id, caption):
	payload = {
	'video':file_id, 
	'caption':caption,
	'supports_streaming':True,
	'reply_markup':
		{'inline_keyboard': 
		[
			[
				{'url': LANDING_PAGE, 'text': 'More Bot'}
			]
		]
		}, 
	'parse_mode':'HTML'
	}
	r = requests.post('https://api.telegram.org/bot' + API_KEY + '/sendVideo?chat_id=' + chat_id, json=payload)

	return r.status_code

def send_movie(query: str='', BASE_URL: str='', chat_id: str=''):
	"""
	"""
	if 'i-ka.herokuapp.com' in BASE_URL:
		r = requests.get(BASE_URL)
		assert r.status_code == 200, ''
		for data in r.json()['results']:
			if data['datatype'] == 'video':
				title = data['title']
				uid = data['id']
				file_id = data['link']
				title = title.lower()

				if '|' in title:
					title = title.split('|')[0]
				else:
					pass

				title_split = title.split()
				for title in title_split:
					if title.isdigit:
						title_split.remove(title)
				if query in title_split:
					title = ' '.join([v for v in title_split])
					title = title.replace('subtitle', '')
					r = send_video(file_id = file_id, chat_id = chat_id, caption = title)
					ic(r)
				else:
					pass 
			else:
				pass
	else:
		r = requests.get(BASE_URL)
		assert r.status_code == 200, ''
		for data in r.json()['results']:
			tandapagar = data['tandapagar'].lower()
			query = query.lower()
			if query in tandapagar:
				tandapagar = tandapagar.split()
				tandapagar = ' #'.join([v for v in tandapagar])

				data_id = data['id']
				file_id = data['file_id']

				title = data['title'].split()
				title = ' '.join([v for v in title])
				title = title.title()

				description = data['description']
				description = Translator().translate(description)

				thumbnail = data['thumbnail']
				genre = data['genre']

				release = data['release'].split('-')
				release = ' '.join([v for v in release])

				captions = f"""<pre>{title.title()} | {release} | {genre}</pre>\n\n[<b>Description</b>]\n{description} #{tandapagar}"""

				r = send_video(file_id = file_id, chat_id = chat_id, caption = captions)
				return r
			else:
				pass
