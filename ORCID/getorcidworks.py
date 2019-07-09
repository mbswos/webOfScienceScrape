import requests
import ast
import json
import pprint

def getorcidinfo(orcid):
	pp = pprint.PrettyPrinter(indent=4)

	base_url = 'https://pub.orcid.org/v3.0/'

	headers={
		'Accept':'application/json'
	}

	get_url = base_url + orcid + '/works'

	get_data = requests.get(get_url, headers=headers)
	data_dictionary = get_data.json()
	return data_dictionary