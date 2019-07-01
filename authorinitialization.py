from nameparser import HumanName
import dbstorer

storer = dbstorer.DBStorer()
storer.connect()
unread_professors = open('CSVOfAllBusinessProfessors/Professors.txt', 'r')

for prof_name in unread_professors:
	prof_name_stripped = prof_name.strip()[1:len(prof_name)-2]
	name = HumanName(prof_name_stripped)
	storer.store_author(name)
storer.commit()
storer.disconnect()
unread_professors.close()