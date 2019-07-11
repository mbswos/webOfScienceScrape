import csv
import ORCID.getorcidworks as gow
import dbconnection

#run from webOfScienceScrape
connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

csv_file = open('ORCID/ORCID.csv', mode='r')
csv_reader = csv.DictReader(csv_file)
count = 0
for row in csv_reader:
	if not row['ORCID'] == 'N/A':
		orcid = row['ORCID']
		professor_name = row['First Name'] + ' ' + row['Last Name']
		orcid_data = gow.getorcidinfo(orcid)
		professor_db_id = querier.get_professor_db_id_by_name(professor_name)
		
		if professor_db_id:
			print(professor_db_id)
			storer.store_author_orcid(professor_db_id, orcid, str(orcid_data))
		else:
			print(professor_name)
		count+=1

connection.commit()
connection.disconnect()
print(count)