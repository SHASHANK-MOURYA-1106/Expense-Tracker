# admin.py
from django.contrib import admin
from tracker.models import *

admin.site.site_header = "Expense Tracker"
admin.site.site_title = "Expense Tracker"
admin.site.site_url = "Expense Tracker"

admin.site.register(CurrentBalance)

class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "amount",
        "current_balance",
        "expense_type",
        "description",
        "created_at"
    
    ]

    search_fields = ['expense_type', 'description']
    list_filter = ['expense_type']
    ordering = ['-expense_type']

admin.site.register(TrackingHistory, TrackingHistoryAdmin)