# Generated by Django 3.0.7 on 2020-10-31 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
    ]
