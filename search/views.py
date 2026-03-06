from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.
from tkinter.font import names
from django.views import View

# Create your views here.
from django.db.models import Q
from unicodedata import category

from superuser.models import Product
class Search_view(View):
    def get(self,request):
        query=request.GET.get('q','').strip()      #reads the keyword
        print(query)
        #ORM query to filter records from table(two or more records)
        p=Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        context={'products':p,'query':query}
        return render(request,'search.html',context)

from .forms import Reviewform
@method_decorator(login_required,name="dispatch")
class Review_view(View):
    def get(self,request,i):
        product=Product.objects.get(id=i)
        f=Reviewform()
        context={'form':f,'product':product}
        return render(request,'review.html',context)
    def post(self,request,i):
        product = Product.objects.get(id=i)
        f=Reviewform(request.POST)
        if f.is_valid:
            review=f.save(commit=False)
            review.user=request.user
            review.product=product
            review.save()
            return redirect('rent:home')
        else:
            return render(request,'review.html',{'form':f})
