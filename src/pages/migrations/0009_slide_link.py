# Generated by Django 5.1.2 on 2024-10-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_alter_page_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
