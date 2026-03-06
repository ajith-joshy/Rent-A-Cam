from .models import Category
from django import forms

class Categoryform(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"


from .models import Product
class Productform(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','description','price','image','stock','category']

class Stockform(forms.ModelForm):
    class Meta:
        model=Product
        fields=['stock']