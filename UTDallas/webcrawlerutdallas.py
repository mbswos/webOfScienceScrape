import requests
from bs4 import BeautifulSoup
import dbstorer
from nameparser import HumanName

def get_name_and_affiliation(author_td):
	author = author_td.split(' - <b>')
	return author[0], author[1][:-4]

storer = dbstorer.DBStorer()
storer.connect()

post_url = 'https://jindal.utdallas.edu/the-utd-top-100-business-school-research-rankings/application/functions.php'

headers={
	
	'Host': 'jindal.utdallas.edu',
	'Connection': 'keep-alive',
	'Content-Length': '212',
	'Accept': 'text/html, */*; q=0.01',
	'Origin': 'https://jindal.utdallas.edu',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://jindal.utdallas.edu/the-utd-top-100-business-school-research-rankings/search',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Cookie': '__cfduid=d475257426da1b373a28b7fbaee3baaf11561124335; _ga=GA1.2.1564682643.1561124336; _gid=GA1.2.171154920.1561556024; utd1P=!LWP3H4DCYWxwjq2Q03aOO1iWpq8YlFS+fFzCbEM4spJZZiBBoXvQIz3vw2gBfcYHZmiIxoOa0KniKlo=; _gcl_au=1.1.1390954278.1561556072; UTDPHPSESSID=smcusrfqqm7ctklan86v5mqlu0; nmstat=1561556350431; _fbp=fb.1.1561556330215.537393654; WT_FPC=id=6c7aa53b-a832-421f-b85a-558ba1b3664a:lv=1561549131457:ss=1561548825383; _gat_UA-28425689-1=1'
}

post_info = {}
post_info['option'] = 'loadSearchResults'
post_info['id'] = 2
post_info['frmDate'] = 1990
post_info['toDate'] = 2019
post_info['journal_ids'] = [28,27,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,8,7,5,4,3,2,1,]
post_info['universities'] = [1774,]
post_info['applyAnd'] = 0

print(post_info)
post_data = requests.post(post_url, headers=headers, data = 'option=loadSearchResults&id=2&frmDate=1990&toDate=2019&journal_ids=28%2C27%2C24%2C23%2C22%2C21%2C20%2C19%2C18%2C17%2C16%2C15%2C14%2C13%2C12%2C11%2C10%2C8%2C7%2C5%2C4%2C3%2C2%2C1%2C&universities=1774%2C&applyAnd=0')

raw = post_data.text

html = BeautifulSoup(raw, 'html.parser')
body = html.find('tbody')
rows = body.find_all('tr')
for row in rows:
	tds = []
	cols = row.find_all('td')
	for col in cols:
		label = col.find('label')
		tds.append(str(label.decode_contents().strip()))
	journal = tds[0]
	title = tds[1]
	authors = tds[2].split('<br/>')[:-1]
	year = tds[3]
	volume = tds[4]

	publication_db_id = storer.get_publication_db_id(title, journal, year)
	if not publication_db_id == None:
		for author in authors:
			author_name_raw, affiliation = get_name_and_affiliation(author)
			author_name = HumanName(author_name_raw)

			storer.update_other_author_db_id_by_name(str(author_name), publication_db_id, affiliation)
	else:
		publication_db_id = storer.store_publication(journal, title, year, volume)
		for author in authors:
			author_name_raw, affiliation = get_name_and_affiliation(author)
			author_name = HumanName(author_name_raw)

			storer.store_other_author(author_name, publication_db_id, affiliation=affiliation)
			professor_db_id = storer.get_professor_db_id_by_name(str(author_name))
			if professor_db_id:
				storer.store_author_and_publication(professor_db_id, publication_db_id)
	storer.store_utdallas_publication(publication_db_id)
storer.commit()
storer.disconnect()
# Find the publication 
# If found update authors?
# If not make a new one
# For each author find the author and make a author_and_publication match
# Create a new UTDallas entry