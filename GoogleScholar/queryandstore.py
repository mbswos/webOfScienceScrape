import signal
import dbconnection
import scholarly
from func_timeout import func_timeout, FunctionTimedOut
from nameparser import HumanName

connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier
wait_time_secs = 60

def generate_name_variants(professor_list):
	professor_name_variant_list = []
	for prof in professor_list:
		last_name = prof[3]
		professor_name_variant_list.append(last_name)
		if '-' in last_name:
			for name_part in last_name.strip().split('-'):
				professor_name_variant_list.append(name_part)
	return professor_name_variant_list

def split_list_into_chunks(name_list, chunk_size):
    for i in range(0, len(name_list), chunk_size):
        yield name_list[i:i + chunk_size]

def generate_query_strings(professor_name_variants):
	name_list_chunks = split_list_into_chunks(professor_name_variants, 11)
	query_strings = []
	for name_list in name_list_chunks:
		string = 'Miami '
		for prof_name in name_list:
			string += '"' + prof_name + '" OR '
		if string == 'Miami ':
			return ''
		string = string[:(len(string) - 4)]
		query_strings.append(string)
	return query_strings

def generate_professor_objects(query_strings):
	professor_objects = []
	for query_string in query_strings:
		search_query = scholarly.search_author(query_string)
		for professor in search_query:
			print(professor.name)
			professor_objects.append(professor.fill())
	return professor_objects

def handler(signum, frame):
	raise Exception('Time out: ' + wait_time_secs)

def store_publications_list(publications_list, prof_db_id, storer, querier):
	for publication in publications_list:
		print(publication['title'])
		publication = publication.fill()
		pub_title = publication['bib']['title']
		pub_journal = publication['bib']['journal'] if 'journal' in publication['bib'] else ''
		pub_year = publication['bib']['year'] if 'year' in publication['bib'] else 0
		pub_volume = publication['bib']['volume'] if 'volume' in publication['bib'] else ''

		pub.bib['abstract'] = str(pub.bib['abstract']) if 'abstract' in pub.bib else ''

		pub_db_id = querier.get_publication_db_id(pub_title, pub_journal, pub_year)
		raw_id = storer.store_raw_publication_google_scholar(prof_db_id, str(publication))

		if not pub_db_id:
			pub_db_id = storer.store_publication(pub_title, pub_journal, pub_year, pub_volume)
			if pub_db_id:
				storer.store_author_and_publication(prof_db_id, pub_db_id)	

		if raw_id and pub_db_id:
			storer.store_raw_and_publication_google_scholar(pub_db_id, raw_id)

		db_ids = storer.store_publication_google_scholar(publication, prof_db_id)
		if db_ids:
			pub_db_id, google_pub_db_id = db_ids


def store_professor(professor, storer):
	print(professor.name)
	professor.publications = []
	coauthors = []
	for co in professor.coauthors:
		coauthors.append(co.name)
	professor.coauthors = coauthors
	professor_db_id, google_professor_db_id = storer.store_prof_google_scholar(professor)
	return professor_db_id

def store_professor_objects_and_publications(professor_objects, storer, querier):
	not_stored_professor_objects = []
	for professor in professor_objects:
		professor_publications = professor.publications
		professor_db_id = store_professor(professor, storer)
		if professor_db_id:
			try:
				func_timeout(wait_time_secs, store_publications_list, args=(professor_publications, professor_db_id, storer, querier))
			except:
				not_stored_professor_objects.append(professor)
		else:
			not_stored_professor_objects.append(professor)

	return not_stored_professor_objects


def query_and_store_google_scholar_professors(professor_list, storer, querier):
	professor_name_variants = generate_name_variants(professor_list)
	query_strings = generate_query_strings(professor_name_variants)
	professor_objects = generate_professor_objects(query_strings)
	not_stored_professor_objects = store_professor_objects_and_publications(professor_objects, storer, querier)
	return not_stored_professor_objects

professor_list = querier.get_professor_list()
not_stored_professors = query_and_store_google_scholar_professors(professor_list, storer, querier)
print('Not stored professors: ')
for prof in not_stored_professors:
	print(prof.name)
connection.commit()
connection.disconnect()