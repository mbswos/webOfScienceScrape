from bs4 import BeautifulSoup
import os
from nameparser import HumanName
import ast
import codecs
import dbconnection

cv_path = 'CurriculumVitae/HTMLPages'
google_path = 'GoogleScholar/textfiles/professors'

# Find html page that matches a google scholar txt file
# Take last name, if it matches something in the professor's list check if we have a first name.
# If first names match, find the google scholar txt file.
# Scan each publication title and match it with the html page. If the html page contains that title
# Store those publications if the google scholar id is not in the googe scholars table
	
def get_name_from_cv_html_file(file_name):
	raw_name = file_name[:-8]
	names = raw_name.split('-')
	new_names = []
	for name in names:
		new_names.append(name.split('_'))
	last_name = '-'.join(new_names[len(new_names)-1])
	first_name = new_names[0][0] if len(new_names) > 1 else None
	middle_name = new_names[1][0] if len(new_names) == 3 else None

	return first_name, middle_name, last_name

def name_is_in_names_list(names_list, first_name, middle_name, last_name):
	matches = False
	for name in names_list:
		first_matches = not first_name or name.first.lower() == first_name.lower() 
		last_matches = name.last.lower() == last_name.lower()
		if first_matches and last_matches:
			return True, name
	return matches, None

f = open('CSVOfAllBusinessProfessors/Professors.txt', 'r')
connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier
professor_name_list = []
for professor_name in f:
	corrected_professor_name = professor_name.strip().replace('"', '')
	professor_name_list.append(HumanName(corrected_professor_name))

files = []
pubs_to_check = []

for filepath, d, file_names in os.walk(cv_path):
	for file_name in file_names:
		if '-cv.html' in file_name:
			first, middle, last = get_name_from_cv_html_file(file_name)
			is_in_list, professor_name_object = name_is_in_names_list(professor_name_list, first, middle, last)
			if is_in_list:
				file = open(cv_path + '/' + file_name, 'r', encoding='utf8')
				data = BeautifulSoup(file, 'html.parser').get_text()
				if data:
					data = data \
						.replace(u'\u2018', '\'') \
						.replace(u'\u2019', '\'') \
						.replace(u'\u201c', '"') \
						.replace(u'\u201d', '"') \
						.replace(u'\u2010', '-') \
						.replace(u'\u2011', '-') 
				file.close()

				professor_db_id = querier.get_professor_db_id_by_name(professor_name_object.full_name)
				if professor_db_id:
					storer.store_author_html_cv(professor_db_id, data)
				else:
					print(file_name)
			else:
				print(file_name)
				first = first or ''
				middle = middle or ''
				print(first + ' ' + middle + ' ' + last)
				print()

connection.commit()
connection.disconnect()
