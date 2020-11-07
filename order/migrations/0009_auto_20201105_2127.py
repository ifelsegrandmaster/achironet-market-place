# Generated by Django 3.0.7 on 2020-11-05 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_sellerprofile_country'),
        ('order', '0008_order_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='seller',
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ManyToManyField(blank=True, related_name='customer_orders', to='users.SellerProfile'),
        ),
    ]
