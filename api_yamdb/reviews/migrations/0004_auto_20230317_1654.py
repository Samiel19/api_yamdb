# Generated by Django 3.2 on 2023-03-17 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0003_auto_20230317_1141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-pub_date'], 'verbose_name': 'review', 'verbose_name_plural': 'reviews'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='value',
            new_name='score',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='comment',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='titles',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='users.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='titles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title'),
        ),
    ]
