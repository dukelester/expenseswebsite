from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>', views.delete_expense, name='delete_expense'),
    path('search_expense', csrf_exempt(views.search_expenses), name='search_expense'),
    path('expenses_category_summary', views.expenses_category_summary,
        name='expenses_category_summary'),
    path('stats', views.stats_view, name='stats'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('export_excel', views.export_excel, name='export_excel'),
]
