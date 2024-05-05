from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('validate_username', csrf_exempt(views.UsernameValidationView.as_view()),
        name='validate_username'),
    path('success', views.register_success, name='success'),
    path('validate_email', csrf_exempt(views.EmailValidationView.as_view()),
        name='validate_email'),
    path('activate/<uidb64>/<token>', views.EmailVerificationView.as_view(), name='activate'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('request_rest_link', views.password_reset, name='request_rest_link'),
    path('reset_user_password/<uidb64>/<token>',views.reset_user_password,
        name='reset_user_password'),
]
