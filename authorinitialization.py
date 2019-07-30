from nameparser import HumanName
import dbconnection

connection = dbconnection.DBConnection()
storer = connection.storer
unread_professors = open('MiamiBusinessSchool/Professors.txt', 'r')

for prof_name in unread_professors:
	prof_name_stripped = prof_name.strip()[1:len(prof_name)-2]
	name = HumanName(prof_name_stripped)
	storer.store_author(name)
connection.commit()
connection.disconnect()
unread_professors.close()