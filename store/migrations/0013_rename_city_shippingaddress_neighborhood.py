# Generated by Django 3.2.8 on 2021-12-11 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20211211_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='city',
            new_name='neighborhood',
        ),
    ]
