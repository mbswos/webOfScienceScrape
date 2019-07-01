import scholarly
import codecs

# Based on the system of scraping from google scholar (Defunct functionkinda)
def storeprofessor(professor, storer):
	print('Storing professor ' + professor.name)
	prof_db_id = storer.store_prof_google_scholar(professor)
	if prof_db_id:
		print('Stored professor:' + str(prof_db_id))
	else:
		prof_db_id = storer.get_professor_db_id(professor.id)

	print('Storing publications...')
	for publication in professor.publications:
		pub = publication.fill()
		pub_title = pub.bib['title']
		pub_journal = pub.bib['journal'] if 'journal' in publication.bib else ''
		pub_year = pub.bib['year'] if 'year' in publication.bib else ''
		pub_db_id = storer.store_publication_google_scholar(pub, prof_db_id)
		if not pub_db_id:
			pub_db_id = storer.get_publication_db_id(pub_title, pub_journal, pub_year)
		print('Publication id - ' + str(pub_db_id) + ': ' + pub_title)

	storer.commit()
	print('Professor and publications stored.')