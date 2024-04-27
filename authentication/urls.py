from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('validate_username', csrf_exempt(views.UsernameValidationView.as_view()), name='validate_username'),
    path('login', views.login, name='login'),
]
