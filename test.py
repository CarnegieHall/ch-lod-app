from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://rdf.s4.ontotext.com/4038405949/carnegiehall_db/repositories/ch-lod")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT *
    WHERE { ?s ?p ?o }
    LIMIT 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result)