import requests, uuid
from bs4 import BeautifulSoup as BS
from threading import *
import logging

logging.basicConfig(level = logging.DEBUG)

class MovieLink:
	host = 'filmapik.today' #'103.194.171.232'
	baseUrl = f"http://{host}"
	headers={
			'authority':'filmapik.today',
			'cache-control':'max-age=0',
			'sec-ch-ua':'"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
			'sec-ch-ua-mobile':'?1',
			'sec-ch-ua-platform':'"Android"',
			'upgrade-insecure-requests':'1',
			'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
			'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'sec-fetch-site':'none',
			'sec-fetch-mode':'navigate',
			'sec-fetch-user':'?1',
			'sec-fetch-dest':'document',
			'accept-language':'en-US,en;q=0.9',
			'cookie':'_ga=GA1.1.1947761994.1634526077; _gid=GA1.1.1271674786.1634526077; _gat_gtag_UA_102649030_1=1'
	}
	def __init__(self):
		pass
		
	def GetFileName(self, belakang):
		UUID = str(uuid.uuid4()).split('-')[-1] + belakang
		return UUID
		
	def SearchApik(self, query):
		URL = self.baseUrl + '/?s=' + query
		r = requests.post(URL)
		soup = BS(r.text, 'html.parser')
		aTag = soup.find_all('a')
		urls = []
		newUrls = []
		datas = {}
		i=0
		for a in aTag:
			href = a.get('href')
			hrefSplit = href.split('/')
			if 'http' in href and len(hrefSplit) >= 4 and not 'page' in hrefSplit[3] and not 'tvshows' in hrefSplit[3]:
				data = {}
				title = (href.split('/')[-1]).replace('-', ' ').upper()
				data['url'] = href
				data['title'] = title
				data['id'] = i
				i+=1
				urls.append(data)
			datas['results'] = urls
		return datas
		
	def GettingUrl(self, fullUrl):
		dataDicts = {}
		class One(Thread):
			def run(self):
				with requests.Session() as session:
					r = session.get(fullUrl + '/play', headers=MovieLink.headers)
					soup = BS(r.text, 'html.parser')
					meta = soup.find_all('meta')
					title = soup.find('title')
					if title:
						dataDicts['title'] = (title.string).split('|')[0]
					for m in meta:
						try:
							content = m.get('content')
							if content.endswith('.jpg') and 'amazon.com' in content:
								dataDicts['image'] = content
							if ('genre' in content.lower()):
								print(content)
								dataDicts['description'] = content.split('LK21')[0]
						except AttributeError:
							pass
						except Exception as er:
							print(er)
			
		class Two(Thread):
			def run(self):
				r = requests.get(fullUrl + '/play', headers=MovieLink.headers)
				soup = BS(r.text, 'html.parser')
				aTag = soup.find_all('a')
				urls = []
				newUrls = []
				for a in aTag:
					try:
						url = a.get('href')
						if 'https' in url:
							if url in urls:
								pass
							urls.append(url)
					except:
						pass
				dataDicts['urls'] = urls
				for url in dataDicts['urls']:
					urlSplit = url.split('/')
					if not 'http' in url and len(urlSplit) < 4:
						pass
					if url.split('/')[2] == MovieLink.host:
						pass
					elif url.split('/')[2] == 'youtube.com':
						pass
					else:
						payload = {'url':url}
						r = requests.post('http://ik-a.herokuapp.com', json=payload)
						assert r.status_code == 200, "Error: shortener"
						newUrl = r.json()['url']
						newUrls.append(newUrl)
				dataDicts['newUrls'] = newUrls
		t = One()
		t_ = Two()
		t.start()
		t_.start()
		t.join()
		t_.join()
		return dataDicts
