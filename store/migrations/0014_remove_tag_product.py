# Generated by Django 3.2.6 on 2021-10-19 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20211019_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='product',
        ),
    ]