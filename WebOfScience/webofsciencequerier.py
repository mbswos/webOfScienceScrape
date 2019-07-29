import requests
import pprint
import dbconnection
import time

url = 'https://api.clarivate.com/api/woslite'
headers = {
	'x-Apikey':'1040b7d68bca922c6e93e44a48c8cc3c909bc09f'
}

def set_params(prof_query_name, first_record):
	params = {
		'databaseId':'WOS',
		'usrQuery':'AU=(' + prof_query_name + ') AND OG=(University of Miami)',
		'count':100,
		'firstRecord':first_record
	}

	return params

def get_data(prof_query_name, first_record):
	params = set_params(prof_query_name, first_record)
	time.sleep(1)
	raw = requests.get(url, params=params, headers=headers)
	data_dict = raw.json()

	return data_dict

def get_all_data(prof_query_name):
	first_record = 1
	data_dict = get_data(prof_query_name,first_record)
	if 'Data' in data_dict:
		prof_pub_count = data_dict['QueryResult']['RecordsFound']
		pub_count_to_read = prof_pub_count
		pub_count_to_read -= len(data_dict['Data'])

		while pub_count_to_read > 0:
			first_record+=100
			more_data = get_data(prof_query_name, first_record)
			data_dict['Data'].extend(more_data['Data'])
			pub_count_to_read -= len(more_data['Data'])
	return data_dict, prof_pub_count

def create_prof_query_name(last_name, first_name):
	return last_name + ', ' + first_name[0] 

def store_publications(publications):
	for pub in publications:
		raw_pub_db_id = storer.store_web_of_science_raw_publication(pub)
		if raw_pub_db_id:
			pub_authors = pub['Author']['Authors']
			for author in pub_authors:
				storer.store_web_of_science_raw_author(raw_pub_db_id, author)

# query
connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

professors = querier.get_professor_list()

total_data = 0
authors_with_pubs = 0
authors_found = 0

for prof in professors:

	last_name = prof[3]
	first_name = prof[1]
	prof_query_name = create_prof_query_name(last_name, first_name)
	data_dict, prof_pub_count = get_all_data(prof_query_name)

	print(prof_query_name + ':' + str(prof_pub_count))
	authors_found+=1
	if prof_pub_count:
		publications = data_dict['Data']
		store_publications(publications)

		# Do some statistics
		total_data += prof_pub_count
		if prof_pub_count > 0:
			authors_with_pubs+=1

print(total_data)
print(authors_with_pubs)
print(authors_found)
connection.commit()
connection.disconnect()