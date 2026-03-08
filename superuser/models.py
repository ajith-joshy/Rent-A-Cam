from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField()
    image=CloudinaryField('image')
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=30)
    description = models.TextField()
    image=CloudinaryField('image')
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.name