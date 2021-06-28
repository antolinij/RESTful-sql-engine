#import ipdb

# django rest
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    

    handlers = {
        'ImproperlyConfigured': _handle_generic_error,
    }
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response

def _handle_generic_error(exc, context, response):
    return Response(data=str(exc), status=status.HTTP_400_BAD_REQUEST)