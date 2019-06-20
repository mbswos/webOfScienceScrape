"""
Example usage.

"""
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

import environment_variables

from wos2vivo.harvest import get_publications_for_org
from rdflib import Graph



g = Graph()

org_name = "University of Florida"
author_name = "Cronqvist Henr*"

tspan = dict(begin="2016-03-01", end="2016-03-14")

for pub in get_publications_for_org(
        org_name,
        span=tspan
    ):
    print pub.ut()
    print pub.title()
    print pub.doi()

    g += pub.to_rdf()

    print
    print '-' * 10
    print

for pub in get_publications_for_author(author_name):
    print pub.ut()
    print pub.title()
    print pub.doi()

    g += pub.to_rdf()

    print
    print '-' * 10
    print

# Serialize as RDF.
#print g.serialize(format='turtle')