# Generated by Django 3.0.7 on 2020-09-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0009_seller_product_cart_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='items_in_cart',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seller',
            name='no_of_sales',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seller',
            name='total_sale_amount',
            field=models.FloatField(default=0.0),
        ),
    ]