# Generated by Django 3.0.7 on 2020-12-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='received',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
