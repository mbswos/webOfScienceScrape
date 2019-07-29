import requests
from xml.etree import ElementTree
from nameparser import HumanName

raw = requests.get('https://www.bus.miami.edu/_cms-includes/pagination-people.json')
data_dict = raw.json()
professors = data_dict['items']
print(len(professors))
links_to_dep = {
		'accounting':'Accounting',
		'business-law':'Business Law',
		'business-technology':'Business Technology',
		'economics':'Economics',
		'finance':'Finance',
		'health-sector':'Health Sector Management and Policy',
		'management':'Management',
		'management-science':'Management Science',
		'marketing':'Marketing'
	}

web_lnames = []
for prof in professors:
	taxonomy = prof['taxonomy']
	if 'departments' in taxonomy:
		deps = taxonomy['departments']
		dep = deps[0]
	else:
		link = prof['link']
		dep_link = link.split('/')[3]
		dep = links_to_dep[dep_link]
	raw_name = prof['sortname']
	name = HumanName(raw_name)

	if '-' in name.last:
		last_name = name.last.split('-')[0].lower()
	elif ' ' in name.last:
		last_name = name.last.split(' ')[0].lower()
	else:
		last_name = name.last.lower()
	web_lnames.append(last_name)

prof_names = open('Professors.txt','r')
file_lnames = []
file_duplicates = []
for prof_name in prof_names:
	test = prof_name.strip()[1:len(prof_name)-2]
	name = HumanName(test)		

	if '-' in name.last:
		last_name = name.last.split('-')[0].lower()
	elif ' ' in name.last:
		last_name = name.last.split(' ')[0].lower()
	else:
		last_name = name.last.lower()
	if last_name in file_lnames:
		file_duplicates.append(last_name)
	file_lnames.append(last_name)

matches = []
non_matches_file = []
non_matches_web = []
for web_lname in web_lnames:
	for file_lname in file_lnames:
		if file_lname == web_lname:
			matches.append(web_lname)
			break;

for web_lname in web_lnames:
	if web_lname not in matches:
		non_matches_web.append(web_lname)

for file_lname in file_lnames:
	if file_lname not in matches:
		non_matches_file.append(file_lname)

print(matches)
print(len(matches))
print(len(web_lnames))
print(len(file_lnames))

print(non_matches_web)
print(len(non_matches_web))

print(non_matches_file)
print(len(non_matches_file))

print(file_duplicates)

r = requests.get('https://people.miami.edu/collections/acad-bus/bus-master-collections/bus-master.xml')
faculty_and_staff_xml = ElementTree.fromstring(r.content)
faculty_count = 0
for child in faculty_and_staff_xml:
	if child.tag == 'people-profile':
		employee_tag = child.find('employee-type')
		print(employee_tag.text.lower())
		if 'faculty' in employee_tag.text.lower():
			faculty_count += 1

print(faculty_count)
