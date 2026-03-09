from .models import Review
from django import forms

class Reviewform(forms.ModelForm):
    rating = forms.IntegerField(required=True,error_messages={
            'required': 'Please select a rating'
        })
    comment = forms.CharField(required=True, widget=forms.Textarea)
    class Meta:
        model=Review
        fields=['rating','comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }