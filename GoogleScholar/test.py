import scholarly
import codecs
import csv
import dbstorer

storer = dbstorer.DBStorer()
storer.connect()

print('Searching for prof')
search_string = 'Cronqvist, Henrik'
search_query = scholarly.search_author(search_string)
prof = next(search_query).fill()
print('Prof found')
print(prof.name)
prof_db_id = storer.get_professor_db_id(prof.id)
storer.store_cites_per_year(prof.cites_per_year, prof_db_id)
storer.commit()
storer.disconnect()
print('Stored procedures committed')