from django import forms

from .models import Transaction

    
class TransactonForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'date']