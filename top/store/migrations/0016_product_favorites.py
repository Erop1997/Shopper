# Generated by Django 4.1.7 on 2023-07-06 13:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0015_auto_20230705_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
