from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.contrib.auth.models import AbstractUser
# Create your models here.


class custom_user(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
# ---------------------transaction model----------------------

class Transaction(models.Model):
    Transaction_type = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
        ('loan', 'Loan'),
        ('repayment', 'Repayment'),
        ('investment', 'Investment'),
        ('savings', 'Savings'),
        ('food', 'Food'),
        ('others', 'Others'),
    ]
    user = models.ForeignKey(custom_user, on_delete=models.CASCADE)
    type = models.CharField(choices = Transaction_type, max_length=50)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    date = models.DateField()   
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.type}- {self.amount}'
    
# ----------------------------budget model----------------------------------------
class Budget(models.Model):
    user = models.ForeignKey(custom_user, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income =  models.DecimalField(max_digits=10, decimal_places=2)
    savings = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)

   
    def save(self,*args,**kwargs):
        # self.clean()
        self.total_balance = self.income - self.expenses
        self.savings = self.total_balance
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.category} - {self.limit}"


#-----------------------------login----------------------------------------------

