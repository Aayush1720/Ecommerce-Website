# Generated by Django 3.0.7 on 2020-09-30 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0008_auto_20200930_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller_product',
            name='cart_no',
            field=models.IntegerField(default=0),
        ),
    ]
