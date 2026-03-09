# Create your models here.
from django.db import models
from superuser.models import Product
from django.conf import settings

# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    def sub_total(self):
        return self.product.price*self.quantity

from django.core.validators import RegexValidator
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must contain exactly 10 digits"
)

class Order(models.Model):
    order_id=models.CharField(max_length=50, blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount=models.IntegerField()
    address=models.TextField()
    phone = models.CharField(max_length=10, validators=[phone_validator])
    payment_method=models.CharField(max_length=10)
    ordered_date=models.DateTimeField(auto_now_add=True)
    is_ordered=models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=20,default="Pending")
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.order_id

class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self):
        return self.order.order_id

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'product')