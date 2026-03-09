from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from superuser.models import Category, Product
from search.models import Review

# Create your views here.
class Home(View):
    def get(self,request):
        categories=Category.objects.all()
        products=Product.objects.all()
        reviews=Review.objects.select_related('user').order_by('-id')[:6]
        context={'products':products,'categories':categories,'reviews':reviews}
        return render(request,'home.html',context)


import threading
from django.core.mail import send_mail
from django.conf import settings
def send_otp_email(email, otp):
    try:
        send_mail(
            "Django Auth OTP",
            f"Your OTP is {otp}. It is valid for 5 minutes.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True
        )
    except Exception as e:
        print("Email sending failed:", e)

class Register(View):
    def get(self,request):
        f=Registerform()
        context={'form':f}
        return render(request,'register.html',context)
    def post(self,request):
        f=Registerform(request.POST)
        if f.is_valid():
            u=f.save(commit=False)
            u.is_active=False
            u.save()
            u.generate_otp()    #calls generate_otp defined in model
            threading.Thread(
                target=send_otp_email,
                args=(u.email, u.otp)
            ).start()
            request.session['otp_user'] = u.id
            return redirect('rent:verify')
        return render(request, 'register.html', {'form': f})

from .models import Customuser
from django.utils.timezone import now
from datetime import timedelta

class Otp_verify(View):
    def get(self,request):
        return render(request,'verify.html')
    def post(self, request):
        entered_otp = request.POST.get('o')
        user_id = request.session.get('otp_user')
        if not user_id:
            messages.error(request, "Session expired")
            return redirect('rent:register')
        try:
            u = Customuser.objects.get(id=user_id, otp=entered_otp)
        except Customuser.DoesNotExist:
            messages.error(request, "Invalid OTP")
            return redirect('rent:verify')
        if now() - u.otp_created_at > timedelta(minutes=5):
            messages.error(request, "OTP expired")
            return redirect('rent:register')
        u.is_active = True
        u.is_verified = True
        u.otp = None
        u.otp_created_at = None
        u.save()
        del request.session['otp_user']
        messages.success(request, "OTP verified successfully.")
        return redirect('rent:login')

from django.contrib import messages
from .forms import Loginform, Registerform
class Userlogin(View):
    def get(self,request):
        f=Loginform()
        context={'form':f}
        return render(request,'login.html',context)
    def post(self,request):
        f=Loginform(request.POST)
        if f.is_valid():
            data=f.cleaned_data #Fetch the data after validation
            u=data['username']  #retrieve username from cleaned_data
            p=data['password']  #retrieve password from cleaned_data
            user=authenticate(username=u,password=p)    #Calls authenticate() to verify if user exists
                                                        #if record exists then it returns user object
                                                        #else none
            if user:    #if user exists
                login(request,user)     #adds the user into current session
                return redirect('rent:home')
            else:   #if user does not exist
                messages.error(request, "Invalid credentials")
                return redirect('rent:login')

class Userlogout(View):
    def get(self,request):
        logout(request) #removes the user from current session
        return redirect('rent:login')

