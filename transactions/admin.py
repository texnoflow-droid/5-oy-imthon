from django.contrib import admin

# Register your models here.
from .models import Transaction, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'type', 'category', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['title', 'description']
