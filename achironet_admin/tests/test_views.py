from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile, User, SellerProfile, RequestReviewGroup, Testmonial, Photo
from sell.models import Revenue
from achironet_admin.models import EmailNewsletter
from datetime import datetime
import json
from json.decoder import JSONDecodeError
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
        # create brand logo
        self.brand_logo = Photo.objects.create(
            file='static/core/img/logo.png'
        )
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
            brand_logo=self.brand_logo,
            review_group=self.review_group,
            user=self.user
        )

        self.testimonial = Testmonial.objects.create(
            fullname="Patrice Chaula",
            your_say="Just testing if it works",
            score=5
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

    def test_delete_testimonial(self):
        url = reverse("achironet_admin:delete_testmonial")
        # make a run for it
        response = self.client.post(url, {'testmonial_id': '1'})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)

    def test_approve_testimonial(self):
        url = reverse("achironet_admin:approve_testmonial")
        # make a run for it
        response = self.client.post(url, {'testmonial_id': '1'})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)

    def test_create_newsletter(self):
        url = reverse("achironet_admin:create_newsletter")
        # make a run for it
        response = self.client.post(url,
                                    {
                                        'subject': 'testing',
                                        'message': '<h1>Get them now </h1>'
                                    })
        self.assertEquals(EmailNewsletter.objects.last().subject, 'testing')

    def test_edit_newsletter(self):
        # Create the newsletter to be edited
        newsletter = EmailNewsletter.objects.create(
            subject="Just testing",
            message="<p>Send some html</p>"
        )
        url = reverse("achironet_admin:edit_newsletter",
                      kwargs={"pk": newsletter.pk})
        # get it done
        response = self.client.post(url, {
            'subject': 'Just update testing',
            'message': '<p>Dont worry, fear no man</p>'
        })
        # refresh the updated object
        newsletter = EmailNewsletter.objects.get(pk=newsletter.pk)
        self.assertEquals(newsletter.subject,
                          'Just update testing')
        newsletter.delete()

    def test_delete_newsletter(self):
        # Create the newsletter to be deleted
        newsletter = EmailNewsletter.objects.create(
            subject="Just testing delete",
            message="This will be deleted"
        )
        # get the url to the view
        url = reverse("achironet_admin:delete_newsletter")
        response = self.client.post(
            url, {"email_newsletter_id": newsletter.pk})
        # now check if the operation was successful
        data = json.loads(response.content)
        self.assertEquals(data['success'], True)

    def test_search_seller_claims(self):
        #create seller claims to be saerched for
        Revenue.objects.create(
            month="January",
            seller=self.seller,
            sales=567,
            products_sold=78,
            claimed=True,
            paid=True,
            year="2020"
        )
        #now make a get request
        url = reverse('achironet_admin:seller_claims')
        response = self.client.get(url, {"month": "January"})
        self.assertContains(response, "567")

