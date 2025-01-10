from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices = Transaction_type, max_length=50)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.type}- {self.amount}'
    
# ----------------------------budget model----------------------------------------
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.limit}"

