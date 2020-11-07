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

    def __str__(self):
        return self.month
