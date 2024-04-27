from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json

# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({
                'username_error': 'username should only contain alphanumeric!'
            })
        return JsonResponse({ 'username_valid': True})

def register(request):
    return render(request, 'authentication/register.html')

def login(request):
    return render(request, 'authentication/login.html') 