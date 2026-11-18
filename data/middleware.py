import threading

_thread_locals = threading.local()


def get_client_ip():
    return getattr(_thread_locals, 'client_ip', None)


class ClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        _thread_locals.client_ip = (
            forwarded_for.split(',')[0].strip() if forwarded_for
            else request.META.get('REMOTE_ADDR', '')
        )
        try:
            return self.get_response(request)
        finally:
            _thread_locals.client_ip = None