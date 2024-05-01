from django.contrib import admin

# Register your models here.
from .models import SourceOfIncome, UserIncome

admin.site.register(SourceOfIncome)
admin.site.register(UserIncome)