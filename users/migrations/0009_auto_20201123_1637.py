# Generated by Django 3.0.7 on 2020-11-23 16:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import users.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_sellerprofile_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestReviewGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Testmonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_picture', models.ImageField(upload_to=users.helpers.RandomFileName('testmonial-profiles'))),
                ('fullname', models.CharField(max_length=90)),
                ('your_say', models.TextField(max_length=500)),
                ('score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('seller', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.SellerProfile')),
            ],
        ),
        migrations.AddField(
            model_name='sellerprofile',
            name='review_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.RequestReviewGroup'),
        ),
    ]
