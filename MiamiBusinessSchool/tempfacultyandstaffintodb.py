import dbconnection
import csv
import os
from nameparser import HumanName

connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

inputdir = 'MiamiBusinessSchool\\DepartmentCSVs'
total = 0
for csvs in os.listdir(inputdir):
	print(csvs)
	csvfile = open('MiamiBusinessSchool/DepartmentCSVs/'+csvs, 'r')
	csvs = csvs.replace('.csv','')
	department_id = storer.store_department(csvs)
	department = csv.DictReader(csvfile, delimiter=',')
	for faculty in department:
		if 'Professor' in faculty['Position'] or 'Lecturer' in faculty['Position']:
			author_name = faculty['Worker']
			author_id = querier.get_professor_db_id_by_name(author_name)
			if author_id:
				storer.store_author_and_department(author_id, department_id)

connection.commit()
connection.disconnect()