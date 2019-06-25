import pymysql
import dbconnection

connection = dbconnection.DBConnection()
cursor = connection.connect()

# Prepare SQL query to INSERT a record into the database.
# Make sure you call cursor.execute(sql) to run the script
authors_table_sql = """CREATE TABLE AUTHORS (
	AUTHOR_ID INT NOT NULL AUTO_INCREMENT,
	FIRST_NAME  VARCHAR(50) NOT NULL,
	LAST_NAME  VARCHAR(50) NOT NULL,
	AFFILIATION VARCHAR(100),  
	CITEDBY INT,
	CITEDBY5Y INT,
	EMAIL VARCHAR(100),
	HINDEX INT,
	HINDEX5Y INT,
	I10INDEX INT,
	I10INDEX5Y INT,
	GOOGLE_ID VARCHAR(20) UNIQUE,
	URL_PICTURE VARCHAR(500),
	PRIMARY KEY (AUTHOR_ID) )"""

publications_table_sql = """CREATE TABLE PUBLICATIONS (
	PUBLICATION_ID INT NOT NULL AUTO_INCREMENT,
	TITLE VARCHAR(200) NOT NULL,
	YEAR INT,
	ABSTRACT TEXT,
	AUTHOR VARCHAR(200),
	EPRINT VARCHAR(500),
	JOURNAL VARCHAR(200),
	PAGES VARCHAR(20),
	PUBLISHER VARCHAR(100),
	URL VARCHAR(500),
	VOLUME VARCHAR(10),
	ID_SCHOLARCITEDBY VARCHAR(20) UNIQUE,
	CITEDBY INT,
	ID_CITATIONS VARCHAR(30) UNIQUE,
	PRIMARY KEY (PUBLICATION_ID),
	UNIQUE KEY(TITLE, JOURNAL))
"""

authors_and_publications_table_sql = """CREATE TABLE AUTHORS_AND_PUBLICATIONS (
	AUTHOR_ID INT NOT NULL,
	PUBLICATION_ID INT NOT NULL,
	PRIMARY KEY (AUTHOR_ID, PUBLICATION_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY (PUBLICATION_ID)
	REFERENCES PUBLICATIONS(PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)
""" 

cites_per_year_table_sql = """CREATE TABLE CITES_PER_YEAR (
	YEAR INT NOT NULL,
	AUTHOR_ID INT NOT NULL,
	CITATIONS INT NOT NULL,
	PRIMARY KEY (YEAR, AUTHOR_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)
"""

cursor.execute(authors_table_sql)
cursor.execute(publications_table_sql)
cursor.execute(authors_and_publications_table_sql)
cursor.execute(cites_per_year_table_sql)
# disconnect from server
connection.disconnect()