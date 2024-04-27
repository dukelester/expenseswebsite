from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

# Create your views here.

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
    return render(request, 'authentication/register.html')

def login(request):
    return render(request, 'authentication/login.html') 