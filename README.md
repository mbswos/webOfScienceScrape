README

Requirements:
	Python Libraries
	- Python 3 installed
	- python3 is a PATH system variable
	- pip install beautifulsoup4
	- pip install func-timeout
	- pip install nameparser
	- pip install PyMySQL
	- pip install requests
	- pip install scholarly

	Node.js
	- npm install mysql
	- npm install fs
	- npm install exceljs
	- npm install path

	Other Applications
	- Tableau Desktop 2019.2 or newer

	Database Requirements
	- MySQL Server 8.0.0 or newer

Setup:
	MySQL
	- Create a webofsciencescraper schema
	- Set the proper user credentials in the dbconnection.py file

	Python
	- Click the run.bat and link to the database
	- Or open command prompt and open the directory webOfScienceScrape and run the setup.py file.

Visualizing Data:
	- Open Professor Overview.twb with Tableau
	- Run the web server 

Folders in webOfScienceScrape:
	CurriculumVitae 
		- Contains department folders holding pdf cvs of professors and a folder that holds all those cvs in html form
	Diagrams
		- Contains diagrams that may be useful to understanding the layout of the project.
	Documentation
		- Contains documentation on folders within the WebOfScience Scrape
	ExportServer
		- Responsible for the website created to reveal the information
	FinancialTimesTop50Journals (FTT50)
		- Contains the code for storing the FTT50 Journals. 
	GoogleScholar
		- Contains the code for storing Google Scholar data.
	MiamiBusinessSchool
		- Contains code that tries to grab information available to the Miami Business School. Most python files may not be useful.
	ORCID
		- Contains the code that stores ORCID information from a csv Steve has gathered on the Miami Business School Professors.
	RateMyProfessorsScrape
		- Contains the code for storing data from RateMyProfessors.
	Scopus
		- Contains the coding attempt by Marco for querying Scopus. There needs to be major work done to create storing procedures and the like.
	SQL
		- Contains SQL scripts that may or may not be useful for querying the database. Mostly can be ignored.
	Tableau
		- Contains the Tableau workbook files for displaying data. The Tableau extension is YearRangeSelect folder found under Tableau/extensions-api-master/Samples
	UTDallas
		- Contains the code for querying and storing data from UTDallas.
	WebOfScience
		- Contains the code for querying and storing data from WebOfScienceLite.

Files in webOfScienceScrape:
	authorinitialization.py (deletable)
		- takes a text file and stores the authors. This py file is either phased out or in the process of being phased out. We are trying to move to automatic professor information from Workday. Refer to facultyandstaffinfointodb.py for what we are moving to. 
	checkgooglewithhtml.py
		- Looks throught CurriculumVitae/HTMLPages and goes through all the professor html pages which have been reformatted to go first-middle-last-cv.html where first and last are not required. The html pages were converted from the pdfs that are in the other folders in the CurriculumVitae folder.
	dbconnection.py
		- Hosts the DBConnection class, which connects to the mysql database and creates both a storer and querier object. It is responsible for connecting and disconnecting to the database and providing DBStorer and DBQuerier objects.
	dbquerier.py
		- Hosts the DBQuerier class, which requires a DBConnection object (already connected to the database).
		- Every method is a SELECT statement in sql executed against the database. Returns what the method name says.
	dbstorer.py
		- Hosts the DBStorer class, which requires a DBConnection object (already connected to the database). 
		- The store methods (methods that start with "store") are responsible for creating a columns dictionary with the key as the name of the column in the table you're storing into and with the value as what needs to be stored in the column. Other logic is then added and then the __store_into_db procedure is called with the first parameter as the table name, and then columns as the column names and data. It is optional to return the db_id of whatever table you have stored the information in.
			- Columns - {key (column name): value (column value)}
			- Store Algorithm
				- Setup columns object
				- Store into database
				- Get and return database id (optional)
		- __store_into_db(self, table_name, dictionary) inserts data into the database given a dictionary. It does not return errors for duplicates. If necessary, either copy most of the method or modify the return sql slightly so that it "ON DUPLICATE" updates. Currently configured to do nothing if SQL determines there is a duplicate. The best option will be to create a DBUpdate class. This method will skip inserting row entries if there is a SQL bug so it means the program will continue to run if there is an error.
			- table_name - needs to be the table name
			- dictionary - usually a columns dictionary (explained above)
			- has a try and except handler so skipped entries will be stored in the UnstoredEntries.txt file.
		- update function (should not be in this class, but there's only one function so this is technical debt for later)
	ProfessorListDump.txt
		- This file contains RateMyProfessor data on all UM professors. (It's file storage and can be deleted as it was done in July)
	ProfessorScoreOverview.hyper
		- This is a Tableau extract file that can be ignored.
	README.md
		- The README is self explanatory
	run.bat
		- Runs the setup program on a Windows machine.
	setup.py
		- This builds and populates the tables and should run all the scripts. To create an update script, just remove the import tablesetupscript and modify the __store_into_db method in the DBStorer class in the dbstorer.py file so that the __store_into_db method updates the row upon insertion.
	storecvs.py
		- Stores the raw text of html cvs into the database.
	tablesetupscript.py
		- Contains the SQL to setup all the tables and will setup all the tables in the database.
	UnstoredEntries.txt
		- Contains the latest unstored entries in string format from when a DBStorer object was created.