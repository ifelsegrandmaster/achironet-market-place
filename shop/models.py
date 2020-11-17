from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import SellerProfile, Profile


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.IntegerField()
    seller = models.ForeignKey(
        SellerProfile, related_name='stock', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    # get the first 50 characters
    def get_short_description(self):
        return self.description[:50] + "..."

    def get_average_review(self):
        total = sum(review.score for review in self.review_set.all())
        avg = 0
        try:
            avg = (total / self.review_set.all().count())
        except ZeroDivisionError:
            avg = 0
        print(avg)
        return int(avg)

    def get_rating_html(self):
        # so now create an html markup string to render into the browser
        colored_stars = self.get_average_review()
        uncolored_stars = 5 - colored_stars
        colored_stars_string = ""
        uncolored_stars_string = ""
        counter = 0
        # now create the colored stars markup
        for i in range(1, colored_stars+1):
            colored_stars_string += '<span><input type="radio" name="rating" id="str{0}" value="{0}"><label style="color:#F90" id="label{0}" for="str{0}"><i class="fas fa-star"></i></label></span>'.format(
                i)

        for i in range(colored_stars+1, 6):
            uncolored_stars_string += '<span><input type="radio" name="rating" id="str{0}" value="{0}"><label id="label{0}" for="str{0}"><i class="fas fa-star"></i></label></span>'.format(
                i)

        return '<div class="product-rating">' + colored_stars_string + uncolored_stars_string + '</div>'


class OverView(models.Model):
    description = models.TextField(blank=True)
    product = models.OneToOneField(
        Product, null=True, blank=True, on_delete=models.CASCADE)


class Specification(models.Model):
    product = models.OneToOneField(
        Product, null=True, blank=True, on_delete=models.CASCADE
    )


class Attribute(models.Model):
    key = models.CharField(max_length=90)
    value = models.CharField(max_length=512)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)


class Review(models.Model):
    your_message = models.TextField(max_length=4000)
    score = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL)

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
            uncolored_stars_string += '<span><input type="radio" name="rating" id="str{0}" value="{0}"><label id="label{0}" for="str{0}"><i class="fas fa-star"></i></label></span>'.format(
                i)

        return '<div class="product-rating">' + colored_stars_string + uncolored_stars_string + '</div>'
