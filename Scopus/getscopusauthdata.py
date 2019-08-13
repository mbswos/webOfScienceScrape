from bs4 import BeautifulSoup
import requests
from requests import Session


# file = open('Scopus/professorsauid.html', 'r', encoding='utf8')
# soup = BeautifulSoup(file, 'html.parser')
# professors_html = soup.find_all('input', {"class": "overlaycloseCheck"})
# professors_list = list(professors_html)
# for professor in professors_list:
# 	print(professor['value'])
session = requests.Session()
cookies = session.cookies.get_dict()
#response = session.get('https://www.scopus.com/standard/viewMore.uri')
response = requests.get("https://www.scopus.com/search/form/authorFreeLookup.uri")
print(session.cookies.get_dict())
print(response)


# alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
# "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# for letter in alph:
# 	response = session.post(
# 	    url='http://sportsbeta.ladbrokes.com/view/EventDetailPageComponentController',
# 	    data={
# 			'clusterDisplayCount':'260',
# 			'sot': 'a',
# 			'navigatorName': 'AUTHOR_NAME_AND_ID',
# 			'clusterCategory': 'selectedAuthorClusterCategories',
# 			's': 'AF-ID("University of Miami" 60029251) AND SUBJAREA(busi)',
# 			'sid': '1006d0cd0692a3d8a41fc7f99753cd55',
# 			'sdt': 'a',
# 			'sort': 'plf-f',
# 			'origin': 'resultslist',
# 			'scla': letter,
# 			'src': 's',
# 			'offset': '1',
# 			'isRebrandLayout': 'true'
# 	    },
# 	    headers={
# 			':authority': 'www.scopus.com',
# 			':method': 'POST',
# 			':path': '/standard/viewMore.uri',
# 			':scheme': 'https',
# 			'accept': '*/*',
# 			'accept-encoding': 'gzip, deflate, br',
# 			'accept-language': 'en-US,en;q=0.9',
# 			'content-length': '455',
# 			'content-type': 'application/x-www-form-urlencoded',
# 			'cookie': ,
# 			'origin: https':'//www.scopus.com',
# 			'referer: https':'//www.scopus.com/results/results.uri?sort=plf-f&src=s&sid=1006d0cd0692a3d8a41fc7f99753cd55&sot=a&sdt=a&sl=56&s=AF-ID%28%22University+of+Miami%22+60029251%29+AND+SUBJAREA%28busi%29&origin=searchadvanced&editSaveSearch=&txGid=c925c55a64c40a4d1e713b924d378b15',
# 			'sec-fetch-mode': 'cors',
# 			'sec-fetch-site': 'same-origin',
# 			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
# 			'x-newrelic-id': 'VQQPUFdVCRADVVVXAwABVA=='
# 	    }
# 	)

# print response.text