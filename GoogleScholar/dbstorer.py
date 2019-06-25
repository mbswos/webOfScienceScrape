import pymysql
import pymysql.cursors
import dbconnection

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

	# Assumes professor's name is in the format firstname lastname
	# Technically gets both the first and middle names
	def parse_first_name(self, professor_name):
		names = professor_name.split(' ')
		first_name = ''
		for i in range(len(names)-1):
			first_name += names[i]
		return first_name

	# Assumes professor's name is in the format firstname lastname
	def parse_last_name(self, professor_name):
		names = professor_name.split(' ')
		last_name = names[len(names)-1]
		return last_name

	# Sets up the db, must call commit to actually save the data, returns id if successfully committed
	def store_prof(self, professor):
		first_name = self.parse_first_name(professor.name)
		last_name = self.parse_last_name(professor.name)
		affiliation = professor.affiliation
		citedby = professor.citedby
		citedby5y = professor.citedby5y
		email = professor.email
		hindex = professor.hindex
		hindex5y = professor.hindex5y
		i10index = professor.i10index
		i10index5y = professor.i10index5y
		google_id = professor.id
		url_picture = professor.url_picture

		try:
			# Create a new author/professor
			sql = """INSERT INTO `AUTHORS` (
				`FIRST_NAME`,
				`LAST_NAME`,
				`AFFILIATION`,
				`CITEDBY`,
				`CITEDBY5Y`,
				`EMAIL`,
				`HINDEX`,
				`HINDEX5Y`,
				`I10INDEX`,
				`I10INDEX5Y`,
				`GOOGLE_ID`,
				`URL_PICTURE`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			self.cursor.execute(sql, (
				first_name, 
				last_name, 
				affiliation, 
				citedby, 
				citedby5y, 
				email, 
				hindex, 
				hindex5y, 
				i10index, 
				i10index5y, 
				google_id, 
				url_picture))
			professor_db_id = self.cursor.lastrowid
			self.store_cites_per_year(professor.cites_per_year, professor_db_id)
			return professor_db_id
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	# Sets up the db, must call commit to actually save the data, returns id if successfully committed
	def store_publication(self, publication, professor_id):
		author_id = professor_id
		title = publication.bib['title'] if 'title' in publication.bib else ''
		year = publication.bib['year'] if 'year' in publication.bib else 0
		abstract = str(publication.bib['abstract']) if 'abstract' in publication.bib else ''
		author = publication.bib['author'] if 'author' in publication.bib else ''
		eprint = publication.bib['eprint'] if 'eprint' in publication.bib else ''
		journal = publication.bib['journal'] if 'journal' in publication.bib else ''
		pages = publication.bib['pages'] if 'pages' in publication.bib else ''
		publisher = publication.bib['publisher'] if 'publisher' in publication.bib else ''
		url = publication.bib['url'] if 'url' in publication.bib else ''
		volume = publication.bib['volume'] if 'volume' in publication.bib else ''
		id_scholarcitedby = publication.id_scholarcitedby if hasattr(publication, 'id_scholarcitedby') else ''
		citedby = publication.citedby if hasattr(publication, 'citedby') else 0
		id_citations = publication.id_citations if hasattr(publication, 'id_citations') else ''

		try:
			sql = """INSERT INTO `PUBLICATIONS` (
				`TITLE`,
				`YEAR`,
				`ABSTRACT`,
				`AUTHOR`,
				`EPRINT`,
				`JOURNAL`,
				`PAGES`,
				`PUBLISHER`,
				`URL`,
				`VOLUME`,
				`ID_SCHOLARCITEDBY`,
				`CITEDBY`,
				`ID_CITATIONS`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			self.cursor.execute(sql, (
				title,
				year,
				abstract,
				author,
				eprint,
				journal,
				pages,
				publisher,
				url,
				volume,
				id_scholarcitedby,
				citedby,
				id_citations))
			publication_db_id = self.cursor.lastrowid
			self.store_author_and_publications(author_id, publication_db_id)
			return publication_db_id
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	# Sets up the db, must call commit to actually save the data, returns id if successfully committed
	def store_cites_per_year(self, cites_per_year, professor_id):
		cites_per_year_list = cites_per_year.items()
		sql = """INSERT INTO `CITES_PER_YEAR` (`YEAR`, `AUTHOR_ID`, `CITATIONS`) VALUES (%s, %s, %s)"""
		for cite_per_year in cites_per_year_list:
			try:
				year = cite_per_year[0]
				citations = cite_per_year[1]
				self.cursor.execute(sql, (year, professor_id, citations))
				store_cites_per_year_db_id = self.cursor.lastrowid
			except Exception as e:
				print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	# Sets up the db, must call commit to actually save the data, returns id if successfully committed
	def store_author_and_publications(self, author_id, publication_id):
		sql ="""INSERT INTO `AUTHORS_AND_PUBLICATIONS` (`AUTHOR_ID`, `PUBLICATION_ID`) VALUES (%s, %s)"""
		try:
			self.cursor.execute(sql, (author_id, publication_id))
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))

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

	# This gets the publication db id, by the article's title and journal
	def get_publication_db_id(self, publication_title, publication_journal):
		# Read the publication's id
		sql = "SELECT `PUBLICATION_ID` FROM `PUBLICATIONS` WHERE `TITLE`=%s AND `JOURNAL`=%s"
		try:
			self.cursor.execute(sql, (publication_title, publication_journal))
			publication_db_id = self.cursor.fetchone()
			return publication_db_id[0]
		except Exception as e:
			print('Got error {!r}, errno is {}'.format(e, e.args[0]))
