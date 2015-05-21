from SPARQLWrapper import SPARQLWrapper, JSON, XML
from lxml import etree
import rdflib
import rdfextras
import rdfextras.store.SPARQL

query1 = """
PREFIX db: <http://dbpedia.org/resource/>
PREFIX dbonto: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?who
FROM <http://dbpedia.org>
WHERE {
?who dbonto:genre db:Metal .
}
"""

query = """
SELECT distinct ?subject
FROM <http://dbpedia.org>
{
?subject rdfs:domain ?object .
<http://dbpedia.org/ontology/Band> rdfs:subClassOf ?object
OPTION (TRANSITIVE, t_distinct, t_step('step_no') as ?n, t_min
(0) ).
}"""

def get_country_description():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(XML)

    sparql.setQuery(query)  # the previous query as a literal string
    #print type(sparql.query().convert())
    return sparql.query().convert()

##f = open("output.xml", "w")
##try:
##    f.write(get_country_description().toprettyxml(indent="  "))
##finally:
##    f.close()

##xml_str = get_country_description()
##print type(xml_str)
##root = etree.fromstring(xml_str)
##print etree.tostring(root, pretty_print=True)
##

# SPARQL endpoint setup
endpoint = "http://dbpedia.org/sparql"
store = rdfextras.store.SPARQL.SPARQLStore(endpoint)
graph = rdflib.Graph(store)
# Namespaces to clear up definitions
DBONTO = rdflib.Namespace("http://dbpedia.org/ontology/")
DB = rdflib.Namespace("http://dbpedia.org/resource/")
# Query
for label in graph.predicates(DBONTO.genre, DB.music):
    print label
