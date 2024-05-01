from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.index, name='incomes'),
    path('add_income', views.add_user_income, name='add_income'),
    path('edit_income/<int:income_id>', views.edit_user_income, name='edit_income'),
    path('delete_income/<int:income_id>', views.delete_user_income, name='delete_income'),
    path('search_income', csrf_exempt(views.search_user_income), name='search_income'),
]
