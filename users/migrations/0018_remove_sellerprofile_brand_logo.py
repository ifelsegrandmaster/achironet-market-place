# Generated by Django 3.0.7 on 2020-11-30 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20201129_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerprofile',
            name='brand_logo',
        ),
    ]
