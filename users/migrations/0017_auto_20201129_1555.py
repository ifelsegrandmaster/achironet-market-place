# Generated by Django 3.0.7 on 2020-11-29 15:55

from django.db import migrations, models
import users.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20201128_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(blank=True, upload_to=users.helpers.RandomFileName('profile-images')),
        ),
    ]
