import scholarly
import codecs
import csv
import storeprofessor
import traceback
import ast

def getprofessorlist():
	unread_professors = open('textfiles/professors/NotReadProfessors.txt', 'r')
	professors_to_read = []
	for line in unread_professors:
		professors_to_read.append(line.strip())
	unread_professors.close()
	return professors_to_read

def createprofessorsearchstring(professors):
	string = 'Miami '
	for prof in professors:
		string += prof + ' OR '
	if string == 'Miami ':
		return ''
	string = string[:(len(string) - 4)]
	return string

def storeprofessor(professor):
	print(professor.name)

	profstripped = "-".join(professor.name.split())
	file_name = profstripped.replace(',','')
	file_name = file_name.replace('.','')
	prof_file = codecs.open('textfiles/professors/' + file_name + '.txt', 'w+', 'utf-8')
	all_publications = []
	for publication in professor.publications:
		try:
			print(publication.bib['title'])
			pub = publication.fill()
			if 'abstract' in pub.bib:
				pub.bib['abstract'] = str(pub.bib['abstract'])
			all_publications.append(ast.literal_eval(str(pub)))
		except:
			if 'abstract' in pub.bib:
				pub.bib['abstract'] = str(pub.bib['abstract'])
			all_publications.append(ast.literal_eval(str(publication)))

	coauthors = []
	for co in professor.coauthors:
		coauthors.append(co.name)
	professor.coauthors = coauthors
	professor.publications = []
	fileprof.write(str(professor) + ',\n')

	prof_file.write(str(all_publications))
	prof_file.close()

# Get a list of unread professors and prep the file to read
# Must be done in this order because we first read from the
# 	same file before writing to it
professors_to_store = getprofessorlist()
file = codecs.open('textfiles/professors/NotReadProfessors.txt', 'w+', 'utf-8')
filenotreadpubs = codecs.open('textfiles/NotReadPublications.txt', 'w+', 'utf-8')
fileprof = codecs.open('textfiles/professors/Professors.txt', 'w+', 'utf-8')
fileprof.write('[')

# Store all the professors in the files
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
		# Try to store those professors in a file
		try:
			search_query = scholarly.search_author(search_string)
			for prof in search_query:
				professor = prof.fill()
				storeprofessor(professor)

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
fileprof.write(']')

fileprof.close()
file.close()