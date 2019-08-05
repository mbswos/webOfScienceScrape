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
	counter = 0
	for faculty in department:
		if 'Professor' in faculty['Position'] or 'Lecturer' in faculty['Position']:
			author_name = HumanName(faculty['Worker'])
			author_id = storer.store_author(author_name)
			storer.store_author_and_department(author_id, department_id)
	print(counter)
	total+=counter
print(total)

connection.commit()
connection.disconnect()