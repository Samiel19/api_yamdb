# Generated by Django 3.2 on 2023-03-22 08:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20230322_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(2023)]),
        ),
    ]