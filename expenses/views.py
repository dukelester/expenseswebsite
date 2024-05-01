from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from . models import Category, Expense

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
        expenses = (Expense.objects.filter(amount__istartswith=search_text, user=request.user) |
                    Expense.objects.filter(date__istartswith=search_text, user=request.user) |
                    Expense.objects.filter(description__icontains=search_text, user=request.user) |
                    Expense.objects.filter(category__icontains=search_text, user=request.user)
                    )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(user=request.user).all()
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)
    context = { 'expenses': expenses, 'page_object': page_object }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        expense_date = request.POST.get('expense_date')

        if not amount:
            messages.error(request, 'The amount cant be empty!')
            return render(request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'The description cant be empty!')
            return render(request, 'expenses/add_expense.html', context)
        try:
            expense = Expense.objects.create(
                amount=amount,  date=expense_date,
                description=description, user=request.user,
                category=category)
            expense.save()
            messages.success(request, 'The Expense was added successfully!')
            return redirect('expenses')
        except Exception as e:
            messages.error(request, f'{e} \n Adding the expense caused an error')
            return render(request, 'expenses/add_expense.html', context)
    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='authentication/login')
def edit_expense(request, expense_id):
    expense = Expense.objects.get(pk=expense_id)
    context = {
        'expense': expense,
        'values': expense,
        'categories': Category.objects.all(),
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        expense_date = request.POST.get('expense_date')

        if not amount:
            messages.error(request, 'The amount cant be empty!')
            return render(request, 'expenses/edit_expense.html', context)
        if not description:
            messages.error(request, 'The description cant be empty!')
            return render(request, 'expenses/edit_expense.html', context)
        try:
            expense.amount = amount
            expense.category = category
            expense.description = description
            expense.date = expense_date
            expense.save()
            messages.success(request, 'The Expense was updated successfully!')
            return redirect('expenses')
        except Exception as e:
            messages.error(request, f'{e} \n Error occurred while updating')
            return render(request, 'expenses/edit_expense.html', context)
    return render(request, 'expenses/edit_expense.html', context)


@login_required(login_url='authentication/login')
def delete_expense(request, expense_id):
    expense = Expense.objects.get(pk=expense_id)
    try:
        expense.delete()
        messages.success(request, 'The expense has been successfully deleted!')
        return redirect('expenses')
    except Exception as e:
        messages.error(request, f'{e} \n Error occurred while deleting')
        return redirect('expenses')
