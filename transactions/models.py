from django.db import models
from user_profile.models import Profile

class Transaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account = models.ForeignKey(Profile, related_name = 'transactions', on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12, null=True)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']