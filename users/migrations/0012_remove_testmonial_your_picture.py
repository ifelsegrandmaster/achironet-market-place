# Generated by Django 3.0.7 on 2020-11-24 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_sellerprofile_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testmonial',
            name='your_picture',
        ),
    ]
