import scholarly
import codecs
import csv

#next() is search

# Initialize file
f = codecs.open('textfiles/dumpFile.txt', 'w+', 'utf-8')
read_file = open('textfiles/Professors.txt')
unread_professors = open('textfiles/NotReadProfessors.txt', 'w+')

search_string = "Miami "
for i in range(11):
	professor = read_file.readline()
	prof = professor.strip()
	search_string = search_string + prof + " OR "

search_string = search_string[:(len(search_string) - 4)]

print(search_string)
search_query = scholarly.search_author(search_string)
print(search_query)

#read through each professor
for professor in read_file:
	# Retrieve the author's data, fill-in, and print
	search_query = scholarly.search_author(professor.strip())
	try:
		author = next(search_query).fill()
		f.write(str(author))
		for pub in author.publications:
			f.write(str(pub))
		print(professor.strip())

	except:
		err_message = professor.strip() + " was blocked."
		print(err_message)
		unread_professors.write(str(professor))

	#for pub in author.publications:
	#	publication = pub.fill()
	#	f.write(str(publication))

f.close()