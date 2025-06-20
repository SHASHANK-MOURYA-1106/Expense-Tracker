from django.shortcuts import render,redirect
from django.contrib import messages
from .models import CurrentBalance, TrackingHistory, RequestLogs
# Create your views here.
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