from django.shortcuts import render,redirect
from .models import Transaction, Budget
from django.db.models import Sum
from .forms import add_transaction_form

def get_data(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_amt = Budget.objects.first()
    return {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'total_amount': total_amt.total_balance if total_amt else 0,
    }

def dashboard(request):
    context = get_data(request)

    return render(request, 'index.html', context)

            

def get_transaction(request):

    return render(request, 'index.html') 

def all_transaction(request):
    context = get_data(request)
    context['is_transc'] = True
    return render(request, 'index.html', context) 




#---------------------login------------------------------
def register_login(request):
    return render(request,'login_register.html')



# ------------------views for the transaction form---------------------

def add_Transaction(request):
    if request.method == "POST":
        form = add_transaction_form(request.post)
        if form.is_valid():
            Transaction = form.save(commit=False)
            Transaction.user = request.user
            Transaction.save()
            return redirect('transactions') 

    else:
        form = add_transaction_form()
    return render(request, 'add_transaction.html', {'form': form})
