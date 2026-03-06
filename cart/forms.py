from django.utils import timezone
from django import forms
from .models import Order, Order_items

class Orderform(forms.ModelForm):
    payment_choices=(('COD','COD'),('ONLINE','ONLINE'))
    payment_method=forms.ChoiceField(choices=payment_choices)
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','class': 'form-control','min': timezone.now().date().isoformat()})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','class': 'form-control','min': timezone.now().date().isoformat()})
    )
    class Meta:
        model=Order
        fields=['address','phone','payment_method','start_date','end_date']

