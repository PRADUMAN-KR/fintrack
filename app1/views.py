from django.shortcuts import render,redirect
from .models import Transaction, Budget
from django.db.models import Sum
from .forms import TransactonForm

def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'index.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
    })



# adding the Transaction through the forms

# def Add_Transaction(request):
#     if request.method =='POST':
#         form = TransactonForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             transaction.user = request.user
#             transaction.save()
#             return redirect('dashboard')
#     else:
#         form = TransactonForm()
#     return render(request, 'add_transaction.html', {'form': form})
            

def get_transaction(request):
    return render(request, 'index.html') 

def all_transaction(request):
    transactions = Transaction.objects.all()
    return render(request, 'index.html', {'is_transc': True, 'transactions': transactions}) 

def get_budget(request):
    total_amt = Budget.objects.filter(total_balance=0).values_list('total_balance', flat=True)
    print(total_amt)
    return render(request, 'index.html',{'total_amount':total_amt})