import requests
import RateMyProfessorsScrape.RMPClass
import ast
import dbconnection

connection = dbconnection.DBConnection()
storer = connection.storer

f = open('RateMyProfessorsScrape/ProfessorListDump.txt', 'r')
professors = ast.literal_eval(f.read())
f.close()
print(len(professors))

for professor in professors:
	tid = professor['tid']
	professor_name = professor['tLname'].strip() + '_' + professor['tFname'].strip().replace('"', '&')
	print(professor_name)

	rate_my_prof_db_id = storer.store_rate_my_professors_professor(professor)

	path = 'RateMyProfessorsScrape/professors/' + professor_name + '.txt'
	f = open(path, 'r')
	student_ratings = ast.literal_eval(f.read())
	f.close()

	for student_rating in student_ratings:
		if not isinstance(student_rating, str):
			storer.store_rate_my_professors_student_rating(student_rating, rate_my_prof_db_id)

connection.commit()
connection.disconnect()
