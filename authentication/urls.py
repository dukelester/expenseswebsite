from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('validate_username', csrf_exempt(views.UsernameValidationView.as_view()),
        name='validate_username'),
    path('validate_email', csrf_exempt(views.EmailValidationView.as_view()),
        name='validate_email'),
    path('login', views.login, name='login'),
]
