import scholarly
import dbstorer
import storeprofessor

storer = dbstorer.DBStorer()
storer.connect()

print('Searching for prof...')
search_string = 'Kumar, Alok'
search_query = scholarly.search_author(search_string)
prof = next(search_query).fill()

storeprofessor.storeprofessor(prof, storer)

storer.disconnect()
print('Stored procedures committed')