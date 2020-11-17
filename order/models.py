from django.db import models
from shop.models import Product
from users.models import Profile, SellerProfile
from django.conf import settings


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    profile = models.ForeignKey(
        Profile, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    seller = models.ManyToManyField(SellerProfile, related_name='customer_orders', blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    seller = models.ForeignKey(SellerProfile, related_name='customer_order_items', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class ShippingInformation(models.Model):
    fullname = models.CharField(max_length=90)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField()
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=90)
    country = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    postal_code = models.CharField(max_length=20)
    order = models.OneToOneField(
        Order, related_name='shipping_address', on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, related_name='my_shipments_addresses', on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname + ", " + self.phone_number + ", " + self.country + ",  " + self.street_address


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username