# Generated by Django 3.0.7 on 2020-10-31 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20201031_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippinginformation',
            old_name='address',
            new_name='street_address',
        ),
    ]
