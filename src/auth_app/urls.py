from django.urls import path
from .views.auth_login import LoginAPIView
from .views.auth_register import RegisterAPIView

urlpatterns = [

    path('login/', LoginAPIView.as_view(), name='auth_login'),
    path('register/', RegisterAPIView.as_view(), name='auth_register')

]