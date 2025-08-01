from django.shortcuts import render,redirect
from .models import *
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
        return redirect('index')
    
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