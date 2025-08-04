from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.utils.timezone import now

# Create your views here.

def index(request):
    balance,_= CurrentBalance.objects.get_or_create(id=1)
    history = TrackingHistory.objects.filter(created_at__month=now().month).order_by('-created_at')

    if request.method == 'POST':
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))
        expense_type = request.POST.get('expense_type')

        if expense_type == 'CREDIT':
            balance.current_bal += amount
        else:
            balance.current_bal -= amount
        balance.save()

        TrackingHistory.objects.create(
            current_balance=balance,
            amount=amount,
            expense_type=expense_type,
            description=description
        )
        return redirect('/')
    
    credit = TrackingHistory.objects.filter(expense_type='CREDIT', created_at__month=now().month)
    debit = TrackingHistory.objects.filter(expense_type='DEBIT', created_at__month=now().month)
    monthly_expense = sum(i.amount for i in debit)
    monthly_income = sum(i.amount for i in credit)

    weekly_transactions = {}
    for transaction in history:
        week_number = transaction.created_at.isocalendar()[1]
        if week_number not in weekly_transactions:
            weekly_transactions[week_number] = []
        weekly_transactions[week_number].append(transaction)

    context = {
        "current_balance": balance,
        "monthly_income": monthly_income,
        "monthly_expense": monthly_expense,
        "weekly_expenses": weekly_transactions
    }

    return render(request, 'index.html', context)

def delete(request, id):
    history = TrackingHistory.objects.filter(id=id)
    
    if history.exists():
        balance,_= CurrentBalance.objects.get_or_create(id=1)
        if history[0].expense_type == 'DEBIT':
            balance.current_bal += float(history[0].amount)
        else:
            balance.current_bal -= float(history[0].amount)
        balance.save()
    history.delete()
    
    return redirect('/')

def edit(request,id):
    transaction = TrackingHistory.objects.filter(id=id)
    balance,_ = CurrentBalance.objects.get_or_create(id=1)
    old_amount = float(transaction[0].amount)
    old_type = transaction[0].expense_type

    if request.method == 'POST':
        form = EditForm(request.POST,instance=transaction[0])
        if form.is_valid():
            form.save()

            if old_type == 'DEBIT':
                balance.current_bal += old_amount
            else:
                balance.current_bal -= old_amount

            if transaction[0].expense_type == 'DEBIT':
                balance.current_bal -= float(transaction[0].amount)
            else:
                balance.current_bal += float(transaction[0].amount)

            balance.save()
            return redirect('index')
    else:
        form = EditForm(instance=transaction[0])

    return render(request,'edit.html',{'form':form})
