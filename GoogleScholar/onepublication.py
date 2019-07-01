import scholarly
import codecs
import dbstorer

search_string = 'DAvinCi: A Cloud Computing Framework for Service Robots'
search_query = scholarly.search_pubs_query(search_string)
pub = next(search_query).fill()
print(pub)