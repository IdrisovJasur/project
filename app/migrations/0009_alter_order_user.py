# Generated by Django 4.2 on 2023-05-05 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.IntegerField(max_length=200),
        ),
    ]
