import pymysql
import pymysql.cursors

class DBConnection:
	def __init__(self):
		print('dbconnection created')

	#connects to the db and returns a cursor object
	def connect(self):
		# Open database connection ip, username, password, database name
		self.connection = pymysql.connect("localhost","admin","admin","webofsciencescraper" )

		# prepare a cursor object using cursor() method
		self.cursor = self.connection.cursor()
		return self.cursor

	def disconnect(self):
		self.cursor.close()
		self.connection.close()

	def commit(self):
		self.connection.commit()