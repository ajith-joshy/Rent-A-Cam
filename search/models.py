from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from superuser.models import Product
# Create your models here.
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField()