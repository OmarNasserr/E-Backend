from rest_framework.exceptions import APIException
from rest_framework import  status


class PermissionDenied(APIException):
        status_code = status.HTTP_403_FORBIDDEN
        default_detail = {'message': 'You do not have permission to perform this action.',
                          'status': status.HTTP_403_FORBIDDEN,}
        default_code = 'permission_denied'

class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {'message': 'Authentication credentials were not provided.',
                    'status': status.HTTP_401_UNAUTHORIZED,}
    default_code = 'not_authenticated'
    
    