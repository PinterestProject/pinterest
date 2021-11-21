from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField()



    def __str__(self):
        return self.name


# class Tag(models.Model):
#    name = models.CharField(max_length=255)

#    def __str__(self):
#       return self.name

