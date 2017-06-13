from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import URIRef, Graph, Literal, plugin
from rdflib.serializer import Serializer
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

"""
Returns the work URIs for a work event id
"""
def return_works_from_event(uris):
	sparql = SPARQLWrapper(settings.SPARQL_ENDPOINT)

	query = 'PREFIX dcterms: <http://purl.org/dc/terms/>' 
	query = query + 'SELECT * WHERE{' 
	query = query + '?uri <http://purl.org/NET/c4dm/event.owl#product> ?o . ?uri ?p ?o .' 
	query = query + 'FILTER (?uri IN ('+ ','.join(uris)  +'))' 
	query = query + '}'

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	event_work_map = {}
	work_uris = []

	for result in results["results"]["bindings"]:
		work_uris.append('<' + result['o']['value'] + '>')
		event_work_map[result['uri']['value']] = result['o']['value']

	labels = return_label_date(work_uris)

	for label in labels["results"]["bindings"]:
		print(label)
		for key in event_work_map:
			if event_work_map[key] == label['uri']['value']:
				event_work_map[key] = label['o']['value']

	return event_work_map


"""
Returns the work URIs for a work event id
"""
def return_serialized_subjects(uri,type):
	sparql = SPARQLWrapper(settings.SPARQL_ENDPOINT)

	if uri[0] != '<':
		uri_no_bracket = uri
		uri = '<' + uri + '>'
	else:
		uri_no_bracket = uri[1:]
		uri_no_bracket = uri_no_bracket[:-1]


	query = 'SELECT * WHERE{' 
	query = query + uri + ' ?p ?o .' 
	query = query + '}'

	sparql.setQuery(query)	

	g = Graph()

	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	for result in results["results"]["bindings"]:
		print(result)
		if (result['o']['type'] == 'uri'):
			g.add( (URIRef(uri_no_bracket), URIRef(result['p']['value']) , URIRef(result['o']['value'])) )
		else:
			if 'datatype' in result['o']:
				g.add( (URIRef(uri_no_bracket), URIRef(result['p']['value']) , Literal(result['o']['value'], datatype=URIRef(result['o']['datatype']))) )
			else:
				g.add( (URIRef(uri_no_bracket), URIRef(result['p']['value']) , Literal(result['o']['value'])) )


	
	if (type == 'xml'):
		return g.serialize(format="xml")
	elif (type == 'n3'):
		return g.serialize(format="n3")
	elif (type == 'nt'):
		return g.serialize(format="nt")
	elif (type == 'turtle'):
		return g.serialize(format="turtle")
	elif (type == 'jsonld'):
		return g.serialize(format="json-ld")
	else:	
		return g.serialize(format="nt")



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

	product_uris = []
	for p in product:
		product_uris.append('<'+p+'>')

	event_work_map = return_works_from_event(product_uris)

	product_with_labels = []
	for p in product:
		product_with_labels.append([p,event_work_map[p]])


	event = {
		'dcterms_date' : dates,
		'rdf_type' : types,
		'rdfs_label' : labels,
		'rdfs_label_string' : (',').join(labels),
		'unmapped' : unmapped,
		'people' : people,
		'product': product_with_labels,
		'venues' : venues
	}




	return event
	

def format_product_dict(product_uri):

	o = return_objects(product_uri)
	s = return_subjects(product_uri)

	print(o)
	print(s)

	types = []
	unmapped = []
	events = []

	for result in o["results"]["bindings"]:
		if result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		else:
			unmapped.append([result['p']['value'], result['o']['value']])


	for result in s["results"]["bindings"]:
		if result['p']['value'] == 'http://purl.org/NET/c4dm/event.owl#product':
			events.append('<'+result['s']['value']+'>')



	work_labels = return_works_from_event([product_uri])
	for key in work_labels:
		work_labels = [[key,work_labels[key]]]


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

	events = []

	for key in events_map:
		events.append([key,events_map[key]['rdfs:label'],events_map[key]['dcterms:date']])


	product = {
		'rdf_type': types,
		'work_label' : work_labels[0][1],
		'events' : events
	}

	return product



def format_venues_dict(venue_uri):
	o = return_objects(venue_uri)
	s = return_subjects(venue_uri)

	types = []
	labels = []
	unmapped = []
	comment = []
	parent = []
	historical_name = []
	contains_place = []

	for result in o["results"]["bindings"]:
		if result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#comment':
			comment.append(result['o']['value'])
		elif result['p']['value'] == 'http://purl.org/dc/terms/date':
			dates.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.geonames.org/ontology#parentFeature':
			parent.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			labels.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.geonames.org/ontology#historicalName':
			historical_name.append(result['o']['value'])
		elif result['p']['value'] == 'http://schema.org/containsPlace':
			contains_place.append(result['o']['value'])
		else:
			unmapped.append([result['p']['value'], result['o']['value']])




	venue = {
		'rdf_type' : types,
		'rdfs_label' : labels,
		'unmapped' : unmapped,
		'parent' : parent,
		'comment': comment,
		'historical_name' : historical_name,
		'contains_place' : contains_place
	}




	return venue

def format_roles_dict(role_uri):
	o = return_objects(role_uri)
	s = return_subjects(role_uri)

	types = []
	labels = []
	unmapped = []
	comment = []

	for result in o["results"]["bindings"]:
		if result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#comment':
			comment.append(result['o']['value'])
		elif result['p']['value'] == 'http://purl.org/dc/terms/date':
			dates.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			labels.append(result['o']['value'])
		else:
			unmapped.append([result['p']['value'], result['o']['value']])


	role = {
		'rdf_type' : types,
		'rdfs_label' : labels,
		'unmapped' : unmapped,
		'comment': comment
	}
	return role

def format_instruments_dict(instrument_uri):
	o = return_objects(instrument_uri)
	s = return_subjects(instrument_uri)

	types = []
	labels = []
	unmapped = []
	comment = []

	for result in o["results"]["bindings"]:
		if result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#comment':
			comment.append(result['o']['value'])
		elif result['p']['value'] == 'http://purl.org/dc/terms/date':
			dates.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			labels.append(result['o']['value'])
		else:
			unmapped.append([result['p']['value'], result['o']['value']])


	instrument = {
		'rdf_type' : types,
		'rdfs_label' : labels,
		'unmapped' : unmapped,
		'comment': comment
	}




	return instrument

def format_names_dict(name_uri):
	o = return_objects(name_uri)
	s = return_subjects(name_uri)

	types = []
	labels = []
	name = []
	unmapped = []
	comment = []
	parent = []
	match = []
	profession_or_occupation = []
	labels_map = []
	played_instrument = []
	birth = []
	death = []

	for result in o["results"]["bindings"]:
		if result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#comment':
			comment.append(result['o']['value'])
		elif result['p']['value'] == 'http://purl.org/dc/terms/date':
			dates.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			types.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.geonames.org/ontology#parentFeature':
			parent.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
			labels.append(result['o']['value'])
		elif result['p']['value'] == 'http://xmlns.com/foaf/0.1/name':
			name.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.geonames.org/ontology#historicalName':
			historical_name.append(result['o']['value'])
		elif result['p']['value'] == 'http://schema.org/containsPlace':
			contains_place.append(result['o']['value'])
		elif result['p']['value'] == 'http://d-nb.info/standards/elementset/gnd#professionOrOccupation':
			labels_map.append('<'+result['o']['value']+'>')
			profession_or_occupation.append(result['o']['value'])
		elif result['p']['value'] == 'http://d-nb.info/standards/elementset/gnd#playedInstrument':
			played_instrument.append(result['o']['value'])
			labels_map.append('<'+result['o']['value']+'>')

		elif result['p']['value'] == 'http://xmlns.com/foaf/0.1/name':
			name.append(result['o']['value'])
		elif result['p']['value'] == 'http://www.w3.org/2004/02/skos/core#exactMatch':
			match.append(result['o']['value'])

		elif result['p']['value'] == 'http://schema.org/birthDate':
			birth.append(result['o']['value'])
		elif result['p']['value'] == 'http://schema.org/deathDate':
			death.append(result['o']['value'])
		else:
			result['p']['value'] = result['p']['value'].replace('http://schema.org/','schema:')
			result['p']['value'] = result['p']['value'].replace('http://dbpedia.org/ontology/','dbo:')



			unmapped.append([result['p']['value'], result['o']['value']])


	labels_map = return_name(labels_map)

	played_instrument_with_labels = []
	profession_or_occupation_with_labels = []
	for p in played_instrument:
		for result in labels_map["results"]["bindings"]:
			if result['uri']['value'] in p:
				played_instrument_with_labels.append([p,result['o']['value']])

	for p in profession_or_occupation:
		for result in labels_map["results"]["bindings"]:
			if result['uri']['value'] in p:
				profession_or_occupation_with_labels.append([p,result['o']['value']])





	if len(name) > 0:
		display_name = name[0] 

	if len(labels) > 0:
		display_name = labels[0] 
	name = {
		'rdf_type' : types,
		'rdfs_label' : labels,
		'display_name': display_name,
		'name' : name,
		'unmapped' : unmapped,
		'parent' : parent,
		'comment': comment,
		'match' : match,
		'birth' : birth,
		'death' : death,
		'profession_or_occupation': profession_or_occupation_with_labels,
		'played_instrument': played_instrument_with_labels
	}




	return name
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

