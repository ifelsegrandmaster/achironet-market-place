from django.test import TestCase, Client
from django.shortcuts import reverse
from users.models import Profile, User
from order.models import Order, OrderItem, ShippingInformation
from shop.models import Product, Category


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            password='secretpass203',
            username='johndoe',
        )
        self.user2 = User.objects.create_user(
            email='petergriffin@gmail.com',
            password="secretpass203",
            username='petergriffin'
        )
        # Now log in the test client
        self.password = "secretpass203"
        self.is_authenticated = self.client.login(
            username=self.user.username, password=self.password)
