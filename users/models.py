from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .helpers import RandomFileName
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class User(AbstractUser):
    is_seller = models.BooleanField('Seller status', default=False)


class Profile(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    profile_picture = models.OneToOneField(
        "Photo", null=True, blank=True, on_delete=models.SET_NULL)
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
    company_name = models.CharField(max_length=90, blank=True)
    website = models.URLField(max_length=200, blank=True)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=45)
    country = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    address = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=12)
    review_group = models.ForeignKey(
        'RequestReviewGroup', null=True, blank=True, on_delete=models.SET_NULL)
    brand_logo = models.OneToOneField(
        "Photo", null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tradename


class Testmonial(models.Model):
    seller = models.OneToOneField(
        SellerProfile, null=True, blank=True, on_delete=models.SET_NULL)
    fullname = models.CharField(max_length=90)
    your_say = models.TextField(max_length=500)
    score = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def get_rating_html(self):
        # so now create an html markup string to render into the browser
        colored_stars = self.score
        uncolored_stars = 5 - colored_stars
        colored_stars_string = ""
        uncolored_stars_string = ""
        counter = 0
        # now create the colored stars markup
        for i in range(1, colored_stars+1):
            colored_stars_string += '<span><input type="radio" name="rating" id="str{0}" value="{0}"><label style="color:#F90" id="label{0}" for="str{0}"><i class="fas fa-star"></i></label></span>'.format(
                i)

        for i in range(colored_stars+1, 6):
            uncolored_stars_string +='<span><input type="radio" name="rating" id="str{0}" value="{0}"><label id="label{0}" for="str{0}"><i class="fas fa-star"></i></label></span>'.format(
                i)

        return '<div class="product-rating">' + colored_stars_string + uncolored_stars_string + '</div>'


class RequestReviewGroup(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Group: {}".format(self.pk)

class Photo(models.Model):
    file = models.ImageField(upload_to=RandomFileName("profile-images"), blank=True)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
