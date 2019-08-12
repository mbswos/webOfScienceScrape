import requests
import pprint
import dbconnection
import time

url = 'https://api.clarivate.com/api/woslite'
headers = {
	'x-Apikey':'1040b7d68bca922c6e93e44a48c8cc3c909bc09f'
}

def create_all_professor_query_strings(professors):
	prof_query_string_1 = ''
	prof_query_string_2 = ''
	prof_list1 = professors[:100]
	prof_list2 = professors[100:]
	for prof in prof_list1:
		last_name = prof[3]
		first_name = prof[1]
		name = create_prof_query_name(last_name, first_name)
		prof_query_string_1 += 'AU=(' + name + ') OR '
	prof_query_string_1 = '(' + prof_query_string_1[:-3] + ') AND OG=(University of Miami)'

	for prof in prof_list2:
		last_name = prof[3]
		first_name = prof[1]
		name = create_prof_query_name(last_name, first_name)
		prof_query_string_2 += 'AU=(' + name + ') OR '
	prof_query_string_2 = '(' + prof_query_string_2[:-3] + ') AND OG=(University of Miami)'
	return prof_query_string_1, prof_query_string_2

def get_all_professor_data(prof_query_string):
	first_record = 1
	data_dict = get_data(prof_query_string,first_record)

	if 'Data' in data_dict:
		prof_pub_count = data_dict['QueryResult']['RecordsFound']
		pub_count_to_read = prof_pub_count
		pub_count_to_read -= len(data_dict['Data'])

		while pub_count_to_read > 0:
			first_record+=100
			more_data = get_data(prof_query_string, first_record)
			data_dict['Data'].extend(more_data['Data'])
			pub_count_to_read -= len(more_data['Data'])
	return data_dict

def set_all_params(prof_query_string, first_record):
	params = {
		'databaseId':'WOS',
		'usrQuery':prof_query_string,
		'count':100,
		'firstRecord':first_record
	}

	return params

def get_data(prof_query_string, first_record):
	print(prof_query_string)
	params = set_all_params(prof_query_string, first_record)
	time.sleep(1)
	raw = requests.get(url, params=params, headers=headers)
	print(raw)
	data_dict = raw.json()

	return data_dict

def create_prof_query_name(last_name, first_name):
	return last_name + ', ' + first_name[0] 

connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

professors = querier.get_professor_list()
prof_query_string_1, prof_query_string_2 = create_all_professor_query_strings(professors)
data_dict = get_all_professor_data(prof_query_string_1)
data_dict2 = get_all_professor_data(prof_query_string_2)

print(data_dict)
print(data_dict2)
print(len(data_dict['Data']))
print(len(data_dict2['Data']))

connection.disconnect()