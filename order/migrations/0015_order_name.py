# Generated by Django 3.0.7 on 2020-12-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20201130_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default='Patrice Chaula', max_length=90),
            preserve_default=False,
        ),
    ]
