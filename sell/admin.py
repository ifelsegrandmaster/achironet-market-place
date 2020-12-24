from django.contrib import admin
from .models import Revenue, BankDetails
# Register your models here.



@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['month', 'sales', 'products_sold', 'seller', 'bank_details']

@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'bank_account', 'revenue']
