from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from dotenv import load_dotenv
from validate_email import validate_email

import json
import os
# Create your views here.
from .utills import token_generator

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
                    # create the uid
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    # Get the current email
                    domain = get_current_site(request).domain
                    # get the link
                    link = reverse('activate', kwargs={ 'uidb64': uidb64,
                                                    'token': token_generator.make_token(user)})
                    activate_url = f'http://{domain}/{link}'
                    messages.success(request, 'Account successfully Created')
                    subject = 'Activate your Account'
                    email_body = f'''
                    Hello {user.username}
                    Your account has been created successfully.
                    Click on the link below to verify your account
                    {activate_url}
                    '''
                    email = EmailMessage(
                        subject,
                        email_body,
                        os.getenv("DEFAULT_FROM_EMAIL"),
                        [email,],
                    )
                    email.send(fail_silently=False)
                    return redirect('/authentication/success')
                messages.info(request, 'Password must match')
                return render(request, 'authentication/register.html', context)
    return render(request, 'authentication/register.html')

class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not token_generator.check_token(user, token):
                messages.info(request, 'Your account has been activated. Login now')
                return redirect('/authentication/login')
            if user.is_active:
                return redirect('/authentication/login')
            user.is_active = True
            user.save()
            messages.success(request,
                            'Your account has been activated successfully! Proceed to login')
            return redirect('/authentication/login')
        except Exception as e:
            JsonResponse({'error': e})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {user.username}. You are now logged in')
                    return redirect('expenses')
                messages.error(request, 'Your account is not active. Check your email to activate')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid user credentials')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Details Cannot be null')
        return render(request, 'authentication/login.html')
    return render(request, 'authentication/login.html')

def  register_success(request):
    return render(request, 'authentication/success_registration.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('/authentication/login')


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        context = {
            'values': request.POST,
        }
        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'authentication/reset-password.html')
        user = User.objects.filter(email=email)
        print(user)
        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            # Get the current email
            domain = get_current_site(request).domain
            # get the link
            link = reverse('reset_user_password',
                        kwargs={
                            'uidb64': uidb64,
                            'token': PasswordResetTokenGenerator().make_token(user[0]),
                            })
            reset_password_link = f'http://{domain}/{link}'
            subject = 'Password Reset'
            email_body = f'''
            Hello {user[0].username}
            Your password reset request has been received.
            Click on the link below to reset your password.
            {reset_password_link}
            '''
            email = EmailMessage(
                subject,
                email_body,
                os.getenv("DEFAULT_FROM_EMAIL"),
                [email,],
            )
            email.send(fail_silently=False)
            return redirect('/authentication/success')
        messages.success(request, '''We have sent you an email.
                        Follow the instructions to reset your password.''')
        return render(request, 'authentication/reset-password.html', context)
    return render(request, 'authentication/reset-password.html')


def reset_user_password(request, uidb64, token):
    
    return render(request, 'authentication/set-newpassword.html')
    