from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
import re


from . import utils

limit_re = re.compile('LIMIT\s([0-9]+)', re.IGNORECASE)


content_type_map = {
	'xml' : 'text/xml',
	'turtle' : 'text/turtle',
	'jsonld' : 'application/ld+json',
	'n3' : 'text/n3',
	'nt' : 'text/plain',
}

@csrf_exempt
def route_sparql_query(request):

	query = request.body.decode('utf-8')

	if (len(request.body.decode('utf-8')) == 0):
		query = request.GET.get('query', '')


	# add a limit to it if ther is not one yet
	re_match = limit_re.search(query)
	
	if re_match == None:
		query = query + ' LIMIT 10000'
	else:
		if int(re_match.group(1)) > 10000:
			query = query.replace(re_match.group(),'LIMIT 10000')
		
	r = requests.post(settings.SPARQL_ENDPOINT, headers={"Accept":"application/sparql-results+json"}, data = {'query':query})
	# print(request.body.decode('utf-8'))
	return HttpResponse(content=r.text, status=200)

@csrf_exempt
def route_sparql(request):


	isKey = request.GET.get('key', False)

	if isKey != False:
		return HttpResponse(content="", status=200)
	else:
		template = loader.get_template('main/sparql.html')
		context = {
		    'data': None,
		}
		return HttpResponse(template.render(context, request))



def route_homepage(request):
		response = HttpResponse(content="",status=302)
		response["Location"] = '/sparql'
		return response


def route_works(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/works/'+id+'/about'
		return response

	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/works/'+id+'/about'
		return response

def about_works(request,id,type):

	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/works/%s>" % (id),type), content_type=content_type_map[type], status=200)
	else:
		data = utils.format_works_dict("<http://data.carnegiehall.org/works/%s>" % (id))
		template = loader.get_template('works/works.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))


def route_events(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/events/'+id+'/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/events/'+id+'/about'
		return response


def about_events(request,id,type):
	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/events/%s>" % (id),type), content_type=content_type_map[type], status=200)
	else:
		data = utils.format_events_dict("<http://data.carnegiehall.org/events/%s>" % (id))

		template = loader.get_template('events/events.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))


def route_products(request, id,product_id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/events/'+id+'/work_' + product_id + '/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/events/'+id+'/about'
		return response


def about_products(request,id,product_id,type):
	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/events/%s/work_%s>" % (id,product_id),type),  content_type=content_type_map[type], status=200)
	else:
		data = utils.format_product_dict("<http://data.carnegiehall.org/events/%s/work_%s>" % (id,product_id))

		template = loader.get_template('events/products.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))




def route_venues(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/venues/'+id+'/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/venues/'+id+'/about'
		return response


def about_venues(request,id,type):
	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/venues/%s>" % (id),type), content_type=content_type_map[type], status=200)
	else:
		data = utils.format_venues_dict("<http://data.carnegiehall.org/venues/%s>" % (id))

		template = loader.get_template('venues/venues.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))



def route_instruments(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/instruments/'+id+'/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/instruments/'+id+'/about'
		return response


def about_instruments(request,id,type):
	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/instruments/%s>" % (id),type), content_type=content_type_map[type], status=200)
	else:
		data = utils.format_instruments_dict("<http://data.carnegiehall.org/instruments/%s>" % (id))

		template = loader.get_template('instruments/instruments.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))



def route_roles(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/roles/'+id+'/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/roles/'+id+'/about'
		return response


def about_roles(request,id,type):
	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/roles/%s>" % (id),type), content_type=content_type_map[type], status=200)
	else:
		data = utils.format_roles_dict("<http://data.carnegiehall.org/roles/%s>" % (id))

		template = loader.get_template('roles/roles.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))




def route_names(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/names/'+id+'/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/names/'+id+'/about'
		return response


def about_names(request,id,type):
	if type == 'xml'  or type == 'turtle' or type == 'jsonld' or type == 'n3' or type == 'nt':
		return HttpResponse(content=utils.return_serialized_subjects("<http://data.carnegiehall.org/names/%s>" % (id),type), content_type=content_type_map[type], status=200)
	else:
		data = utils.format_names_dict("<http://data.carnegiehall.org/names/%s>" % (id))

		template = loader.get_template('names/names.html')
		context = {
		    'data': data,
		}
		return HttpResponse(template.render(context, request))




