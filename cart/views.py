from django.shortcuts import render,redirect
from django.views import View
from superuser.models import Product
from .models import Cart, Wishlist, Order, Order_items
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.db.models import Sum

# Create your views here.
@method_decorator(login_required,name="dispatch")
class Addtowishlist(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        Wishlist.objects.get_or_create(user=u,product=p)
        return redirect('cart:wishlistview')

@method_decorator(login_required,name="dispatch")
class Wishlist_view(View):
    def get(self, request):
        u = request.user
        w = Wishlist.objects.filter(user=u)
        return render(request, 'wishlist.html', {'wishlist': w})

@method_decorator(login_required,name="dispatch")
class Deletefromwishlist(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        Wishlist.objects.filter(user=u,product=p).delete()
        return redirect('cart:wishlistview')

@method_decorator(login_required,name="dispatch")
class Addtocart(View):
    def get(self,request,i):
        u = request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)    #if yes
            c.quantity+=1   #increments quantity by 1
            c.save()
        except:             #if product does not exist
            c=Cart.objects.create(user=u,product=p,quantity=1)  #creates a new record with quantity=1
            c.save()
        return redirect('cart:cartview')

@method_decorator(login_required,name="dispatch")
class Removefromcart(View):
    def get(self,request,i):
        u=request.user
        p = Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            if c.quantity>1:
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except Cart.DoesNotExist:
            pass
        return redirect('cart:cartview')

@method_decorator(login_required,name="dispatch")
class Deletefromcart(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        Cart.objects.filter(user=u,product=p).delete()
        return redirect('cart:cartview')

@method_decorator(login_required,name="dispatch")
class Cart_view(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+i.sub_total()
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

import uuid
import razorpay
from .forms import Orderform
@method_decorator(login_required,name="dispatch")
class Checkout(View):
    def get(self,request):
        f=Orderform()
        u = request.user
        c = Cart.objects.filter(user=u)
        daily_total = sum(i.product.price * i.quantity for i in c)
        context={'form':f,
                 'daily_total':daily_total,
                 'total':daily_total,
                 'shipping_cost': 0,
                 'grand_total': daily_total
                 }
        return render(request,'checkout.html',context)
    def post(self,request):
        f=Orderform(request.POST)
        if f.is_valid():
            o=f.save(commit=False)
            u=request.user
            o.user=u
            c = Cart.objects.filter(user=u)
            start_date = f.cleaned_data['start_date']
            end_date = f.cleaned_data['end_date']
            if end_date < start_date:
                total = sum(i.sub_total() for i in c)
                messages.error(request, "End date must be after start date.")
                return render(request, 'checkout.html', {
                    'form': f,
                    'total': total,
                    'shipping_cost':0,
                    'grand_total':total
                })
            rental_days = (end_date - start_date).days + 1
            for item in c:
                booked_qty = Order_items.objects.filter(product=item.product,order__is_ordered=True).filter(
                    Q(order__start_date__lte=end_date) & Q(order__end_date__gte=start_date)
                    ).aggregate(total=Sum('quantity'))['total'] or 0
                available_stock = item.product.stock - booked_qty
                if item.quantity > available_stock:
                    total = 0
                    for cart_item in c:
                        rental_price = cart_item.product.price * rental_days
                        total += rental_price * cart_item.quantity
                    messages.error(
                        request,f"Only {available_stock} {item.product.name} available for selected dates."
                    )
                    return render(request, 'checkout.html', {
                        'form': f,
                        'total': total,
                        'shipping_cost': 0,
                        'grand_total': total
                    })
            total=0
            for item in c:
                rental_price = item.product.price * rental_days
                total += rental_price * item.quantity
            shipping_cost=0
            shipping_option=request.POST.get('shipping-option')
            if shipping_option == 'express':
                shipping_cost = 50
            elif shipping_option == 'standard' :
                shipping_cost=0
            grand_total = total + shipping_cost
            o.amount = grand_total
            o.start_date = start_date
            o.end_date = end_date
            o.save()
            # Create Order_items for this ONE order
            for cart_item in c:
                Order_items.objects.create(
                    order=o,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )
            if o.payment_method=="ONLINE":
                #Create a razorpay connection using Keys
                client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                #Creates a new order in razorpay
                response_payment = client.order.create({
                    'amount': int(o.amount * 100),
                    'currency': 'INR'
                })
                #retreives the order id from the response_payment
                id=response_payment['id']
                #saves it in the order table
                o.order_id=id
                o.save()
                context={'payment':response_payment,'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID,'amount_rupees': o.amount}
                return render(request,'payment.html',context)
            else:   #COD
                id='ORD_COD'+uuid.uuid4().hex[:14]
                o.order_id=id
                o.is_ordered=True
                o.save()
                items=Order_items.objects.filter(order=o)
                for item in items:
                    item.product.stock -= item.quantity
                    item.product.save()
                Cart.objects.filter(user=u).delete()
            return render(request,'payment.html',{'order':o})
        else:
            u = request.user
            c = Cart.objects.filter(user=u)
            total = sum(i.sub_total() for i in c)
            return render(request, 'checkout.html', {
                'form': f,
                'total': total,
                'shipping_cost': 0,
                'grand_total': total
            })

#CSRF_EXEMPT -to ignore csrf verification for this view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")
class Payment_success(View):
    def post(self,request):
        response=request.POST
        #Updates Order Table
        razorpay_order_id = response.get('razorpay_order_id')
        razorpay_payment_id = response.get('razorpay_payment_id')
        razorpay_signature = response.get('razorpay_signature')
        o=Order.objects.get(order_id=razorpay_order_id)    #retreieves the order record matching with the order id
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        o.is_ordered = True
        o.payment_id = razorpay_payment_id
        o.save()
        Cart.objects.filter(user=o.user).delete()
        items = Order_items.objects.filter(order=o)
        for item in items:
            item.product.stock -= item.quantity
            item.product.save()
        return render(request, 'payment_success.html', {'order': o})

@method_decorator(login_required,name="dispatch")
class Your_orders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True).order_by('-ordered_date')
        context={'your_orders':o}
        return render(request,'your_orders.html',context)
