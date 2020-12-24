from django.test import TestCase, Client
from django.shortcuts import reverse
from users.models import Profile, User, SellerProfile, Photo
from order.models import Order, OrderItem, ShippingInformation
from shop.models import Category, Product, Specification, Attribute
from sell.models import Revenue
import json


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

        # create profile picture for the user
        self.profile_picture = Photo.objects.create(
            file='static/core/img/logo.png'
        )
        # Create user profile
        self.profile = Profile.objects.create(
            firstname="Peter",
            lastname="Griffin",
            user=self.user,
            profile_picture=self.profile_picture
        )
        self.brand_logo = Photo.objects.create(
            file='static/core/img/logo.png'
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
            brand_logo=self.brand_logo
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
            stock=23,
            seller=self.sellerprofile
        )

        # create another product
        self.product2 = Product.objects.create(
            category=self.category,
            id=21,
            name='testproduct',
            slug='testproduct',
            description='my test product',
            image='static/core/img/logo.png',
            price=30,
            stock=23,
            seller=self.sellerprofile
        )

        # Now create an order item
        self.orderitem = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=6,
            seller=self.sellerprofile
        )

        # Now create a specification item
        self.specification = Specification.objects.create(
            product=self.product2
        )

        # Now create attributes
        attributes = [
            {
                "key": "Processor",
                "value": "i5 Quad core"
            },
            {
                "key": "RAM",
                "value": "8GB DDR3"
            },
            {
                "key": "Storage",
                "value": "250GB SSD"
            }
        ]
        for attribute in attributes:
            Attribute.objects.create(
                specification=self.specification,
                key=attribute['key'],
                value=attribute['value']
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
            self.assertEquals(Product.objects.get(
                pk=self.product.pk).name, 'Bicyle')

    def test_view_revenue_page(self):
        url = reverse("sell:revenue")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_overview(self):
        url = reverse("sell:create_overview", kwargs={"pk": self.product.pk})
        response = self.client.post(
            url, {'description': '<h1>Just a simple test descripiton</h1>'})
        self.assertEquals(response.status_code, 302)

    def test_create_specification(self):
        url = reverse("sell:create_specification",
                      kwargs={"pk": self.product.pk})
        attributes = [
            {
                "key": "Processor",
                "value": "i5 Quad core"
            },
            {
                "key": "RAM",
                "value": "8GB DDR3"
            },
            {
                "key": "Storage",
                "value": "250GB SSD"
            }
        ]
        attributesString = json.dumps(attributes)
        # now send the data
        response = self.client.post(url, {"attributes": attributesString})
        # check if there was a redirect, that means the operation
        # was successful
        self.assertEquals(response.status_code, 302)

        def test_update_specification(self):
            url = reverse("sell:update_specification",
                          kwargs={"pk": self.specification.pk})
            attributes = [
                {
                    "key": "Processor",
                    "value": "i5 Quad core"
                },
                {
                    "key": "RAM",
                    "value": "8GB DDR3"
                },
                {
                    "key": "Storage",
                    "value": "250GB SSD"
                },
                {
                    "key": "Model name",
                    "value": "Vostro"
                }
            ]
            attributesString = json.dumps(attributes)
            # now send the data
            response = self.client.post(url, {"attributes": attributesString})
            # check if there was a redirect, that means the operation
            # was successful
            self.assertEquals(response.status_code, 302)
