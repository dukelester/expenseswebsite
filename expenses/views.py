from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum

import datetime
import json
import csv
import tempfile

import xlwt
from weasyprint import HTML


from . models import Category, Expense
from userpreferences.models import UserPreferences

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
    currency = UserPreferences.objects.get(user=request.user).currency
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)
    context = { 'expenses': expenses, 'page_object': page_object, 'currency': currency }
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


def expenses_category_summary(request):
    todays_date = datetime.date.today()
    print('Todays date is ', todays_date)
    # Six months ago
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    print('six months ago', six_months_ago)
    expenses = Expense.objects.filter(user=request.user,
        date__gte=six_months_ago, date__lte=todays_date
    )
    final_data = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))
    print('category_list', category_list)
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for expense in expenses:
        for category in category_list:
            final_data[category] = get_expense_category_amount(category)
    return JsonResponse({'expense_category_data': final_data}, safe=False)

def stats_view(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"""attachment; filename=Expenses{str(datetime.datetime.now())}.csv"""
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    expenses = Expense.objects.filter(user=request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.description,
                        expense.category, expense.date])
    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"""attachment; filename=Expenses{str(datetime.datetime.now())}.xls"""
    workbook = xlwt.Workbook(encoding='utfg-8')
    wooksheet = workbook.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Description', 'Category', 'Date']
    for col_num in range(len(columns)):
        wooksheet.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(user=request.user).values_list(
        'amount', 'description', 'category', 'date'
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            wooksheet.write(row_num, col_num, str(row[col_num]), font_style)
    workbook.save(response)
    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"""inline; attachment; filename=Expenses{str(datetime.datetime.now())}.pdf"""
    response['Content-Transfer-Encoding'] = 'binary'
    
    html_string = render_to_string('expenses/pdf_output.html', {
        'expenses': [], 'total': 0
    })
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
