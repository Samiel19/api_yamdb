# Generated by Django 3.2 on 2023-03-21 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230318_2257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': 'reviews', 'ordering': ['-pub_date'], 'verbose_name': 'review', 'verbose_name_plural': 'reviews'},
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(),
        ),
    ]
