import os
import json
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

from . models import UserPreferences
# Create your views here.


def index(request):
    print(request)
    curreny_data = []
    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    # import pdb; pdb.set_trace()
    with open(file_path, 'r') as file:
        data = json.load(file)
        for key, value in data.items():
            curreny_data.append({'name': key, 'value': value})

    if request.method == 'POST':
        currency = request.POST.get('currency')
        print(currency, 'currrrrrrrrrrrrrrrrrrrr')
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            user_currency = UserPreferences.objects.create(user=request.user, currency=currency)
            user_currency.save()
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html',{ 'currencies': curreny_data,
                                                        'user_preferences': user_preferences })
    return render(request, 'preferences/index.html', { 'currencies': curreny_data,
                                                'user_preferences': user_preferences })
