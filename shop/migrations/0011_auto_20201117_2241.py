# Generated by Django 3.0.7 on 2020-11-17 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20201117_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
