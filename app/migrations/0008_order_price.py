# Generated by Django 4.2 on 2023-05-05 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=15),
            preserve_default=False,
        ),
    ]
