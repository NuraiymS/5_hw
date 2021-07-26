from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    price = models.IntegerField(default=20, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ConfirmCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=16)