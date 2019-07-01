from nameparser import HumanName
import dbstorer

storer = dbstorer.DBStorer()
storer.connect()
unread_professors = open('textfiles/Professors.txt', 'r')

for prof_name in unread_professors:
	name = HumanName(prof_name)
	storer.store_author(name)

storer.disconnect()
unread_professors.close()