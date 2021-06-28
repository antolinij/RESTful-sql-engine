from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status
from django.utils.encoding import force_text


# maybe I should move this to utils.custom_exception_handler
class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = force_text(detail)
        else: self.detail = {'detail': force_text(self.default_detail)}