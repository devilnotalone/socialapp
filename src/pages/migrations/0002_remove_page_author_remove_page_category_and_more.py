# Generated by Django 5.1.2 on 2024-10-18 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='author',
        ),
        migrations.RemoveField(
            model_name='page',
            name='category',
        ),
        migrations.RemoveField(
            model_name='page',
            name='tags',
        ),
        migrations.DeleteModel(
            name='PageCategory',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='PageTag',
        ),
    ]