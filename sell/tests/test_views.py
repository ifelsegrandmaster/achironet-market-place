from django.test import TestCase, Client
from django.shortcuts import reverse
from users.models import Profile, User, SellerProfile
from order.models import Order, OrderItem, ShippingInformation
from shop.models import Category, Product


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user to use when logging int
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            password='secretpass203',
            username='johndoe',
        )
        self.password = 'secretpass203'
        self.is_authenticated = self.client.login(
            username=self.user.username, password=self.password)

        # Create user profile
        self.profile = Profile.objects.create(
            firstname="Peter",
            lastname="Griffin",
            user=self.user,
            profile_picture='static/core/img/logo.png'
        )

        # Create a seller profile
        self.sellerprofile = SellerProfile.objects.create(
            user=self.user,
            tradename="Abantusoft",
            firstname="Peter",
            lastname="Griffin",
            phone_number="+263782841339",
            email="petergriffin@gmail.com",
            city="Gweru",
            country="Zimbabwe",
            state="Midlands",
            address="405 Fake Street 12",
            bank_account="06784920",
            brand_logo='static/core/img/logo.png'
        )

        # Now create an order
        self.order = Order.objects.create(
            profile=self.profile
        )
        self.order.seller.add(self.sellerprofile)
        # Now create a category
        self.category = Category.objects.create(
            name='fastfood',
            slug='fastfood1'
        )
        self.product = Product.objects.create(
            category=self.category,
            id=20,
            name='testproduct',
            slug='testproduct',
            description='my test product',
            image='static/core/img/logo.png',
            price=30,
            stock=23
        )

        # Now create an order item
        self.orderitem = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=6,
            seller=self.sellerprofile
        )

    def test_view_user_dashboard(self):
        url = reverse("sell:dashboard")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # Test if a product can be edited
    def test_edit_product(self):
        url = reverse("sell:product_edit", kwargs={"pk": self.product.pk})
        with open("test_data/profile.jpg", 'rb') as image:
            response = self.client.post(url, {
                'name': 'Bicyle',
                'image': image,
                'description': 'Just testing editing of product',
                'price': 34,
                'stock': 20
            })
            # Check if the view loaded correctly
            self.assertEquals(response.status_code, 302)
            # Now check if the product has been edited
            self.assertEquals(Product.objects.last().name, 'Bicyle')

    def test_view_sells_page(self):
        url = reverse("sell:revenue")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
