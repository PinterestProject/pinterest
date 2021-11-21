from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager

from django.contrib.auth import get_user_model


class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    password_conf = models.CharField(max_length=255,default="")
    email = models.EmailField(max_length=225,unique=True)
    birth_day = models.DateField(null=True)

    gender = models.TextField(choices=[
        ('male', 'Male'),
        ('female','Female')
    ],null=True)
    pronoun = models.TextField(choices=[
        ('he', 'He'),
        ('she','She')
    ],null=True)
    language = models.TextField(choices=[
        ('arabic', 'ar'),
        ('english','en')
    ],null=True)

    address = models.CharField(max_length=225,null=True)
    bio = models.TextField(max_length=3000,null=True)
    profile_image=models.ImageField(upload_to='User/profile',null=True)
    cover_image=models.ImageField(upload_to='User/cover',null=True)
    social_facebook=models.CharField(max_length=100,null=True)
    social_google=models.CharField(max_length=100,null=True)
    social_twitter=models.CharField(max_length=100,null=True)
    history=models.JSONField(null=True,default={'recent_categories':[]})
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']

    objects=UserManager()

    def __str__(self):
        return self.email
