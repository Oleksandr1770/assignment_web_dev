from django.db import models

# Create your models here.
class Account (models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Category(models.Model):
    name = models.CharField(max_length=200)


class Transaction(models.Model):
    value = models.CharField(max_length=12)
    transaction_type = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
