# Generated by Django 3.1 on 2020-08-30 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_orderdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
    ]
