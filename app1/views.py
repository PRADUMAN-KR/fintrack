from django.shortcuts import render,redirect
from .models import Transaction, Budget
from django.db.models import Sum
from .forms import add_transaction_form
from django.contrib.auth import authenticate,login
from .models import custom_user
from django.contrib import messages
from django.contrib.auth.hashers import make_password





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




#---------------------signup and login------------------------------

def signup_view(request):
    form_type = request.GET.get("type",login)

    if request.method =="POST":
        if form_type == 'register':
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')

            if not all([username, email, password, phone_number, confirm_password]):
                messages.error(request, "All fields are required")
                return redirect('/auth/?type=register')
            if password != confirm_password:
                messages.error(request, "passwords do not match")
                return redirect(f'/auth/?type=register')
            
            if custom_user.objects.filter(email = email).exists():
                messages.error(request,"email is already present")
                return redirect(f'/auth/?type=register')
            
            #create user:
            user = custom_user(
                username = username,
                email = email,
                phone_number = phone_number,
                password = make_password(password)
            )
            user.save()

            messages.success(request, "user created successfully")
            return redirect(f'/auth/?type=login')
        
        elif form_type == 'login':
            # email = request.POST.get('email')
            # password = request.POST.get('password')

            # user = authenticate(request, email=email, password=password)
            # if user is not None:
            #     login(request, user)
            #     return redirect('home')
            # else:
            #     messages.error(request, "invalid credentials")
            #     return redirect('auth')


            email = request.POST.get('email')
            password = request.POST.get('password')
            
            # Authenticate using the custom backend
            user = custom_user.objects.filter(email=email).first()
            print(password, "###################",user)
            if user and user.check_password(password):
            # user = authenticate(request, email=email, password=password)
            
            # if user is not None:
                login(request, user)
                
                return redirect('home')  # Redirect to home or dashboard
            else:
                messages.error(request, "Invalid credentials")
                return redirect('auth')  # Or your login URL or pag

        
    return render(request, 'login_register.html',{'form_type': form_type})








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
