# Generated by Django 3.2.8 on 2021-12-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211206_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='wish_list',
            field=models.ManyToManyField(blank=True, null=True, to='store.Product'),
        ),
    ]