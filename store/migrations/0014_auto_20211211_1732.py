# Generated by Django 3.2.8 on 2021-12-11 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_rename_city_shippingaddress_neighborhood'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='flavor',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='flavor',
            field=models.ManyToManyField(null=True, to='store.Flavor'),
        ),
    ]
