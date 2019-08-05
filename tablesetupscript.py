import pymysql
import dbconnection

connection = dbconnection.DBConnection()
cursor = connection.connect()

# Prepare SQL query to INSERT a record into the database.
# Make sure you call cursor.execute(sql) to run the script
authors_table_sql = """CREATE TABLE AUTHORS (
	AUTHOR_ID INT NOT NULL AUTO_INCREMENT,
	FIRST_NAME  VARCHAR(50) NOT NULL,
	MIDDLE_NAME  VARCHAR(50),
	LAST_NAME  VARCHAR(50) NOT NULL,
	TITLE VARCHAR(50),	
	SUFFIX VARCHAR(50),
	NICKNAME VARCHAR(50),
	PRIMARY KEY (AUTHOR_ID),
	UNIQUE KEY(FIRST_NAME, LAST_NAME))"""

departments_table_sql = """CREATE TABLE DEPARTMENTS (
	DEPARTMENT_ID INT NOT NULL AUTO_INCREMENT,
	DEPARTMENT_NAME  VARCHAR(126) NOT NULL,
	PRIMARY KEY (DEPARTMENT_ID))"""

authors_and_departments_table_sql = """CREATE TABLE AUTHORS_AND_DEPARTMENTS (
	AUTHOR_ID INT NOT NULL,
	DEPARTMENT_ID INT NOT NULL,
	PRIMARY KEY (AUTHOR_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY (DEPARTMENT_ID)
	REFERENCES DEPARTMENTS(DEPARTMENT_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

authors_orcid_table_sql = """CREATE TABLE AUTHOR_ORCIDS (
	AUTHOR_ID INT NOT NULL,
	ORCID VARCHAR(20),
	ORCID_INFO_DUMP MEDIUMTEXT,
	PRIMARY KEY (ORCID),
	UNIQUE KEY(AUTHOR_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

authors_html_cvs_table_sql = """CREATE TABLE AUTHOR_HTML_CVS (
	HTML_CV_ID INT NOT NULL AUTO_INCREMENT,
	AUTHOR_ID INT NOT NULL,
	HTML_CV_TEXT MEDIUMTEXT,
	PRIMARY KEY (HTML_CV_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

other_authors_table_sql = """CREATE TABLE OTHER_AUTHORS (
	OTHER_AUTHOR_ID INT NOT NULL AUTO_INCREMENT,
	PUBLICATION_ID INT NOT NULL,
	FIRST_NAME  VARCHAR(50) NOT NULL,
	MIDDLE_NAME  VARCHAR(50),
	LAST_NAME  VARCHAR(50) NOT NULL,
	TITLE VARCHAR(50),	
	SUFFIX VARCHAR(50),
	NICKNAME VARCHAR(50),
	AFFILIATION VARCHAR(100),
	PRIMARY KEY (OTHER_AUTHOR_ID),
	FOREIGN KEY (PUBLICATION_ID)
	REFERENCES PUBLICATIONS(PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	UNIQUE KEY(FIRST_NAME, LAST_NAME, PUBLICATION_ID))"""

publications_table_sql = """CREATE TABLE PUBLICATIONS (
	PUBLICATION_ID INT NOT NULL AUTO_INCREMENT,
	TITLE VARCHAR(200) NOT NULL,
	JOURNAL VARCHAR(200),
	YEAR INT,
	VOLUME VARCHAR(10),
	PRIMARY KEY (PUBLICATION_ID),
	UNIQUE KEY(TITLE, JOURNAL, YEAR))"""

journals_table_sql = """CREATE TABLE JOURNALS (
	JOURNAL_ID INT NOT NULL AUTO_INCREMENT,
	JOURNAL_NAME VARCHAR(200) NOT NULL,
	PRIMARY KEY (JOURNAL_ID),
	UNIQUE KEY(JOURNAL_NAME))"""

# Not yet implemented might not need to be implemented
publications_validated_by_cv_table_sql = """CREATE TABLE PUBLICATIONS_VALIDATED_BY_CV (
	PUBLICATION_ID INT NOT NULL,
	PRIMARY KEY (PUBLICATION_ID),
	FOREIGN KEY (PUBLICATION_ID)
	REFERENCES PUBLICATIONS(PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)""" 

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
	ON UPDATE CASCADE)""" 

google_scholar_author_info_table_sql = """CREATE TABLE GOOGLE_SCHOLAR_AUTHOR_INFO (
	AUTHOR_ID INT NOT NULL,
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
	PRIMARY KEY (AUTHOR_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

google_scholar_cites_per_year_table_sql = """CREATE TABLE GOOGLE_SCHOLAR_CITES_PER_YEAR (
	YEAR INT NOT NULL,
	AUTHOR_ID INT NOT NULL,
	CITATIONS INT NOT NULL,
	PRIMARY KEY (YEAR, AUTHOR_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

google_scholar_publication_info_table_sql = """CREATE TABLE GOOGLE_SCHOLAR_PUBLICATION_INFO (
	PUBLICATION_ID INT NOT NULL,
	ABSTRACT TEXT,
	EPRINT VARCHAR(2047),
	PAGES VARCHAR(50),
	PUBLISHER VARCHAR(100),
	URL VARCHAR(2047),
	ID_SCHOLARCITEDBY VARCHAR(20),
	CITEDBY INT,
	ID_CITATIONS VARCHAR(30),
	PRIMARY KEY (PUBLICATION_ID),
	FOREIGN KEY (PUBLICATION_ID)
	REFERENCES PUBLICATIONS(PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

google_scholar_raw_publication_info_table_sql = """CREATE TABLE GOOGLE_SCHOLAR_RAW_PUBLICATION_INFO (
	RAW_GOOGLE_SCHOLAR_ID INT NOT NULL AUTO_INCREMENT,
	AUTHOR_ID INT NOT NULL,
	INFO_RAW TEXT,
	PRIMARY KEY (RAW_GOOGLE_SCHOLAR_ID),
	FOREIGN KEY (AUTHOR_ID)
	REFERENCES AUTHORS(AUTHOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

google_scholar_raws_and_publications_table_sql = """CREATE TABLE GOOGLE_SCHOLAR_RAWS_AND_PUBLICATIONS (
	RAW_GOOGLE_SCHOLAR_ID INT NOT NULL,
	PUBLICATION_ID INT NOT NULL,
	PRIMARY KEY (RAW_GOOGLE_SCHOLAR_ID),
	FOREIGN KEY GOOGLE_SCHOLAR_RAW_PUBLICATION_INFO(RAW_GOOGLE_SCHOLAR_ID)
	REFERENCES GOOGLE_SCHOLAR_RAW_PUBLICATION_INFO(RAW_GOOGLE_SCHOLAR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY (PUBLICATION_ID)
	REFERENCES PUBLICATIONS(PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

utdallas_publications_table_sql = """CREATE TABLE UTDALLAS_PUBLICATIONS (
	PUBLICATION_ID INT NOT NULL,
	PRIMARY KEY (PUBLICATION_ID),
	FOREIGN KEY (PUBLICATION_ID)
	REFERENCES PUBLICATIONS(PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)""" 

utdallas_journals_table_sql = """CREATE TABLE UTDALLAS_JOURNALS (
	JOURNAL_ID INT NOT NULL,
	DATA_COLLECTION_START_YEAR INT,
	JOURNAL_URL VARCHAR(2047),
	PRIMARY KEY (JOURNAL_ID),
	FOREIGN KEY (JOURNAL_ID)
	REFERENCES JOURNALS(JOURNAL_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

financial_times_top_50_journals_table_sql = """CREATE TABLE FINANCIAL_TIMES_TOP_50_JOURNALS (
	JOURNAL_ID INT NOT NULL,
	JOURNAL_RANK INT,
	PRIMARY KEY (JOURNAL_ID),
	FOREIGN KEY (JOURNAL_ID)
	REFERENCES JOURNALS(JOURNAL_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

rate_my_professors_professors_table_sql = """CREATE TABLE RATE_MY_PROFESSORS_PROFESSORS (
	RATE_MY_PROFESSORS_PROFESSOR_ID INT NOT NULL AUTO_INCREMENT,
	TDEPT VARCHAR(50),
	TSID VARCHAR(10),
	INSTITUTION_NAME VARCHAR(50),
	TFNAME VARCHAR(50),
	TMIDDLENAME VARCHAR(50),
	TLNAME VARCHAR(50),
	TID INT,
	TNUMRATINGS INT,
	RATING_CLASS VARCHAR(10),
	CONTENTTYPE VARCHAR(10),
	CATEGORYTYPE VARCHAR(10),
	OVERALL_RATING VARCHAR(3),
	UNIQUE KEY (TID),
	PRIMARY KEY (RATE_MY_PROFESSORS_PROFESSOR_ID))"""

rate_my_professors_student_ratings_table_sql ="""CREATE TABLE RATE_MY_PROFESSORS_STUDENT_RATINGS (
	RATE_MY_PROFESSORS_STUDENT_RATING_ID INT NOT NULL AUTO_INCREMENT,
	RATE_MY_PROFESSORS_PROFESSOR_ID INT NOT NULL,
	ATTENDANCE VARCHAR(20),
	CLARITYCOLOR VARCHAR(20),
	EASYCOLOR VARCHAR(20),
	HELPCOLOR VARCHAR(20),
	HELPCOUNT INT,
	ID INT,
	NOTHELPCOUNT INT,
	ONLINECLASS VARCHAR(10),
	QUALITY VARCHAR(20),
	RCLARITY VARCHAR(20),
	RCLASS VARCHAR(20),
	RCOMMENTS VARCHAR(2047),
	RDATE VARCHAR(20),
	REASY VARCHAR(20),
	REASYSTRING VARCHAR(20),
	RERRORMSG VARCHAR(200),
	RHELPFUL VARCHAR(20),
	RINTEREST VARCHAR(20),
	ROVERALL DECIMAL(2,1),
	ROVERALLSTRING VARCHAR(3),
	RSTATUS INT,
	RTEXTBOOKUSE VARCHAR(10),
	RTIMESTAMP BIGINT,
	RWOULDTAKEAGAIN VARCHAR(10),
	SID INT,
	TAKENFORCREDIT VARCHAR(10),
	TEACHER VARCHAR(20),
	TEACHERGRADE VARCHAR(20),
	UNUSEFULGROUPING VARCHAR(10),
	USEFULGROUPING VARCHAR(10),
	PRIMARY KEY (RATE_MY_PROFESSORS_STUDENT_RATING_ID),
	UNIQUE KEY (ID),
	FOREIGN KEY (RATE_MY_PROFESSORS_PROFESSOR_ID)
	REFERENCES RATE_MY_PROFESSORS_PROFESSORS(RATE_MY_PROFESSORS_PROFESSOR_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

rate_my_professors_student_rating_tags_table_sql = """CREATE TABLE RATE_MY_PROFESSORS_STUDENT_RATING_TAGS (
	RATE_MY_PROFESSORS_TEACHER_RATING_TAG_ID INT NOT NULL AUTO_INCREMENT,
	RATE_MY_PROFESSORS_STUDENT_RATING_ID INT NOT NULL,
	TAG VARCHAR(50),
	PRIMARY KEY (RATE_MY_PROFESSORS_TEACHER_RATING_TAG_ID),
	UNIQUE KEY (RATE_MY_PROFESSORS_STUDENT_RATING_ID, TAG),
	FOREIGN KEY (RATE_MY_PROFESSORS_STUDENT_RATING_ID)
	REFERENCES RATE_MY_PROFESSORS_STUDENT_RATINGS(RATE_MY_PROFESSORS_STUDENT_RATING_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

web_of_science_raw_publications_table_sql = """CREATE TABLE WEB_OF_SCIENCE_RAW_PUBLICATIONS (
	WOS_RAW_PUBLICATION_ID INT NOT NULL AUTO_INCREMENT,
	WOS_ACCESSION_NUMBER VARCHAR(20) NOT NULL,
	TITLE VARCHAR(500) NOT NULL,
	PAGES VARCHAR(20),
	JOURNAL VARCHAR(200) NOT NULL,
	ISSUE VARCHAR(10),
	YEAR INT,
	VOLUME VARCHAR(10),
	PRIMARY KEY (WOS_RAW_PUBLICATION_ID),
	UNIQUE KEY(TITLE, JOURNAL, YEAR))"""

web_of_science_raw_authors_table_sql = """CREATE TABLE WEB_OF_SCIENCE_RAW_AUTHORS(
	WOS_RAW_PUBLICATION_ID INT NOT NULL,
	FULL_AUTHOR_NAME VARCHAR(200) NOT NULL,
	PRIMARY KEY (WOS_RAW_PUBLICATION_ID, FULL_AUTHOR_NAME),
	FOREIGN KEY (WOS_RAW_PUBLICATION_ID)
	REFERENCES WEB_OF_SCIENCE_RAW_PUBLICATIONS(WOS_RAW_PUBLICATION_ID)
	ON DELETE CASCADE
	ON UPDATE CASCADE)"""

# Order is important
cursor.execute(authors_table_sql)
cursor.execute(publications_table_sql)
cursor.execute(departments_table_sql)
cursor.execute(journals_table_sql)
cursor.execute(other_authors_table_sql)
cursor.execute(authors_orcid_table_sql)
cursor.execute(authors_html_cvs_table_sql)
cursor.execute(authors_and_publications_table_sql)
cursor.execute(authors_and_departments_table_sql)
cursor.execute(google_scholar_author_info_table_sql)
cursor.execute(google_scholar_cites_per_year_table_sql)
cursor.execute(google_scholar_publication_info_table_sql)
cursor.execute(google_scholar_raw_publication_info_table_sql)
cursor.execute(google_scholar_raws_and_publications_table_sql)
cursor.execute(utdallas_publications_table_sql)
cursor.execute(utdallas_journals_table_sql)
cursor.execute(financial_times_top_50_journals_table_sql)
cursor.execute(rate_my_professors_professors_table_sql)
cursor.execute(rate_my_professors_student_ratings_table_sql)
cursor.execute(rate_my_professors_student_rating_tags_table_sql)

# save and disconnect from server
connection.commit()
connection.disconnect()