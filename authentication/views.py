from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages


from validate_email import validate_email

import json

# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({
                'email_error': 'The email is invalid. Enter a valid email',
            }, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error': 'Invalid email, choose another email'
                }, status=409)
        return JsonResponse({ 'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({
                'username_error': 'username should only contain alphanumeric!',
            }, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': 'Invalid username, choose another username'
                }, status=409)
        return JsonResponse({ 'username_valid': True})

def register(request):
    if request.method == 'POST':
        messages.success(request, 'success message')
    return render(request, 'authentication/register.html')

def login(request):
    return render(request, 'authentication/login.html')
