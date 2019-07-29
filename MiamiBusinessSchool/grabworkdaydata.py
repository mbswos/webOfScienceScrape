import requests
from xml.etree import ElementTree
from xml.dom import minidom
import codecs

data_list = [
	'https://people.miami.edu/collections/acad-arc/arc-master-collections/arc-master.xml',
	'https://people.miami.edu/collections/acad-as/as-master-collections/as-master.xml',
	'https://people.miami.edu/collections/acad-bus/bus-master-collections/bus-master.xml',
	'https://people.miami.edu/collections/acad-scom/scom-master-collections/com-master.xml',
	'https://people.miami.edu/collections/acad-dcie/dcie-master-collections/dcie-master.xml',
	'https://people.miami.edu/collections/acad-educ/educ-master-collections/education-master.xml',
	'https://people.miami.edu/collections/acad-eng/eng-master-collections/coe-master.xml',
	'https://people.miami.edu/collections/acad-grad/grad-master-collections/gs-master.xml',
	'https://people.miami.edu/collections/acad-law/law-master-collections/law-master.xml',
	'https://people.miami.edu/collections/acad-rsms/rsmas-master-collections/rsmas-master.xml',
	'https://people.miami.edu/collections/acad-med/med-master-collections/leadership/leadership.xml',
	'https://people.miami.edu/collections/acad-mus/mus-master-collections/music-master.xml',
	'https://people.miami.edu/collections/acad-sonhs/sonhs-master-collections/sonhs-master.xml'
]

file = codecs.open('ForSteveBetter.xml', 'w+', 'utf-8')

for url in data_list:
	r = requests.get(url)
	testtree = ElementTree.fromstring(r.content)
	treestring = str(ElementTree.tostring(testtree))

file.close()