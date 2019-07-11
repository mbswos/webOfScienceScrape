import requests
import dbconnection
from bs4 import BeautifulSoup

connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

url = 'https://jindal.utdallas.edu/the-utd-top-100-business-school-research-rankings/index.php'
data = requests.get(url)
raw = data.text

html = BeautifulSoup(raw, 'html.parser')
journal_div = html.find('div', {'class':'listJournals'})
count = 0
for journal in journal_div.find_all('a'):
	url = journal['href'].strip()
	journal_name = journal.div['title']
	year_since_raw = journal.div.div.get_text()
	year = int(year_since_raw[8:].strip())
	print(url)
	print(journal_name)
	print(year)
	print()

	journal_db_id = storer.store_journal(journal_name)
	if not journal_db_id:
		journal_db_id = querier.get_journal_db_id_by_name(journal_name)

	storer.store_journal_utdallas(journal_db_id, year, url)
	count+=1

connection.commit()
connection.disconnect()
print(count)
