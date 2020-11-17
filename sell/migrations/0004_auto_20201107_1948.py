# Generated by Django 3.0.7 on 2020-11-07 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0003_revenue_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenue',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revenue',
            name='recent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revenue',
            name='year',
            field=models.CharField(default='2020', max_length=4),
            preserve_default=False,
        ),
    ]
