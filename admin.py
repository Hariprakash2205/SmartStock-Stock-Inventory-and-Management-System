from django.contrib import admin
from .models import Department, StockItem, StockRequest, Transaction

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'quantity',"vendor_name",     # 🔹 NEW
        "purchase_date", 'created_at')
    list_filter = ('department','vendor_name')  # 🔹 NEW
    search_fields = ('name','vendor_name')  # 🔹 NEW

@admin.register(StockRequest)
class StockRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'requester', 'quantity', 'status', 'requested_at')
    list_filter = ('status',)
    search_fields = ('item__name', 'requester__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'quantity_changed', 'performed_by', 'timestamp')
    search_fields = ('item__name',)
