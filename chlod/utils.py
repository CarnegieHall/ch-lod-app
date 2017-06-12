from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings
import operator


def return_objects(uri):
	sparql = SPARQLWrapper(settings.SPARQL_ENDPOINT)
	sparql.setQuery("""
	    SELECT *
	    WHERE { %s ?p ?o }
	    LIMIT 9000
	""" % (uri))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	return results
	# for result in results["results"]["bindings"]:
	#     print(result)

def return_subjects(uri):
	sparql = SPARQLWrapper(settings.SPARQL_ENDPOINT)
	sparql.setQuery("""
	    SELECT *
	    WHERE { ?s ?p %s }
	    LIMIT 9000
	""" % (uri))
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	return results
	# for result in results["results"]["bindings"]:
	#     print(result)
"""
Returns the label and date of uris given good for events
"""
def return_label_date(uris):
	sparql = SPARQLWrapper(settings.SPARQL_ENDPOINT)

	query = 'PREFIX dcterms: <http://purl.org/dc/terms/>' 
	query = query + 'SELECT * WHERE{' 
	query = query + '{?uri rdfs:label ?o . ?uri ?p ?o .}' 
	query = query + 'UNION' 
	query = query + '{?uri dcterms:date ?o . ?uri ?p ?o .}' 
	query = query + 'FILTER (?uri IN ('+ ','.join(uris)  +'))' 
	query = query + '}'

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	return results


"""
Returns the names of the URIs given, either as foaf name or label depending on how they were stored
"""
def return_name(uris):
	sparql = SPARQLWrapper(settings.SPARQL_ENDPOINT)

	query = 'PREFIX foaf: <http://xmlns.com/foaf/0.1/>' 
	query = query + 'SELECT * WHERE{' 
	query = query + '{?uri rdfs:label ?o . ?uri ?p ?o .}' 
	query = query + 'UNION' 
	query = query + '{?uri foaf:name ?o . ?uri ?p ?o .}' 
	query = query + 'FILTER (?uri IN ('+ ','.join(uris)  +'))' 
	query = query + '}'

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	return results


def format_events_dict(event_uri):


	o = return_objects(event_uri)
	s = return_subjects(event_uri)

	agents = []
	dates = []
	types = []
	labels = []
	unmapped = []
	product = []
	venue = []

	for result in o["results"]["bindings"]:
		if '/names/' in result['o']['value']:
			agents.append('<'+result['o']['value']+'>')

		if result['p']['value'] == 'http://purl.org/NET/c4dm/event.owl#product':
			product.append(result['o']['value'])
		elif result['p']['value'] == 'http://purl.org/dc/terms/date':
			dates.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		elif result['p']['value'] == 'http://purl.org/NET/c4dm/event.owl#place':
			venue.append('<'+result['o']['value']+'>')


		elif result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			labels.append(result['o']['value'])
		elif '/names/' in result['o']['value']:
			pass
		else:
			unmapped.append([result['p']['value'], result['o']['value']])



	product.sort()
	people = []

	agents = return_name(agents)
	for agent in agents["results"]["bindings"]:

		#look for the triple in the main set
		for result in o["results"]["bindings"]:
			if result['o']['value'] == agent['uri']['value']:
				people.append([agent['uri']['value'], agent['o']['value'],result['p']['value'].replace('http://purl.org/ontology/mo/','mo:') ])

	venue = return_name(venue)
	venues = []
	for v in venue["results"]["bindings"]:
		venues.append([v['uri']['value'],v['o']['value']])



	event = {
		'dcterms_date' : dates,
		'rdf_type' : types,
		'rdfs_label' : labels,
		'rdfs_label_string' : (',').join(labels),
		'unmapped' : unmapped,
		'people' : people,
		'product': product,
		'venues' : venues
	}




	return event
	




def format_works_dict(work_uri):


	o = return_objects(work_uri)
	s = return_subjects(work_uri)

	#these will be all the event works, so we just want to get the parent events
	events = []
	for result in s["results"]["bindings"]:
		if 'http://data.carnegiehall.org/events/' in result['s']['value']:

			uri = result['s']['value'].split('/work_')[0]
			
			if uri not in events:
				events.append('<' + uri + '>')

	#events
	events = return_label_date(events)
	events_map = {}

	for result in events["results"]["bindings"]:
		uri = result['uri']['value']
		if uri not in events_map:
			events_map[uri] = { 'rdfs:label' : '', 'dcterms:date' : '' }

		if result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			events_map[uri]['rdfs:label'] = result['o']['value']

		if result['p']['value'] == 'http://purl.org/dc/terms/date':
			events_map[uri]['dcterms:date'] = result['o']['value']



	creators = []
	creators_map = []
	dates = []
	types = []
	labels = []
	unmapped = []
	match = []

	for result in o["results"]["bindings"]:
		if result['p']['value'] == 'http://purl.org/dc/terms/creator':
			creators.append('<' + result['o']['value'] + '>')
		elif result['p']['value'] == 'http://purl.org/dc/terms/created':
			dates.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			labels.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2004/02/skos/core#exactMatch':
			match.append(result['o']['value'])
		else:
			unmapped.append([result['p']['value'], result['o']['value']])


	creators = return_name(creators)
	for result in creators["results"]["bindings"]:
		uri = result['uri']['value']
		creators_map.append([uri,result['o']['value']])


	events = []
	for key, value in events_map.items():
		events.append([key,value['rdfs:label'],value['dcterms:date']])

	events.sort(key=lambda x: x[2], reverse=True)

	work = {
		'dcterms_creator' : creators_map,
		'dcterms_created' : dates,
		'rdf_type' : types,
		'rdfs_label' : labels,
		'rdfs_label_string' : (',').join(labels),
		'events' : events,
		'unmapped' : unmapped,
		'skos_exact_match' : match
	}

	return work

