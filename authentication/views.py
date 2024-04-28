from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage

from dotenv import load_dotenv
from validate_email import validate_email

import json
import os
# Create your views here.

load_dotenv()
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

def match_password(password1, password2):
    if( len(password1) == len(password2)) and password1 == password2:
        return True


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        context = {
            'field_values': request.POST,
        }

        if len(password) < 4:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/register.html', context)
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if match_password(password, confirm_password):
                    user = User.objects.create(
                        username= username,
                        email=email,
                    )
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    messages.success(request, 'Account successfully Created')
                    subject = 'Activate your Account'
                    email_body = 'Account Activation'
                    email = EmailMessage(
                        subject,
                        email_body,
                        os.getenv("DEFAULT_FROM_EMAIL"),
                        [email,],
                    )
                    email.send(fail_silently=False)
                    return JsonResponse({'success': 'suceses'})
                messages.info(request, 'Password must match')
                return render(request, 'authentication/register.html', context)
        #     messages.error(request, 'Kindly choose another Email address!')
        #     return render(request, 'authentication/register.html')
        # messages.error(request, 'Kindly choose another Username!')
        # return render(request, 'authentication/register.html')
    return render(request, 'authentication/register.html')

def login(request):
    return render(request, 'authentication/login.html')
