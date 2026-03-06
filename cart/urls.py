"""
URL configuration for cam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cart import views
app_name='cart'

urlpatterns = [
    path('addtocart/<int:i>',views.Addtocart.as_view(),name="addtocart"),
    path('removefromcart/<int:i>',views.Removefromcart.as_view(),name="removefromcart"),
    path('deletefromcart/<int:i>',views.Deletefromcart.as_view(),name="deletefromcart"),
    path('cartview',views.Cart_view.as_view(),name="cartview"),
    path('wishlist/<int:i>',views.Addtowishlist.as_view(),name="addtowishlist"),
    path('wishlistview',views.Wishlist_view.as_view(),name="wishlistview"),
    path('deletefromwishlis/<int:i>',views.Deletefromwishlist.as_view(),name="deletefromwishlist"),
    path('checkout',views.Checkout.as_view(),name="checkout"),
    path("payment_success",views.Payment_success.as_view(),name="payment_success"),
    path("your_orders",views.Your_orders.as_view(),name="your_orders"),
]
