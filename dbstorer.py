import pymysql
import pymysql.cursors
import dbconnection
import traceback
import codecs
import re
from nameparser import HumanName

file = codecs.open('UnstoredEntries.txt', 'w+', 'utf-8')

class DBStorer:
	def __init__(self):
		self.dbconnection = dbconnection.DBConnection()
		print('dbstorer created')

	# Save function - has to be executed to actually save what was "stored"
	def commit(self):
		self.dbconnection.commit()

	def connect(self):
		self.cursor = self.dbconnection.connect()

	def disconnect(self):
		self.dbconnection.disconnect()

	def store_prof_google_scholar(self, professor):
		name = HumanName(professor.name)
		columns = {}
		
		columns['affiliation'] = professor.affiliation
		columns['citedby'] = professor.citedby
		columns['citedby5y'] = professor.citedby5y
		columns['email'] = professor.email
		columns['hindex'] = professor.hindex
		columns['hindex5y'] = professor.hindex5y
		columns['i10index'] = professor.i10index
		columns['i10index5y'] = professor.i10index5y
		columns['google_id'] = professor.id
		columns['url_picture'] = professor.url_picture

		professor_db_id = self.store_author(name)
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

	def store_publication_google_scholar(self, publication, professor_id):
		author_id = professor_id
		columns = {}
		title = publication.bib['title'] if 'title' in publication.bib else ''
		year = publication.bib['year'] if 'year' in publication.bib else 0
		journal = publication.bib['journal'] if 'journal' in publication.bib else ''
		volume = publication.bib['volume'] if 'volume' in publication.bib else ''
		
		columns['abstract'] = str(publication.bib['abstract']) if 'abstract' in publication.bib else ''
		columns['eprint'] = publication.bib['eprint'] if 'eprint' in publication.bib else ''
		columns['pages'] = publication.bib['pages'] if 'pages' in publication.bib else ''
		columns['publisher'] = publication.bib['publisher'] if 'publisher' in publication.bib else ''
		columns['url'] = publication.bib['url'] if 'url' in publication.bib else ''
		columns['id_scholarcitedby'] = publication.id_scholarcitedby if hasattr(publication, 'id_scholarcitedby') else ''
		columns['citedby'] = publication.citedby if hasattr(publication, 'citedby') else 0
		columns['id_citations'] = publication.id_citations if hasattr(publication, 'id_citations') else ''

		publication_db_id = self.store_publication('PUBLICATIONS', journal, title, year, volume)

		if 'author' in publication.bib:
			other_authors = publication.bib['author'].split(' and ')
			for oa in other_authors:
				name = HumanName(oa)
				self.store_other_author(name, publication_db_id)			

		self.store_author_and_publication(author_id, publication_db_id)
		google_publication_db_id = self.__store_into_db('GOOGLE_SCHOLAR_PUBLICATION_INFO', columns)
		return publication_db_id, google_publication_db_id

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

	def store_publication(self, journal, title, year, volume):
		columns = {}
		columns['journal'] = journal
		columns['title'] = title
		columns['year'] = year
		columns['volume'] = volume
		publication_db_id = self.__store_into_db('PUBLICATIONS', columns)
		return publication_db_id

	def store_utdallas_publication(self, publication_db_id):
		columns = {}
		columns['publication_id'] = publication_db_id

		self.__store_into_db('UTDALLAS_PUBLICATIONS', columns)

	# The dictionary needs to be in the format {column_name : value} to insert the value properly into the db
	# Returns the db_id of what was last inserted
	# Stores a dictionary of columns and values into a table (stores entry)
	def __store_into_db(self, table_name, dictionary):
		if not re.match('^[a-z,A-Z,_]+$', table_name) is None:
			sql_insert = """INSERT INTO """ + table_name
			sql_values = """ VALUES """
			sql_names = """("""
			sql_params = """("""

			values_list = []
			values = []
			for key, value in dictionary.items():
				if not re.match('^[a-z,A-Z,_]+$', key) is None:
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
					print('Duplicate entry')
				else:
					file.write(table_name + ': ' + str(dictionary) + '\n')
					traceback.print_exc()
		else:
			print('Table name is wrong: ' + table_name)

	# This gets the professor db id by Google ID
	def get_professor_db_id(self, professor_id):
		# Read the professor's id
		sql = "SELECT `AUTHOR_ID` FROM `AUTHORS` WHERE `GOOGLE_ID`=%s"
		try:
			self.cursor.execute(sql, (professor_id))
			professor_db_id = self.cursor.fetchone()
			return professor_db_id[0]
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	def get_professor_db_id_by_name(self, professor_name):
		name = HumanName(professor.name)
		sql = """SELECT `AUTHOR_ID` FROM `AUTHORS` 
				 WHERE `FIRST_NAME`=%s AND `LAST_NAME`=%s"""
		try:
			self.cursor.execute(sql, (name.first, name.last))
			publication_db_id = self.cursor.fetchone()
			return publication_db_id[0]
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	# This gets the publication db id by the article's title, journal, and year
	def get_publication_db_id(self, publication_title, publication_journal, publication_year):
		# Read the publication's id
		sql = """SELECT `PUBLICATION_ID` FROM `PUBLICATIONS` 
				 WHERE `TITLE`=%s AND `JOURNAL`=%s AND `YEAR`=%s"""
		try:
			self.cursor.execute(sql, (publication_title, publication_journal, publication_year))
			publication_db_id = self.cursor.fetchone()
			return publication_db_id[0]
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	def update_other_author_db_id_by_name(self, professor_name, publication_db_id, affiliation):
		name = HumanName(professor.name)
		sql = """UPDATE `OTHER_AUTHORS` SET `AFFILIATION`=%s
				 WHERE `FIRST_NAME`=%s AND `LAST_NAME`=%s"""
		try:
			self.cursor.execute(sql, (affiliation, name.first, name.last))
			publication_db_id = self.cursor.fetchall()
			return publication_db_id
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))