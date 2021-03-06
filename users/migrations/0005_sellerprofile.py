# Generated by Django 3.0.7 on 2020-11-03 18:58

from django.db import migrations, models
import users.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_is_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradename', models.CharField(max_length=45)),
                ('firstname', models.CharField(max_length=45)),
                ('lastname', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=90)),
                ('address', models.CharField(max_length=45)),
                ('bank_account', models.CharField(max_length=12)),
                ('brand_logo', models.ImageField(upload_to=users.helpers.RandomFileName('brand-logos'))),
            ],
        ),
    ]
