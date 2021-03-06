from django.db import models
from shop.models import Product
from users.models import Profile, SellerProfile
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=90)
    paid = models.BooleanField(default=False)
    profile = models.ForeignKey(
        Profile, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    seller = models.ManyToManyField(SellerProfile, related_name='customer_orders', blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    shipped = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # to check it all items have been dropped at the depot
    def is_ready(self):
        for item in self.items.all():
            if item.received == False:
                return False
        return True


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    seller = models.ForeignKey(SellerProfile, related_name='customer_order_items', blank=True, on_delete=models.CASCADE)
    shipped = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class ShippingInformation(models.Model):
    fullname = models.CharField(max_length=90)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=90, blank=True)
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
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