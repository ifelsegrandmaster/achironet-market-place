from django.contrib import admin
from .models import Order, OrderItem, ShippingInformation, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class ShippingInformationInline(admin.TabularInline):
    model = ShippingInformation

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline, ShippingInformationInline]

admin.site.register(Payment)