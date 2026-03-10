from django.shortcuts import render, redirect
from django.views import View
from .forms import Productform, Categoryform
from .models import Product, Category
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test
def admin_required(user):
    return user.is_superuser
# Create your views here.

@method_decorator(login_required,name="dispatch")
@method_decorator(user_passes_test(admin_required),name="dispatch")
class Categories(View):
    def get(self,request):
        c=Category.objects.all()
        context={'cat':c}
        return render(request,'categories.html',context)

@method_decorator(login_required,name="dispatch")
@method_decorator(user_passes_test(admin_required),name="dispatch")
class Add_category(View):
    def get(self, request, i=None):
        if i:
            cat = Category.objects.get(id=i)
            cf = Categoryform(instance=cat)
        else:
            cf = Categoryform()
        categories = Category.objects.all()
        context = {'cform': cf,'categories': categories}
        return render(request, 'addcategory.html', context)
    def post(self, request, i=None):
        if i:
            cat = Category.objects.get(id=i)
            cf = Categoryform(request.POST, request.FILES, instance=cat)
        else:
            cf = Categoryform(request.POST, request.FILES)
        if cf.is_valid():
            cf.save()
        return redirect('superuser:add_category')

@method_decorator(login_required,name="dispatch")
@method_decorator(user_passes_test(admin_required),name="dispatch")
class Delete_category(View):
    def get(self,request,i):
        c = Category.objects.get(id=i)
        c.delete()
        return redirect('superuser:add_category')

@method_decorator(login_required,name="dispatch")
@method_decorator(user_passes_test(admin_required),name="dispatch")
class Add_product(View):
    def get(self, request, i=None):
        if i:
            p = Product.objects.get(id=i)
            pf = Productform(instance=p)
        else:
            pf = Productform()
        categories = Category.objects.all()
        context = {'pform': pf,'categories': categories}
        return render(request, 'addproducts.html', context)
    def post(self, request, i=None):
        if i:
            p = Product.objects.get(id=i)
            pf = Productform(request.POST, request.FILES, instance=p)
        else:
            pf = Productform(request.POST, request.FILES)
        if pf.is_valid():
            pf.save()
        return redirect('superuser:add_product')

@method_decorator(login_required,name="dispatch")
@method_decorator(user_passes_test(admin_required),name="dispatch")
class Delete_product(View):
    def get(self,request,i):
        p = Product.objects.get(id=i)
        p.delete()
        return redirect('superuser:add_product')

from .forms import Stockform
@method_decorator(login_required,name="dispatch")
@method_decorator(user_passes_test(admin_required),name="dispatch")
class Add_stock(View):
    def get(self,request,i):
        b=Product.objects.get(id=i)
        f=Stockform(instance=b)
        context={'form':f}
        return render(request,'edit.html',context)
    def post(self,request,i):
        b=Product.objects.get(id=i)
        f=Stockform(request.POST,instance=b)
        if f.is_valid():
            f.save()
        return redirect('rent:home')

class Detail_view(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'detail.html',context)

class Category_view(View):
    def get(self,request):
        c=Category.objects.all()
        context={'cat':c}
        return render(request,'categories.html',context)

class Product_view(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'cat':c}
        return render(request,'products.html',context)

from cart.models import Order_items
@method_decorator(login_required, name="dispatch")
@method_decorator(user_passes_test(admin_required), name="dispatch")
class Orders(View):
    def get(self, request):
        orders = Order_items.objects.filter(order__is_ordered=True).order_by("-order__ordered_date")
        context = {'orders': orders}
        return render(request, 'orders.html', context)