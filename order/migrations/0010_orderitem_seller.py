# Generated by Django 3.0.7 on 2020-11-05 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_sellerprofile_country'),
        ('order', '0009_auto_20201105_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='seller',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='customer_order_items', to='users.SellerProfile'),
            preserve_default=False,
        ),
    ]
