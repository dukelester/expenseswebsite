from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from . models import UserIncome, SourceOfIncome
from userpreferences.models import UserPreferences

# Create your views here.

def search_user_income(request):
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
        incomes = (
            UserIncome.objects.filter(amount__istartswith=search_text, user=request.user) |
            UserIncome.objects.filter(date__istartswith=search_text, user=request.user) |
            UserIncome.objects.filter(description__icontains=search_text, user=request.user) |
            UserIncome.objects.filter(source_of_income__icontains=search_text, user=request.user)
                    )
        data = incomes.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='authentication/login')
def index(request):
    incomes = UserIncome.objects.filter(user=request.user).all()
    currency = UserPreferences.objects.get(user=request.user).currency
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)
    context = { 'incomes': incomes, 'page_object': page_object, 'currency': currency }
    return render(request, 'income/index.html', context)

@login_required(login_url='authentication/login')
def add_user_income(request):
    sources = SourceOfIncome.objects.all()
    context = {
        'sources': sources,
        'values': request.POST,
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source_of_income = request.POST.get('source')
        user_income_date = request.POST.get('icome_date')

        if not amount:
            messages.error(request, 'The amount cant be empty!')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'The description cant be empty!')
            return render(request, 'income/add_income.html', context)
        try:
            userincome = UserIncome.objects.create(
                amount=amount,  date=user_income_date,
                description=description, user=request.user,
                source_of_income=source_of_income)
            userincome.save()
            messages.success(request, 'The UserIncome was added successfully!')
            return redirect('income')
        except Exception as e:
            messages.error(request, f'{e} \n Adding the userincome caused an error')
            return render(request, 'income/add_income.html', context)
    return render(request, 'income/add_income.html', context)


@login_required(login_url='authentication/login')
def edit_user_income(request, income_id):
    user_income = UserIncome.objects.get(pk=income_id)
    print(user_income, 'IIIIIIIIIIIII', income_id)
    context = {
        'user_income': user_income,
        'values': user_income,
        'sources': SourceOfIncome.objects.all(),
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source_of_income = request.POST.get('source')
        user_income_date = request.POST.get('icome_date')

        if not amount:
            messages.error(request, 'The amount cant be empty!')
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'The description cant be empty!')
            return render(request, 'income/edit_income.html', context)
        try:
            user_income.amount = amount
            user_income.source_of_income = source_of_income
            user_income.description = description
            user_income.date = user_income_date
            user_income.save()
            messages.success(request, 'The User Income was updated successfully!')
            return redirect('income')
        except Exception as e:
            messages.error(request, f'{e} \n Error occurred while updating')
            return render(request, 'income/edit_income.html', context)
    return render(request, 'income/edit_income.html', context)


@login_required(login_url='authentication/login')
def delete_user_income(request, income_id):
    user_income = UserIncome.objects.get(pk=income_id)
    try:
        user_income.delete()
        messages.success(request, 'The user income has been successfully deleted!')
        return redirect('income')
    except Exception as e:
        messages.error(request, f'{e} \n Error occurred while deleting')
        return redirect('income')
