# Generated by Django 4.2.1 on 2023-07-22 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0003_droneboxprofile_total_revenue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='droneboxprofile',
            name='profile_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Customer', 'Customer'), ('Editor', 'Editor'), ('Pilot', 'Pilot')], default='Customer', max_length=8),
        ),
    ]
