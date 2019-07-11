import pymysql
import pymysql.cursors
import dbstorer
import dbquerier

class DBConnection:
	def __init__(self):
		self.storer = dbstorer.DBStorer(self)
		self.querier = dbquerier.DBQuerier(self)
		self.connect()
		print('dbconnection created')

	#connects to the db and returns a cursor object
	def connect(self):
		# Open database connection ip, username, password, database name
		self.connection = pymysql.connect("localhost","admin","admin","webofsciencescraper" )

		# prepare a cursor object using cursor() method
		self.cursor = self.connection.cursor()
		self.storer.cursor = self.cursor
		self.querier.cursor = self.cursor
		return self.cursor

	def disconnect(self):
		self.cursor.close()
		self.connection.close()

	# Save function - has to be executed to actually save what was "stored"
	def commit(self):
		self.connection.commit()

	def getdbstorer(self):
		return self.storer