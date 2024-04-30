from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . models import Category, Expense

# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    return render(request, 'expenses/index.html')

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
        print(amount, description, category, expense_date)
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
            messages.error(request, f'{e} \n The Expense was added successfully!')
            return render(request, 'expenses/add_expense.html', context)
    return render(request, 'expenses/add_expense.html', context)
