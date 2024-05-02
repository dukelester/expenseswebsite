from django.contrib import admin

from . import models

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'category', 'description', 'user')
    search_fields =('amount', 'category', 'description', 'user__username')

admin.site.register(models.Expense, ExpenseAdmin)
admin.site.register(models.Category)