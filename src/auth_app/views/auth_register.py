from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView

from auth_app.serializers.register_serializers import RegisterSerializer


class RegisterAPIView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=400)
        try:
            User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['name'],
                last_name=serializer.validated_data['lastname']
            )
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'Username or password already exists!'}, status=400)
        send_mail(
            'Congratulations, You successfull registered to our website!',
            'Your username is' + serializer.validated_data['username'],
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['email']]
        )
        return JsonResponse({'message': 'Users successfully registered!'}, status=201)
