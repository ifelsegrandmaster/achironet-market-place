from django.db import models
from users.models import SellerProfile
from datetime import datetime

# Create your models here.


class Revenue(models.Model):
    month = models.CharField(max_length=45)
    products_sold = models.IntegerField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(
        SellerProfile, related_name="sales", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    year = models.CharField(max_length=4)
    paid = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    bank_details = models.OneToOneField(
        "BankDetails", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.month

    def is_claimable(self):
        today = datetime.now()
        # check if the next month has been reached
        if today.year == self.created.year:
            if today.month > self.created.month:
                # check if the start day has been reached
                if today.day >= self.created.day:
                    return True
        return False





class BankDetails(models.Model):
    bank_name = models.CharField(max_length=90)
    bank_account = models.CharField(max_length=15)

    def __str__(self):
        return self.bank_name + " >> " + self.bank_account
