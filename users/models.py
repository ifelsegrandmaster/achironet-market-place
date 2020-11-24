from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import RandomFileName
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class User(AbstractUser):
    is_seller = models.BooleanField('Seller status', default=False)


class Profile(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    profile_picture = models.ImageField(
        upload_to=RandomFileName("profile-images"))
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname + " " + self.lastname


class SellerProfile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    tradename = models.CharField(max_length=45)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=45)
    country = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    address = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=12)
    brand_logo = models.ImageField(upload_to=RandomFileName("brand-logos"))
    review_group = models.ForeignKey(
        'RequestReviewGroup', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tradename


class Testmonial(models.Model):
    seller = models.OneToOneField(
        SellerProfile, null=True, blank=True, on_delete=models.SET_NULL)
    your_picture = models.ImageField(
        upload_to=RandomFileName('testmonial-profiles'))
    fullname = models.CharField(max_length=90)
    your_say = models.TextField(max_length=500)
    score = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    created = models.DateTimeField(auto_now_add=True)


class RequestReviewGroup(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Group: {}".format(self.pk)
