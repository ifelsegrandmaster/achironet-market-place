# Generated by Django 3.0.7 on 2020-11-28 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_testmonial_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
    ]
