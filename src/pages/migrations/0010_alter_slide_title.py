# Generated by Django 5.1.2 on 2024-10-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_slide_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
