# Generated by Django 3.0.7 on 2020-10-31 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_shippinginformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippinginformation',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipment_addresses', to='order.Order'),
        ),
    ]
