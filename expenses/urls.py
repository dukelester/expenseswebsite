from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add/', views.add_expense, name='add_expense'),
]
