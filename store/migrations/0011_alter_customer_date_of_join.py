# Generated by Django 3.2.8 on 2021-12-11 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20211211_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_of_join',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
