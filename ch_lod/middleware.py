"""
Middleware to restrict access to requests coming through AWS CloudFront.
No requests allowed to the app through the heroku app url.
"""

import logging
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)
class CloudFrontOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.META.get('HTTP_X_AMZ_CF_ID'):
            return HttpResponseForbidden()
        
        logger.info(
            'ua="%s" path="%s" ip="%s"',
            request.META.get('HTTP_USER_AGENT', ''),
            request.path,
            request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip(),
        )

        return self.get_response(request)