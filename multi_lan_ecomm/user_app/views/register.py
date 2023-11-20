from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from ..validation import UserAppValidation
from ..serializers import RegisterationSerializer

from django.conf import settings
from helper_files.cryptography import AESCipher

aes = AESCipher(settings.SECRET_KEY[:16], 32)


@api_view(['Post',])
def registeration_view(request):

    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)

        data = {}
        valid, err = serializer.is_valid(raise_exception=False)
        print(valid)
        response = UserAppValidation.validate_user_create(
            request.data, valid, err,str(request.LANGUAGE_CODE))
        
        if response.status_code == 400:
            return response

        # we override the save method and it returns an account now
        account = serializer.save(serializer.validated_data)

        data['response'] = "Registeration Successful"
        data['id'] = aes.encrypt(str(account.id))
        data['username'] = account.username
        data['email'] = account.email

        # JWT token
        refresh = RefreshToken.for_user(account)
        data['toekn'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(data, status=status.HTTP_201_CREATED)
