# Generated by Django 5.1.2 on 2024-10-24 04:17

import news.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=news.models.get_image_upload_path),
        ),
    ]
