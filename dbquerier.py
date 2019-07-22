import pymysql
import pymysql.cursors
import dbconnection
import traceback
import codecs
import re
from nameparser import HumanName

file = codecs.open('UnstoredEntries.txt', 'w+', 'utf-8')

class DBQuerier:
	def __init__(self, dbconnection):
		self.dbconnection = dbconnection
		print('dbstorer created')

	# This gets the professor db id by Google ID
	def get_professor_db_id(self, professor_id):
		# Read the professor's id
		sql = "SELECT `AUTHOR_ID` FROM `AUTHORS` WHERE `GOOGLE_ID`=%s"
		self.cursor.execute(sql, (professor_id))
		professor_db_id = self.cursor.fetchone()
		if professor_db_id == None:
			return professor_db_id
		return professor_db_id[0]

	def get_professor_db_id_by_name(self, professor_name):
		name = HumanName(professor_name)
		sql = """SELECT `AUTHOR_ID` FROM `AUTHORS` 
				 WHERE `FIRST_NAME`=%s AND `LAST_NAME`=%s"""
		self.cursor.execute(sql, (name.first, name.last))
		professor_db_id = self.cursor.fetchone()
		if professor_db_id == None:
			return professor_db_id
		return professor_db_id[0]

	# This gets the publication db id by the article's title, journal, and year
	def get_publication_db_id(self, publication_title, publication_journal, publication_year):
		# Read the publication's id
		sql = """SELECT `PUBLICATION_ID` FROM `PUBLICATIONS` 
				 WHERE `TITLE`=%s AND `JOURNAL`=%s AND `YEAR`=%s"""
		self.cursor.execute(sql, (publication_title, publication_journal, publication_year))
		publication_db_id = self.cursor.fetchone()
		if publication_db_id == None:
			return publication_db_id
		return publication_db_id[0]

	# Gets a list of publications that are in cvs (so far just id and title)
	def get_publications_in_cvs(self):
		sql = """SELECT p.PUBLICATION_ID, p.TITLE, p.JOURNAL, p.YEAR, p.VOLUME FROM authors as a
				 JOIN author_html_cvs as ahc on a.AUTHOR_ID = ahc.AUTHOR_ID
				 JOIN authors_and_publications as ap on a.AUTHOR_ID = ap.AUTHOR_ID
				 JOIN publications as p on ap.PUBLICATION_ID = p.PUBLICATION_ID
				 WHERE ahc.HTML_CV_TEXT LIKE CONCAT(\"%\", p.TITLE, \"%\")"""
		self.cursor.execute(sql,())
		publications = self.cursor.fetchall()
		return publications

	def get_journal_db_id_by_name(self, journal_name):
		sql = """SELECT `JOURNAL_ID` FROM `JOURNALS` 
				 WHERE `JOURNAL_NAME`=%s"""
		self.cursor.execute(sql, (journal_name))
		journal_db_id = self.cursor.fetchone()
		if journal_db_id == None:
			return journal_db_id
		return journal_db_id[0]

	def get_professor_list(self):
		sql = """SELECT * FROM `AUTHORS`"""
		self.cursor.execute(sql,())
		professors = self.cursor.fetchall()
		return professors