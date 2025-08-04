from django import forms
from .models import TrackingHistory

class EditForm(forms.ModelForm):
    class Meta:
        model = TrackingHistory
        fields = ['description', 'amount', 'expense_type']
        