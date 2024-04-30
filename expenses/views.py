from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . models import Category

# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    return render(request, 'expenses/index.html')

@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'expenses/add_expense.html', context)
