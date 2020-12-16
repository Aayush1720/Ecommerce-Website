# Generated by Django 3.0.7 on 2020-10-02 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20201002_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, to='store.Tag'),
        ),
    ]