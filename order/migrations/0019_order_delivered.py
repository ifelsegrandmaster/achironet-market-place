# Generated by Django 3.0.7 on 2020-12-09 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_order_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]