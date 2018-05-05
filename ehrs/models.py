from django.db import models

# Create your models here.
class Ehr(models.Model):
    ehruid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

