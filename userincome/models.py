from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

class UserIncome(models.Model):
    amount = models.DecimalField()
    date = models.DateField(default=now)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_of_income = models.CharField(max_length=255)

    def __str__(self):
        return self.source_of_income

    class Meta:
        ordering = ['-date']

class SourceOfIncome(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Sources Of Income'

    def __str__(self):
        return self.name
