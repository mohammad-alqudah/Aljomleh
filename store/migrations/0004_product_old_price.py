# Generated by Django 3.2.8 on 2021-12-06 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_customer_wish_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
