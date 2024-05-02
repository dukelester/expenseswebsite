from django.contrib import admin

# Register your models here.
from .models import SourceOfIncome, UserIncome


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'source_of_income', 'date', 'user')
    search_fields = ('description', 'amount', 'date', 'source_of_income', 'user__username')

admin.site.register(SourceOfIncome)
admin.site.register(UserIncome, IncomeAdmin)