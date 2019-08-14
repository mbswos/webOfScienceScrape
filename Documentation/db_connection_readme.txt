##DB CONNECTION:
**Connection to localhost its required in order to save data on the correct server**

##Getting Started:
	The dbconnection.py file its required to connect to the database.
	the following methods reside inside this object:
	1. DBConnection  > Class where methods are stored
		- connect  > Method used for connection, it required 5 parameters: host, user, password, database and port
		- disconnect  > Method used for database disconnection, always disconnect when query have run
		- commit  > Method to use after an update or some type of modification to the database was done
		- getdbstorer  > Method to return the storer class


##Prerequisites:
	The following modules must be installed to run this file:
		- pymysql > Use for MySQL connections
		- pymysql.cursors > Use run MySQL connections
		- dbstorer > Use to call the dbstorer class / store queries
		- dbquerier > Use to call the dbquerier class / select queries

##Installing:
	- python -m pip install pymysql
		pymysql will be ready to import

##DB CONNECTION: Example:
	After importing the dbconnection file:
		1. connection = dbconnection.DBConnection()
		2. storer = connection.storer
		3. querier = connection.querier
		4. connection.commit()
		5. connection.disconnect()

