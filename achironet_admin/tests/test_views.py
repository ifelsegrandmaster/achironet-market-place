from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile, User, SellerProfile, RequestReviewGroup
from datetime import datetime
import json
# create the test case


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # create a new user
        self.user = User.objects.create_user(
            email='johndoe@gmail.com',
            password='secretpass203',
            username='johndoe',
            is_superuser=True
        )
        self.review_group = RequestReviewGroup.objects.create()
        # create the seller
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
            review_group=self.review_group,
            user=self.user
        )

        # make the date a little backward
        self.seller.created = datetime(2020, 8, 8)
        self.seller.save()
        # Now log in the test client
        password = "secretpass203"
        self.is_authenticated = self.client.login(
            username=self.user.username, password=password)


    def test_mail_sellers(self):
        url = reverse("achironet_admin:mail_sellers")
        # now make a run for it
        response = self.client.post(url, {'group_id': "1"})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['deleteGroup'], True)
