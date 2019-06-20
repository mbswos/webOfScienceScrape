import scholarly
import codecs
import csv

#next() is search

# Initialize file
f = codecs.open('dumpFile.txt', 'w+', 'utf-8')
read_file = open('Professors.txt')


search_query = scholarly.search_author("Aboudi, Ronny")
author = next(search_query).fill()
print(1)
search_query = scholarly.search_author("Abril, Patricia S")
author = next(search_query).fill()
print(2)
search_query = scholarly.search_author("Agramonte, Amy")
author = next(search_query).fill()
print(3)
search_query = scholarly.search_author("Alexandrakis, Alexandros Platon")
author = next(search_query).fill()
print(4)

#read through each professor
for professor in read_file:
	# Retrieve the author's data, fill-in, and print
	print(professor)
	search_query = scholarly.search_author(professor.strip())
	author = next(search_query).fill()
	f.write(str(author))

	#for pub in author.publications:
	#	publication = pub.fill()
	#	f.write(str(publication))

f.close()