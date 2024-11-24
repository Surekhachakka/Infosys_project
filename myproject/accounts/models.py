from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add custom fields if necessary
    pass
from django.db import models

class SignatureModel1(models.Model):
    name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    status = models.CharField(max_length=100)

class SignatureModel2(models.Model):
    name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    status = models.CharField(max_length=100)