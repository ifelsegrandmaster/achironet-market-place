# Generated by Django 3.0.7 on 2021-01-21 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0009_auto_20201213_1901'),
        ('agent', '0004_earning_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='bank_details',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bank_details', to='sell.BankDetails'),
        ),
    ]
