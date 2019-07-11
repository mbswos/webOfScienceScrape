import requests
import dbconnection
from bs4 import BeautifulSoup

connection = dbconnection.DBConnection()
storer = connection.storer
querier = connection.querier

financial_top_journals_file = open('FinancialTimesTop50Journals/FinancialTimesTop50Journals.txt', 'r')
for journal in financial_top_journals_file:
	info = journal.split('.')
	rank = int(info[0].strip())
	journal_name = info[1].strip()

	journal_db_id = storer.store_journal(journal_name)
	if not journal_db_id:
		journal_db_id = querier.get_journal_db_id_by_name(journal_name)

	storer.store_journal_financial_times_top_50(journal_db_id, rank)

financial_top_journals_file.close()
connection.commit()
connection.disconnect()