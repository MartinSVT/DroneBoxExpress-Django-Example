# Generated by Django 4.2.1 on 2023-07-31 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Commercial', '0002_initial'),
        ('UserAccount', '0001_initial'),
        ('Operational', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersmodel',
            name='order_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='UserAccount.droneboxprofile'),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='order_route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Operational.routesmodel'),
        ),
    ]
