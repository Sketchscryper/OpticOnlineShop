from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'created', 'paid']
    list_filter = ['paid', 'created']
    search_fields = ['full_name', 'email', 'phone']
    inlines = [OrderItemInline]
