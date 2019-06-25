import scholarly
import codecs
import dbstorer

storer = dbstorer.DBStorer()
storer.connect()

print('Searching for prof...')
search_string = 'Cronqvist, Henrik'
search_query = scholarly.search_author(search_string)
prof = next(search_query).fill()
print('Prof found: ' + prof.name)
print('Storing prof...')
prof_db_id = storer.store_prof(prof)
if prof_db_id:
	print('Stored prof:' + str(prof_db_id))
else:
	prof_db_id = storer.get_professor_db_id(prof.id)

print('Storing publications...')
for publication in prof.publications:
	pub = publication.fill()
	pub_title = pub.bib['title']
	pub_journal = pub.bib['journal'] if 'journal' in publication.bib else ''
	pub_db_id = storer.store_publication(pub, prof_db_id)
	if not pub_db_id:
		pub_db_id = storer.get_publication_db_id(pub_title, pub_journal)
	print('Publication id - ' + str(pub_db_id) + ': ' + pub_title)

storer.commit()
storer.disconnect()
print('Stored procedures committed')