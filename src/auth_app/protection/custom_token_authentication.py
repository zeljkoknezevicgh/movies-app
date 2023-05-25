from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token


class CustomTokenAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            raise exceptions.AuthenticationFailed({'message': 'Header not provided!'}, code=401)
        try:
            key = header.split(' ')[1]
        except:
            raise exceptions.AuthenticationFailed({'message': 'Bad Token Format!'}, code=401)
        try:
            token = Token.objects.get(key=key)
        except:
            raise exceptions.AuthenticationFailed({'message': 'Invalid Token'}, code=401)
        return token.user, token