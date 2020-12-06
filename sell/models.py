from django.db import models
from users.models import SellerProfile

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


class BankDetails(models.Model):
    bank_name = models.CharField(max_length=90)
    bank_account = models.CharField(max_length=11)

    def __str__(self):
        return self.bank_name + " >> " + self.bank_account
