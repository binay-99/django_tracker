from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CurrentBalance(models.Model):
    current_bal = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    expense_type = models.CharField(choices = (('CREDIT','CREDIT'), ('DEBIT','DEBIT')), max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
