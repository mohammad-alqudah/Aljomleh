# Generated by Django 3.2.8 on 2021-12-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20211219_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
