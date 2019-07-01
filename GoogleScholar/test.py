import scholarly
import codecs
import csv
import dbstorer
import re

table_name ='TEST_TABLE_NAME'
dictionary = {'COLUMN_A' : 'a', 'COLUMN_B' : 'b', 'COLUMN_C' : 1}

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


print(sql)
print(tuple(values_list))