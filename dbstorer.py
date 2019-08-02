import pymysql
import pymysql.cursors
import dbconnection
import traceback
import codecs
import re
from nameparser import HumanName

file = codecs.open('UnstoredEntries.txt', 'w+', 'utf-8')

class DBStorer:
	def __init__(self, dbconnection):
		self.dbconnection = dbconnection
		print('dbstorer created')

	def store_prof_google_scholar(self, professor):
		name = HumanName(professor.name)
		columns = {}
		
		columns['affiliation'] = professor.affiliation
		columns['citedby'] = professor.citedby if hasattr(professor, 'citedby') else 0
		columns['citedby5y'] = professor.citedby5y if hasattr(professor, 'citedby5y') else 0
		columns['email'] = professor.email if hasattr(professor, 'email') else ''
		columns['hindex'] = professor.hindex if hasattr(professor, 'hindex') else 0
		columns['hindex5y'] = professor.hindex5y if hasattr(professor, 'hindex5y') else 0
		columns['i10index'] = professor.i10index if hasattr(professor, 'i10index') else 0
		columns['i10index5y'] = professor.i10index5y if hasattr(professor, 'i10index5y') else 0
		columns['google_id'] = professor.id 
		columns['url_picture'] = professor.url_picture if hasattr(professor, 'url_picture') else ''

		professor_db_id = self.dbconnection.querier.get_professor_db_id_by_name(professor.name)
		if professor_db_id == None:
			print(professor)
		columns['author_id'] = professor_db_id

		self.store_cites_per_year_google_scholar(professor.cites_per_year, professor_db_id)
		google_author_db_id = self.__store_into_db('GOOGLE_SCHOLAR_AUTHOR_INFO', columns)
		return professor_db_id, google_author_db_id

	def store_cites_per_year_google_scholar(self, cites_per_year, professor_id):
		cites_per_year_list = cites_per_year.items()
		for cite_per_year in cites_per_year_list:
			columns = {}
			columns['year'] = cite_per_year[0]
			columns['author_id'] = professor_id
			columns['citations'] = cite_per_year[1]
			store_cites_per_year_db_id = self.__store_into_db('GOOGLE_SCHOLAR_CITES_PER_YEAR', columns)

	# Should only store publications that exist in the db
	# Handles storing the author and publication link
	def store_publication_google_scholar(self, publication, professor_id):
		author_id = professor_id
		columns = {}
		title = publication['bib']['title'] if 'title' in publication['bib'] else ''
		year = publication['bib']['year'] if 'year' in publication['bib'] else 0
		journal = publication['bib']['journal'] if 'journal' in publication['bib'] else ''
		volume = publication['bib']['volume'] if 'volume' in publication['bib'] else ''
		
		columns['abstract'] = str(publication['bib']['abstract']) if 'abstract' in publication['bib'] else ''
		columns['eprint'] = publication['bib']['eprint'] if 'eprint' in publication['bib'] else ''
		columns['pages'] = publication['bib']['pages'] if 'pages' in publication['bib'] else ''
		columns['publisher'] = publication['bib']['publisher'] if 'publisher' in publication['bib'] else ''
		columns['url'] = publication['bib']['url'] if 'url' in publication['bib'] else ''
		columns['id_scholarcitedby'] = publication.id_scholarcitedby if hasattr(publication, 'id_scholarcitedby') else ''
		columns['citedby'] = publication.citedby if hasattr(publication, 'citedby') else 0
		columns['id_citations'] = publication.id_citations if hasattr(publication, 'id_citations') else ''

		publication_db_id = self.dbconnection.querier.get_publication_db_id(title, journal, year)
		if publication_db_id:
			columns['publication_id'] = publication_db_id

			if 'author' in publication['bib']:
				other_authors = publication['bib']['author'].split(' and ')
				for oa in other_authors:
					name = HumanName(oa)
					self.store_other_author(name, publication_db_id)			

			self.store_author_and_publication(author_id, publication_db_id)
			google_publication_db_id = self.__store_into_db('GOOGLE_SCHOLAR_PUBLICATION_INFO', columns)
			return publication_db_id, google_publication_db_id

	def store_raw_publication_google_scholar(self, professor_db_id, raw):
		columns = {}
		columns['author_id'] = professor_db_id
		columns['info_raw'] = raw
		raw_google_db_id = self.__store_into_db('GOOGLE_SCHOLAR_RAW_PUBLICATION_INFO', columns)
		return raw_google_db_id

	def store_raw_and_publication_google_scholar(self, publication_db_id, raw_google_db_id):
		columns = {}
		columns['publication_id'] = publication_db_id
		columns['raw_google_scholar_id'] = raw_google_db_id
		self.__store_into_db('GOOGLE_SCHOLAR_RAWS_AND_PUBLICATIONS', columns)

	def store_author_and_publication(self, author_id, publication_id):
		columns = {}
		columns['author_id'] = author_id
		columns['publication_id'] = publication_id

		author_and_publication_db_id = self.__store_into_db('AUTHORS_AND_PUBLICATIONS', columns)

	def store_author(self, professor_name_object):
		columns = {}
		columns['title'] = professor_name_object.title
		columns['first_name'] = professor_name_object.first
		columns['middle_name'] = professor_name_object.middle
		columns['last_name'] = professor_name_object.last
		columns['suffix'] = professor_name_object.suffix
		columns['nickname'] = professor_name_object.nickname
		professor_db_id = self.__store_into_db('AUTHORS', columns)
		return professor_db_id

	def store_other_author(self, professor_name_object, publication_db_id, affiliation = ''):
		columns = {}
		columns['title'] = professor_name_object.title 
		columns['first_name'] = professor_name_object.first
		columns['middle_name'] = professor_name_object.middle
		columns['last_name'] = professor_name_object.last
		columns['suffix'] = professor_name_object.suffix
		columns['nickname'] = professor_name_object.nickname
		columns['affiliation'] = affiliation
		columns['publication_id'] = publication_db_id
		other_professor_db_id = self.__store_into_db('OTHER_AUTHORS', columns)
		return other_professor_db_id

	def store_publication(self, title, journal, year, volume):
		columns = {}
		columns['title'] = title
		columns['journal'] = journal
		columns['year'] = year
		columns['volume'] = volume
		publication_db_id = self.__store_into_db('PUBLICATIONS', columns)
		return publication_db_id

	def store_utdallas_publication(self, publication_db_id):
		columns = {}
		columns['publication_id'] = publication_db_id

		self.__store_into_db('UTDALLAS_PUBLICATIONS', columns)

	def store_author_orcid(self, professor_db_id, orcid, orcid_info):
		columns = {}
		columns['author_id'] = professor_db_id
		columns['orcid'] = orcid
		columns['orcid_info_dump'] = orcid_info

		self.__store_into_db('AUTHOR_ORCIDS', columns)

	def store_author_html_cv(self, professor_db_id, html):
		columns = {}
		columns['author_id'] = professor_db_id
		columns['html_cv_text'] = html

		self.__store_into_db('AUTHOR_HTML_CVS', columns)

	def store_journal(self, journal_name):
		columns = {}
		columns['journal_name'] = journal_name
		journal_db_id = self.__store_into_db('JOURNALS', columns)
		return journal_db_id

	def store_journal_utdallas(self, journal_db_id, data_collection_start_year, journal_url):
		columns = {}
		columns['journal_id'] = journal_db_id
		columns['data_collection_start_year'] = data_collection_start_year
		columns['journal_url'] = journal_url
		self.__store_into_db('UTDALLAS_JOURNALS', columns)

	def store_journal_financial_times_top_50(self, journal_db_id, journal_rank):
		columns = {}
		columns['journal_id'] = journal_db_id
		columns['journal_rank'] = journal_rank
		self.__store_into_db('FINANCIAL_TIMES_TOP_50_JOURNALS', columns)

	def store_rate_my_professors_professor(self, professor):
		columns = professor
		rate_my_professors_professor_db_id = self.__store_into_db('RATE_MY_PROFESSORS_PROFESSORS', columns)
		return rate_my_professors_professor_db_id

	def store_rate_my_professors_student_rating(self, rating, rate_my_professors_professor_db_id):
		columns = rating
		columns['rate_my_professors_professor_id'] = rate_my_professors_professor_db_id
		teacher_rating_tags = columns.pop('teacherRatingTags', None)
		rate_my_professors_student_rating_db_id = self.__store_into_db('RATE_MY_PROFESSORS_STUDENT_RATINGS', columns)
		for tag in teacher_rating_tags:
			self.store_rate_my_professors_student_rating_tag(tag, rate_my_professors_student_rating_db_id)
		return rate_my_professors_student_rating_db_id

	def store_rate_my_professors_student_rating_tag(self, tag, student_rating_db_id):
		columns = {}
		columns['rate_my_professors_student_rating_id'] = student_rating_db_id
		columns['tag'] = tag
		self.__store_into_db('RATE_MY_PROFESSORS_STUDENT_RATING_TAGS', columns)

	def store_web_of_science_raw_publication(self, publication):
		columns = {}
		columns['wos_accession_number'] = publication['UT']
		columns['title'] = publication['Title']['Title'][0]
		columns['pages'] = publication['Source']['Pages'][0]
		columns['journal'] = publication['Source']['SourceTitle'][0]
		columns['issue'] = publication['Source']['Issue'][0] if 'Issue' in publication['Source'] else ''
		columns['volume'] = publication['Source']['Volume'][0] if 'Volume' in publication['Source'] else 0
		columns['year'] = int(publication['Source']['Published.BiblioYear'][0])
		wos_raw_pub_db_id = self.__store_into_db('WEB_OF_SCIENCE_RAW_PUBLICATIONS', columns)
		return wos_raw_pub_db_id

	def store_web_of_science_raw_author(self, raw_publication_db_id, author_name):
		columns = {}
		columns['wos_raw_publication_id'] = raw_publication_db_id
		columns['full_author_name'] = author_name
		self.__store_into_db('WEB_OF_SCIENCE_RAW_AUTHORS', columns)

	# The dictionary needs to be in the format {column_name : value} to insert the value properly into the db
	# Returns the db_id of what was last inserted
	# Stores a dictionary of columns and values into a table (stores entry)
	def __store_into_db(self, table_name, dictionary):
		if not re.match('^[a-z,A-Z,_,1-9,0]+$', table_name) is None:
			sql_insert = """INSERT INTO """ + table_name
			sql_values = """ VALUES """
			sql_names = """("""
			sql_params = """("""

			values_list = []
			values = []
			for key, value in dictionary.items():
				if not re.match('^[a-z,A-Z,_,1-9,0]+$', key) is None:
					sql_names += key + ""","""
					sql_params += """%s,"""
					values.append(value)
			sql_names = sql_names[:-1]
			sql_names += """)"""
			sql_params = sql_params[:-1]
			sql_params += """)"""

			values_list.extend(values)

			sql = sql_insert + sql_names + sql_values + sql_params

			try:
				self.cursor.execute(sql, tuple(values_list))
				db_id = self.cursor.lastrowid
				return db_id
			except Exception as e:
				if e.args[0] == 1062:
					trap = 1
					# print(e)
					# print('Duplicate entry: ' + table_name + ' - ' + str(dictionary))
				elif e.args[0] == 1406:
					print('Column too long: ' + str(e))
					print(dictionary)
				else:
					file.write(table_name + ': ' + str(dictionary) + '\n')
					traceback.print_exc()
		else:
			print('Table name is wrong: ' + table_name)

	def update_other_author_db_id_by_name(self, professor_name, publication_db_id, affiliation):
		name = HumanName(professor_name)
		sql = """UPDATE `OTHER_AUTHORS` SET `AFFILIATION`=%s
				 WHERE `FIRST_NAME`=%s AND `LAST_NAME`=%s"""
		try:
			self.cursor.execute(sql, (affiliation, name.first, name.last))
			publication_db_id = self.cursor.fetchall()
			return publication_db_id
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	def store_test(self):
		columns = {}
		columns['test_id'] = 1
		self.__store_into_db('TEST', columns)