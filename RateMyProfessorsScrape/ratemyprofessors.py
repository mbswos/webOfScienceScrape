import requests
import ast
import RateMyProfessorsScrape.RMPClass as RMPClass
import dbconnection

connection = dbconnection.DBConnection()
storer = connection.storer
UniversityOfMiami = RMPClass.RateMyProfScraper(1241)
base_url = 'https://www.ratemyprofessors.com/paginate/professors/ratings?tid='
headers = {
	'accept': 'application/json, text/javascript, */*; q=0.01',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US,en;q=0.9',
	'cookie': 'ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22ab563340-e100-4e93-899e-0989abc9cb4e%22; notice=true; _ga=GA1.2.1402873715.1561644322; __gads=ID=fcab18b757e7e364:T=1561644323:S=ALNI_Mb8uq26jEMtYFyxwzfyY03jJ5HN-A; showTeacherPopout=true; _gid=GA1.2.1008645251.1562858751; promotionIndex=0; showSchoolPopout=true; ad_blocker_overlay_2019=true; previousSchoolID=1241; _gat=1',
	'referer': 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1318252&showMyProfs=true',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
	'x-requested-with': 'XMLHttpRequest'
}

for professor in UniversityOfMiami.professorlist:
	tid = professor['tid']
	professor_name = professor['tLname'].strip() + '_' + professor['tFname'].strip().replace('"', '&')
	print(professor_name)
	prof_base_url = base_url + str(tid)
	first_request = requests.get(prof_base_url, headers=headers)
	raw_json = first_request.json()
	ratings = raw_json['ratings']
	if 'remaining' in raw_json:
		count = raw_json['remaining']
		page = 2
		while count > 0:
			prof_url = prof_base_url + '&page=' + str(page)
			data = requests.get(prof_url, headers=headers)
			data_list = data.json()['ratings']
			page += 1
			count -= len(data_list)
			ratings.extend(data_list)

	rate_my_prof_db_id = storer.store_rate_my_professors_professor(professor)
	for student_rating in ratings:
		if not isinstance(student_rating, str):
			storer.store_rate_my_professors_student_rating(student_rating, rate_my_prof_db_id)

connection.commit()
connection.disconnect()
