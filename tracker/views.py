from django.shortcuts import render,redirect
from django.contrib import messages
from .models import CurrentBalance, TrackingHistory, RequestLogs
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.success(request, "Username not found") 
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)
        if not user:
            messages.success(request, "Incorrect password") 
            return redirect('/login/')        
        login(request , user)
        return redirect('/')

    return render(request , 'login.html')
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.success(request, "Username is already taken") 
            return redirect('/register/')
        
        user = User.objects.create(
            username = username,
            first_name = first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created") 
        return redirect('/register/')
    return render(request , 'register.html')


@login_required(login_url='login_view')
def index(request):
    """
    Render the index page of the Expense Tracker application.
    
    This view handles the request to the root URL and returns the index.html template.
    """
    if request.method == 'POST':
        # Handle POST request logic here if needed
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        current_balance,_= CurrentBalance.objects.get_or_create(id = 1)
        expense_type = "CREDIT"
        if float(amount) < 0:
            expense_type = "DEBIT"

        if float(amount) == 0:
            messages.success(request, "Amount cannot be zero") 
            return redirect('/')
        tracking_history = TrackingHistory.objects.create(amount = amount,
            expense_type = expense_type,
            current_balance = current_balance,
            description = description)
        current_balance.balance += float(tracking_history.amount)
        current_balance.save()
        print(f"Description: {description}, Amount: {amount}")
        return redirect('/')
    current_balance = CurrentBalance.objects.get_or_create(id = 1)
    income = 0
    expense = 0
    
    for tracking_history in TrackingHistory.objects.all():
        if tracking_history.expense_type == "CREDIT":
            income += tracking_history.amount
        else:
            expense += tracking_history.amount
    context={'transactions': TrackingHistory.objects.all(),
             'current_balance': CurrentBalance.objects.get(id=1),'income': income,'expense': expense}
    return render(request, 'index.html',context)
 
def delete_transaction(request, id):
    tracking_history = TrackingHistory.objects.filter(id = id)

    if tracking_history.exists():
        current_balance, _ = CurrentBalance.objects.get_or_create(id = 1)
        tracking_history = tracking_history[0]
        
        current_balance.balance = current_balance.balance - tracking_history.amount

        current_balance.save()


    tracking_history.delete()
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/login/')