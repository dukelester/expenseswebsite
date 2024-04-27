from django.urls import path


from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('validate_username', views.UsernameValidationView.as_view(), name='validate_username'),
    path('login', views.login, name='login'),
]
