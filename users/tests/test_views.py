from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Category, Product
from users.models import Profile, User, SellerProfile


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            password='secretpass203',
            username='johndoe',
        )

        User.objects.create_user(
            email='jdox@gmail.com',
            password='secretpass203',
            username='jdox',
        )
        # Now log in the test client
        password = "secretpass203"
        self.is_authenticated = self.client.login(
            username=self.user.username, password=password)

        # Now setup the profile image to be uploaded

    # Test if a user profile can be created successfully
    def test_user_profile_creation(self):
        url = reverse("users:create-profile")
        # Send a post request
        with open("test_data/profile.jpg", 'rb') as dp:
            response = self.client.post(url, {
                'firstname': 'John',
                'lastname': 'Doe',
                'profile_picture': dp
            })
        # assert the response returned if's it is a redirect
        self.assertEquals(response.status_code, 302)
        # Check if the profile was created
        self.assertEquals(Profile.objects.last().firstname, 'John')

    def test_user_is_logged_in(self):
        self.assertEquals(self.is_authenticated, True)

    def test_edit_user_profile(self):
        # Initialize data
        user = User.objects.get(pk=1)
        with open('test_data/profile.jpg', 'rb') as dp:
            self.profile = Profile.objects.create(
                firstname='Peter',
                lastname='Griffin',
                user=user
            )

        # Create a profile
        url = reverse("users:edit-profile",
                      kwargs={'pk': self.user.profile.pk})
        # Now make a post request
        with open("test_data/profile2.jpg", 'rb') as dp2:
            response = self.client.post(url, {
                'profile_picture': dp2
            })
        # If a redirect happens that means the profile has been successfully
        # update
        self.assertEquals(response.status_code, 302)

    def test_seller_profile_creation(self):
        url = reverse("users:create-seller-profile")
        # Send a post request
        with open("test_data/profile.jpg", 'rb') as dp:
            response = self.client.post(url, {
                'tradename': 'Abantusoft',
                'firstname': 'John',
                'lastname': 'Doe',
                'phone_number': '+263782841339',
                'email': 'johndoe@gmail.com',
                'city': 'Gweru',
                'state': 'Midlands',
                'address': '320 Fake Location 12',
                'bank_account': '102002040',
                'brand_logo': dp
            })
        # assert the response returned if's it is a redirect
        self.assertEquals(response.status_code, 302)
        # Check if the profile was created
        self.assertEquals(SellerProfile.objects.last().tradename, 'Abantusoft')

    # Test editing seller profile
    def test_edit_seller_profile(self):
        # Initialize data
        user = User.objects.get(pk=1)
        self.seller = SellerProfile.objects.create(
            tradename="Abantuware",
            firstname='Peter',
            lastname='Griffin',
            phone_number='+263782841339',
            email='petergriffin@gmail.com',
            city="Quahog",
            state='Midlands',
            address='456 Fake Street 12',
            bank_account='203040240506',
            brand_logo='static/core/img/logo.png',
            user=user
        )
        # Create a profile
        url = reverse("users:edit-seller-profile",
                      kwargs={'pk': self.seller.pk})
        # Now make a post request
        with open("test_data/profile2.jpg", 'rb') as dp2:
            self.response = self.client.post(url, {
                'profile_picture': dp2
            })
        # If a redirect happens that means the profile has been successfully
        # update
        self.assertEquals(self.response.status_code, 200)
