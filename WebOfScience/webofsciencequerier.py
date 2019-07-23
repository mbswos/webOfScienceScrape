import requests
import pprint
import dbconnection
import time

def set_params(query_name):
	params = {
		'databaseId':'WOS',
		'usrQuery':'AU=(' + query_name + ') AND OG=(University of Miami)',
		'count':100,
		'firstRecord':1
	}

	return params

url = 'https://api.clarivate.com/api/woslite'
headers = {
	'x-Apikey':'1040b7d68bca922c6e93e44a48c8cc3c909bc09f'
}

connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

professors = querier.get_professor_list()

total_data = 0
authors = 0

for prof in professors:

	last_name = prof[3]
	first_name = prof[1]
	query_name = last_name + ', ' + first_name[0] 

	params = set_params(query_name)
	time.sleep(1)
	raw = requests.get(url, params=params, headers=headers)
	data_dict = raw.json()

	if 'Data' in data_dict:
		prof_pub_count = data_dict['QueryResult']['RecordsFound']
		print(query_name + ':' + str(prof_pub_count))

		total_data += prof_pub_count
		if prof_pub_count > 0:
			authors+=1
			prof_pub_count -= len(data_dict['Data'])

			publications = data_dict['Data']
			for pub in publications:
				raw_pub_db_id = storer.store_web_of_science_raw_publication(pub)
				if raw_pub_db_id:
					pub_authors = pub['Author']['Authors']
					for author in pub_authors:
						storer.store_web_of_science_raw_author(raw_pub_db_id, author)

print(total_data)
print(authors)
connection.commit()
connection.disconnect()