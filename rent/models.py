from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import random

class Customuser(AbstractUser):
    phone = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = now()
        self.save()