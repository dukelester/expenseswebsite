from django.shortcuts import render
import os
import json
from django.conf import settings
# Create your views here.


def index(request):
    curreny_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    # import pdb; pdb.set_trace()
    with open(file_path, 'r') as file:
        data = json.load(file)
        for key, value in data.items():
            curreny_data.append({'name': key, 'value': value})
    return render(request, 'preferences/index.html', { 'currencies': curreny_data })
