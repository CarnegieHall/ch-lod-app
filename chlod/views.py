from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

from . import utils

@csrf_exempt
def route_sparql_query(request):

	r = requests.post(settings.SPARQL_ENDPOINT, headers={"Accept":"application/sparql-results+json"}, data = {'query':request.body.decode('utf-8')})


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





def route_works(request, id):
	if 'text/htm' in request.META.get('HTTP_ACCEPT'):
		response = HttpResponse(content="", status=303)
		response["Location"] = '/works/'+id+'/about'
		return response
	else:
		response = HttpResponse(content="", status=303)
		response["Location"] = '/works/'+id+'/about'
		return response

def about_works(request,id):
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


def about_events(request,id):
	data = utils.format_events_dict("<http://data.carnegiehall.org/events/%s>" % (id))

	template = loader.get_template('events/events.html')
	context = {
	    'data': data,
	}
	return HttpResponse(template.render(context, request))






