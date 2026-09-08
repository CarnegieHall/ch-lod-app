"""
Middleware to restrict access to requests coming through AWS CloudFront.
No requests allowed to the app through the heroku app url.
"""

from django.http import HttpResponseForbidden

class CloudFrontOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.META.get('HTTP_X_AMZ_CF_ID'):
            return HttpResponseForbidden()
        return self.get_response(request)