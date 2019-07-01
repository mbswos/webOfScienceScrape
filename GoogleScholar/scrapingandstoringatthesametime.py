import scholarly
import codecs
import csv
import dbstorer
import storeprofessorandscrapepublication
import traceback

def createprofessorsearchstring(professors):
	string = 'Miami '
	for prof in professors:
		string += prof + ' OR '
	if string == 'Miami ':
		return ''
	string = string[:(len(string) - 4)]
	return string

def getprofessorlist():
	unread_professors = open('textfiles/NotReadProfessors.txt', 'r')
	professors_to_read = []
	for line in unread_professors:
		professors_to_read.append(line.strip())
	unread_professors.close()
	return professors_to_read

# Get a list of unread professors and prep the file to read
# Must be done in this order because we first read from the
# 	same file before writing to it
professors_to_store = getprofessorlist()
file = codecs.open('textfiles/NotReadProfessors.txt', 'w+', 'utf-8')

# Connect to the database and create a database writer
storer = dbstorer.DBStorer()
storer.connect()

# Store all the professors in the database
try:
	while True:
		# Get 11 professors and remove them from professors to store
		professors = professors_to_store[:11]
		del professors_to_store[:11]

		# Get the search string and print it
		# If the search string is empty, we've read all the professors!
		search_string = createprofessorsearchstring(professors)
		if search_string == '':
			break
		print(search_string)

		# Search Google Scholar for those professors 
		# Try to store those professors
		try:
			search_query = scholarly.search_author(search_string)
			for prof in search_query:
				professor = prof.fill()
				storeprofessorandscrapepublication.storeprofessor(professor, storer)

		# If we fail, store that list of 11 professors in a file
		except:
			for prof in professors:
				file.write(prof + '\n')
			print('Wrote professors we need to reread.')
			traceback.print_exc()
except:
	# Store all the professors we didn't even get to in a file
	for prof in professors_to_store:
		file.write(prof + '\n')
	print('Unread professors stored.')
	traceback.print_exc()
storer.disconnect()
