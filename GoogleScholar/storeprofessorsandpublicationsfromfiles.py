import ast
import codecs
import os
from nameparser import HumanName
import dbconnection

path = 'GoogleScholar/textfiles/professors'
f = codecs.open('GoogleScholar/textfiles/Professors.txt', 'r')
connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

#assumes .txt is at the end
def parse_name_from_file_name(file_name):
	author_name_dashed = file_name[:-4]
	author_name = author_name_dashed.replace('-', ' ')
	name_object = HumanName(author_name)
	return name_object

def store_publications_list(publications_list, prof_db_id, storer):
	for publication in publications_list:
		pub_title = publication['bib']['title']
		pub_journal = publication['bib']['journal'] if 'journal' in publication['bib'] else ''
		pub_year = publication['bib']['year'] if 'year' in publication['bib'] else 0
		pub_volume = publication['bib']['volume'] if 'volume' in publication['bib'] else ''
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

professors_list = ast.literal_eval(f.read())
files = []

for filepath, d, file_names in os.walk(path):
    for file_name in file_names:
        if '.txt' in file_name and not file_name == 'Professors.txt' and not file_name == 'NotReadProfessors.txt':
            files.append((filepath,file_name))

for filepath, file_name in files:
	professor_file_name = str(filepath) + '/' + str(file_name)
	name_object = parse_name_from_file_name(file_name)
	for professor in professors_list:
		professor['name'] = professor['name'].replace('.','')
		prof_name_object = HumanName(professor['name'])
		if prof_name_object.first == name_object.first and prof_name_object.last == name_object.last:
			professor_object = professor
			break
	professor_db_id, google_professor_db_id = storer.store_prof_google_scholar(professor_object)
	professor_file = codecs.open(professor_file_name, 'r', 'utf-8')

	publications_list = ast.literal_eval(professor_file.read())
	store_publications_list(publications_list, professor_db_id, storer)

connection.commit()
connection.disconnect()
f.close()

