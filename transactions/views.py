from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from datetime import date
from .models import Transaction, Category, Profile
from .forms import TransactionForm, RegisterForm, ProfileForm



@login_required
def index(request):


    transactions = Transaction.objects.filter(user=request.user)

    
    all_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum']
    if all_income is None:
        all_income = 0

    all_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum']
    if all_expense is None:
        all_expense = 0

  
    balance = all_income - all_expense

    
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
        'balance': balance,             
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

            
            return redirect('index')
    else:
      
        form = TransactionForm()

   
    categories = Category.objects.all()

    return render(request, 'transactions/add.html', {
        'form': form,
        'categories': categories
    })



@login_required
def delete_transaction(request, pk):

    
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    
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