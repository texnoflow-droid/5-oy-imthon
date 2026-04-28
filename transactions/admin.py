from django.contrib import admin
from .models import Transaction, Category, Profile, Card, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'type', 'user', 'card', 'created_at']
    list_filter = ['type', 'category', 'card']
    search_fields = ['title', 'description']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'card_number', 'balance', 'card_type', 'user', 'is_active']
    list_filter = ['card_type', 'is_active']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'limit_amount', 'month']