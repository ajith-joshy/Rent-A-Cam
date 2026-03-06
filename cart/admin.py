from django.contrib import admin

# Register your models here.
from .models import Cart,Order,Order_items
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_items)