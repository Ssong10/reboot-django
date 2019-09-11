from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=20)
    job = models.CharField(max_length=30)
    address = models.CharField(max_length=40)
    birthday = models.DateField()
