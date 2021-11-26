from telethon import TelegramClient, events, errors, utils
from telethon.tl.custom import Button
from telethon.sessions import StringSession
from telethon.tl.types import (
	DocumentAttributeVideo, 
	DocumentAttributeAudio, 
	DocumentAttributeFilename
)
from telethon.sync import TelegramClient
from telethon.tl import types
from malikamovie.FastTelethon import download_file, upload_file
from icecream import ic as ICE
import requests, time, bs4, asyncio
import malikamovie.conf as CONF
import uuid, os

import logging
logging.basicConfig(level = logging.INFO)
ICE.configureOutput(prefix = '[kang_upload] ')
super_user = CONF.SU
class Timer:
	def __init__(self, time_between=2):
		self.start_time = time.time()
		self.time_between = time_between

	def can_send(self):
		if time.time() > (self.start_time + self.time_between):
			self.start_time = time.time()
			return True
		return False
	
class FilmApeek:
	datas = []
	dataDicts = {}
	
	def __init__(self, client: TelegramClient, query: str, chat_id: int):
		self.client = client
		self.query = query
		self.chat_id = chat_id
		
	def OnGettingUrl(self, URL: str):
		session = requests.Session()
		BS = bs4.BeautifulSoup
		host = '103.194.171.18'
		r = session.get(URL, headers =  {
		"Host":"103.194.171.18",
		"user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
		"accept":"image/webp,image/apng,image/*,*/*;q=0.8",
		"referer":'http://' + host + '/',
		"accept-encoding":"gzip, deflate, br",
		"accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
		"cookie":"_ga=GA1.2.66331305.1628932089",
		"cookie":"_gid=GA1.2.1804048429.1628932089"
		})
		text = r.text
		soup = BS(text, 'html.parser')
		meta = soup.find_all('meta')
		title = soup.find('title')
		ICE(text)
		if title:
			self.dataDicts['title'] = (title.string).split('|')[0]
		for m in meta:
			try:
				content = m.get('content')
				if content.endswith('.jpg') and 'amazon.com' in content:
					self.dataDicts['image'] = content
				if ('genre' in content.lower()):
					self.dataDicts['description'] = content.split('LK21')[0]
			except AttributeError:
				pass
			except Exception as er:
				ICE(er)
		return self.dataDicts
				
	def SearchApik(self, query: str):
		host = '103.194.171.232'
		baseUrl = 'http://' + host + '/?s=' + query
		r = requests.post(baseUrl, headers={
		"Host":"103.194.171.18",
		"user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
		"accept":"image/webp,image/apng,image/*,*/*;q=0.8",
		"referer":'http://' + host + '/',
		"accept-encoding":"gzip, deflate, br",
		"accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
		"cookie":"_ga=GA1.2.66331305.1628932089",
		"cookie":"_gid=GA1.2.1804048429.1628932089"
		})
		soup = bs4.BeautifulSoup(r.text, 'html.parser')
		aTag = soup.find_all('a')
		
		urls = []
		newUrls = []
		datas = {}
		i=0
		for a in aTag:
			href = a.get('href')
			hrefSplit = href.split('/')
			if 'http' in href and len(hrefSplit) >= 4 and not 'page' in hrefSplit[3] and not 'tvshows' in hrefSplit[3]:
				if hrefSplit[2] == host:
					pass
				else:
					data = {}
					title = (href.split('/')[-1]).replace('-', ' ').upper()
					data['url'] = href
					data['title'] = title
					data['id'] = i
					i+=1
					urls.append(data)
			datas['results'] = urls
		return datas
				
	async def Uploader(self, filename: str, title: str):
		try:
			msg = await self.client.send_message(self.chat_id, "Uploading..")
			with open(filename, "rb") as out:
				res = await upload_file(self.client, out, title)
				attributes, mime_type = utils.get_attributes(
				filename,
				)
				media = types.InputMediaUploadedDocument(
				file=res,
				mime_type=mime_type,
				attributes=attributes,
				force_file=False
				)
				await msg.delete()
				ICE(media)
				return media
		except OSError:
			await self.client.send_file(self.chat_id, filename)
		except Exception as er:
			ICE(er)


	async def GetFilmShort(self, inputReferer: str):
		data = {}
		host = '103.194.171.232'
		r = requests.get(inputReferer, headers={
		"Host":"103.194.171.18",
		"user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
		"accept":"image/webp,image/apng,image/*,*/*;q=0.8",
		"referer":inputReferer,
		"accept-encoding":"gzip, deflate, br",
		"accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
		"cookie":"_ga=GA1.2.66331305.1628932089",
		"cookie":"_gid=GA1.2.1804048429.1628932089"
		})
		soup = bs4.BeautifulSoup(r.text, 'html.parser')
		this_frame = soup.find_all('iframe')
		aTag = soup.find_all('a')
		
		urls = []
		newUrls = []
		for a in aTag:
			url = a.get('href')
			if 'https' in url and not 'www.youtube.com' in url:
				if url.split('/')[2] == host:
					pass
				else:
					urls.append(url)
		data['urls'] = urls
		for url in data['urls']:
			payload = {'url':url}
			r = requests.post('http://ik-a.herokuapp.com', json=payload)
			assert r.status_code == 200, "Error: shortener"
			newUrl = r.json()['url']
			newUrls.append(newUrl)
		data['newUrls'] = newUrls
		for frame in this_frame:
			try:
				src = frame.get('src')
				if 'fa.efek.stream' in src:
					data['referer'] = src
					ICE(src)
			except:
				pass
		referer = data['referer']
		thisId = referer.split('/')[-2]
		thisReso = (referer.split('/')[-1]).split('&')[0]
		r = (requests.get(f'https://fa.efek.stream/stream/{thisReso}/{thisId}/__001', headers={
		"Host":"fa.efek.stream",
		"accept-encoding":"identity;q=1, *;q=0",
		"user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
		"accept":"*/*",
		"referer":referer,
		"accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
		"cookie":"PHPSESSID=u1l54jl8fmt5h84trcpqpqv9e9",
		"cookie":"_ga=GA1.2.1434219329.1628932106",
		"cookie":"_gid=GA1.2.268446481.1628932106",
		"cookie":"_gat_gtag_UA_172750999_1=1","range":"bytes=0-"
		}, allow_redirects=False).headers['location'])
		
		session = requests.Session()
		r2 = session.get(r, headers={
		"Host":"lbhz23.efek.stream",
		"accept-encoding":"identity;q=1, *;q=0",
		"user-agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 4X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
		"accept":"*/*",
		"referer":"https://fa.efek.stream/",
		"accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
		"cookie":"_ga=GA1.2.1434219329.1628932106",
		"cookie":"_gid=GA1.2.268446481.1628932106",
		"cookie":"_gat_gtag_UA_172750999_1=1"
		})
		title = inputReferer.split('/')[-2] + '.mp4'
		with open(title, 'wb') as fd:
			fd.write(r2.content)
		data['filename'] = title
		media = await self.Uploader(title, title)
		data['media'] = media
		return data

	async def Peek(self):
		query = self.query
		if ' ' in query:
			query = query.replace(' ', '-')
			
		fullUrl = f"http://103.194.171.18/{query}/play"
		reQuery = query.replace('-', ' ')
		msg = await self.client.send_message(self.chat_id, f'__Searching..__ {reQuery}')
		try:
			dataDicts = self.OnGettingUrl(fullUrl)
			ICE(dataDicts)
			r= requests.get(dataDicts['image'])
			assert r.status_code == 200, ""
			with open(f"{query}.jpg", "wb") as f:
				f.write(r.content)
			title = dataDicts['title']
			title = title.replace('Nonton Film ', '')
			title = title.replace('Subtitle Indonesia', '')
			description = "\n".join([i for i in dataDicts['description'].split('|')])
			synopsis = description.split('Genre')[0]
			synopsis = synopsis.split('. ')
			synopsis.pop(0)
			synopsis = '. '.join([v for v in synopsis])
			Genre = (description.split('Genre')[1]).split('Durasi')[0]
			Genre = Genre.split('Negara')[0]
			warningMessage = CONF.warningMessage
			await msg.edit(f"**Extracting..** __takes 5 - 6 minutes streaming time__")
			executeApik = await self.GetFilmShort(fullUrl)
			file = executeApik['media']
			await msg.edit(f"**{title}** Extracted..")
			listLink = executeApik['newUrls']
			dataLink = []
			for i in range(len(listLink) - 1):
				i+=1
				link = listLink[i]
				link = f"👉 <a href='{link}'>Link {i}</a>"
				dataLink.append(link)
			links = ' | '.join([v for v in dataLink])
			captions = f"<b>{title}</b>\n\n<b>[Synopsis]</b>\n{synopsis}\n\n<b>[Genre]</b> {Genre}{warningMessage}\n<b>[Full Movie]</b>\n{links}"
			await self.client.send_file(
				self.chat_id, 
				file,thumb = f"{query}.jpg",
				caption = captions,
				parse_mode = 'html'
			)
			await msg.delete()
		except KeyError:
			data = []
			try:
				query = query.replace('-', '+')
				lookWhatIFound = self.SearchApik(query)
				for i in range(len(lookWhatIFound['results'])):
					url = lookWhatIFound['results'][i]['url']
					title = lookWhatIFound['results'][i]['title']
					ICE(title)
					i+=1
					text = f"[{title}]({url})"
					data.append(text)
				texts = '\n'.join([val for val in data])
				reQuery = query.replace('+', ' ')
				ICE(texts)
				await self.client.send_message(self.chat_id, f'**Found** nothing with keyword **{reQuery}** \n\nBut hey! look what i found instead :\n{texts} ')
				await msg.delete()
			except Exception as er:
				ICE(er)
		except Exception as er:
			ICE(er)
			await msg.delete()
			await self.client.send_message(self.chat_id, f"{reQuery} is not **Found**")
			
async def main(query: str, chat_id: int):
	api_id = CONF.APP2['api_id']
	api_hash = CONF.APP2['api_hash']
	SESSION_STRING = CONF.APP2['session_string']
	client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)
	async with client:
		client.start()
		client.run_until_disconnected()
		if client:
			P = FilmApeek(client, query.lower(), chat_id)
			await P.Peek()