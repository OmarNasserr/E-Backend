from rest_framework import status
class Status_code():
    success=status.HTTP_200_OK
    created=status.HTTP_200_OK
    updated=status.HTTP_200_OK
    deleted=status.HTTP_200_OK
    no_content=status.HTTP_204_NO_CONTENT
    internal_server_err=status.HTTP_500_INTERNAL_SERVER_ERROR
    version_err=status.HTTP_306_RESERVED
    bad_request=status.HTTP_400_BAD_REQUEST
    unauthorized=status.HTTP_401_UNAUTHORIZED
    forbidden=status.HTTP_403_FORBIDDEN
    payment_required=status.HTTP_402_PAYMENT_REQUIRED
    un_supported_media_type=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE