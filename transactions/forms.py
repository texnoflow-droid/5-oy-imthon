from django import forms
from django.contrib.auth.models import User
from .models import Transaction, Profile, Card


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos kelmadi!")
        return cleaned_data


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'type', 'category', 'card', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomi'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdor'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'card': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Izoh'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqam'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'O\'zingiz haqingizda'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'card_number', 'balance', 'card_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Karta nomi'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '16 raqamli karta raqami', 'maxlength': '16'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Balans'}),
            'card_type': forms.Select(attrs={'class': 'form-control'}),
        }