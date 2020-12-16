# Generated by Django 3.0.7 on 2020-10-03 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20201002_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
        migrations.AddField(
            model_name='tag',
            name='product',
            field=models.ManyToManyField(blank=True, to='store.Product'),
        ),
    ]