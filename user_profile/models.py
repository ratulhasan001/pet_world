from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=11,default=None,null=True,blank=True)
    address = models.CharField(max_length=200,default=None,null=True,blank=True)
    image = models.ImageField(upload_to='user_profile/media/images/',null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2) 
    def __str__(self):
        return self.user.username