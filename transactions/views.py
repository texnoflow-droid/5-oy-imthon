from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from datetime import date
from .models import Transaction, Category, Profile, Card
from .forms import TransactionForm, RegisterForm, ProfileForm, CardForm


@login_required
def index(request):
    transactions = Transaction.objects.filter(user=request.user)
    cards = Card.objects.filter(user=request.user, is_active=True)

    # Barcha kartalar balansi yig'indisi
    total_card_balance = cards.aggregate(Sum('balance'))['balance__sum']
    if total_card_balance is None:
        total_card_balance = 0

    today = date.today()
    this_month = transactions.filter(
        created_at__month=today.month,
        created_at__year=today.year
    )

    month_income = this_month.filter(type='income').aggregate(Sum('amount'))['amount__sum']
    if month_income is None:
        month_income = 0

    month_expense = this_month.filter(type='expense').aggregate(Sum('amount'))['amount__sum']
    if month_expense is None:
        month_expense = 0

    context = {
        'transactions': transactions,
        'cards': cards,
        'balance': total_card_balance,
        'month_income': month_income,
        'month_expense': month_expense,
    }
    return render(request, 'transactions/index.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            if transaction.card:
                if transaction.type == 'income':
                    transaction.card.balance += transaction.amount
                else:
                    transaction.card.balance -= transaction.amount
                transaction.card.save()

            return redirect('index')
    else:
        form = TransactionForm()
        form.fields['card'].queryset = Card.objects.filter(user=request.user)

    categories = Category.objects.all()
    return render(request, 'transactions/add.html', {
        'form': form,
        'categories': categories
    })


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if transaction.card:
        if transaction.type == 'income':
            transaction.card.balance -= transaction.amount
        else:
            transaction.card.balance += transaction.amount
        transaction.card.save()

    transaction.delete()
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'transactions/register.html', {'form': form})


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'transactions/profile.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
    return redirect('add_transaction')


@login_required
def cards(request):
    all_cards = Card.objects.filter(user=request.user)
    form = CardForm()
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('cards')
    context = {
        'cards': all_cards,
        'form': form,
    }
    return render(request, 'transactions/cards.html', context)


@login_required
def delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    card.delete()
    return redirect('cards')