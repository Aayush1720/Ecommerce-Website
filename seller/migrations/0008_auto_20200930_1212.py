# Generated by Django 3.0.7 on 2020-09-30 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_seller_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller_product',
            name='sale',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seller_product',
            name='visits',
            field=models.IntegerField(default=0),
        ),
    ]