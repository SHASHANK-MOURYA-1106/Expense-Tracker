from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Render the index page of the Expense Tracker application.
    
    This view handles the request to the root URL and returns the index.html template.
    """
    return render(request, 'index.html')