# Generated by Django 3.0.7 on 2020-12-09 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20201206_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='received',
            new_name='delivered',
        ),
    ]
