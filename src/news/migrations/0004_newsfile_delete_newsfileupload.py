# Generated by Django 5.1.2 on 2024-10-24 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_newsfileupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='news/files/')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='news.news')),
            ],
        ),
        migrations.DeleteModel(
            name='NewsFileUpload',
        ),
    ]