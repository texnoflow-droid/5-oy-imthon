from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add-category/', views.add_category, name='add_category'),
    path('cards/', views.cards, name='cards'),
    path('cards/delete/<int:pk>/', views.delete_card, name='delete_card'),
]