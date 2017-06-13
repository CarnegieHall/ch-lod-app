from rdflib import Namespace, URIRef, Graph, Literal


g = Graph()



g.add( (URIRef('http://data.carnegiehall.org/names/43009'), URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type') , URIRef('http://xmlns.com/foaf/0.1/Person')) )
g.add( (URIRef('http://data.carnegiehall.org/names/43009'), URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type') , Literal('01', datatype=URIRef('http://xmlns.com/foaf/0.1/Person'))) )


print(g.serialize(format='nt'))