# Generated by Django 4.2.1 on 2023-07-22 12:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0002_alter_droneboxuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='droneboxprofile',
            name='total_revenue',
            field=models.FloatField(blank=True, default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='droneboxprofile',
            name='profile_type',
            field=models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Customer', 'Customer'), ('Editor', 'Editor'), ('Pilot', 'Pilot')], default='Customer', max_length=8),
        ),
    ]
