from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, unique=True)
    image = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=20, decimal_places=1)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=200)
    user_id = models.BigIntegerField(max_length=200)
    product_id = models.IntegerField(max_length=200)
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=1)

    def __str__(self):
        return str(self.user_id)


class History(models.Model):
    user_id = models.BigIntegerField(null=True, blank=True)
    price = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user_id
