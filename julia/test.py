import requests
from icecream import ic
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

			ic(self.data)
			return self.data
		except Exception as e:
			return e