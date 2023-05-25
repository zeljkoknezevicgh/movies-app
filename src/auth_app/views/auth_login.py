from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView




class LoginAPIView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse({'message': 'Username or password is not correct!'}, status=400)
        token = Token.objects.filter(user=user)
        if token:
            token.delete()
        token = Token.objects.create(user=user).key
        return JsonResponse({
            'message': 'Succesfully authenticated!',
            'token': token,
            'user_id': user.id
        }, status=200)