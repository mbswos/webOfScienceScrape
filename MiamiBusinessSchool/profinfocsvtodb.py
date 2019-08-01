import csv
import dbconnection

connection = dbconnection.DBConnection()
storer = connection.storer

dept_name_to_dept = {
	'CC00007 School of Business Administration - Accounting':'Accounting',
	'CC00053 Business Law':'Business Law',
	'CC00106 Business Technology':'Business Technology',
	'CC00157 School of Business Administration - Economics':'Economics',
	'CC00193 Finance':'Finance',
	'CC00066 Center for Health Management and Policy':'Health Sector Management and Policy',
	'CC00282 Management':'Management',
	'CC00283 Management Science':'Management Science',
	'CC00292 School of Business Administration - Marketing':'Marketing',
	'CC00407 School of Business Administration - Graduate Programs':'Graduate Programs'
}

csv_file = open('MiamiBusinessSchool/WorkerInformation.csv', 'r')
csv_reader = csv.DictReader(csv_file, delimiter=',')
for row in csv_reader:
	prof_id = row['ID']
	last_name = row['Last']
	first_name = row['First']
	employee_type = row['EmployeeType']
	time_type = row['Status']
	title = row['Title']
	department = row['Department']

	print(dept_name_to_dept[department])