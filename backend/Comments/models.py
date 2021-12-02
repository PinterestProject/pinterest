from django.db import models
# Create your models here.
from Pins.models import *
from Users.models import *

class comments(models.Model):
    id = models.AutoField(primary_key=True)
    user_id =models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    pin_id = models.ForeignKey(Pin, null=True, on_delete=models.SET_NULL)
    reply_content = models.TextField(default="")


    class Meta:
        verbose_name_plural = "Comments"

class comments_likes(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey(comments, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(Pin, null=True, on_delete=models.SET_NULL)
    is_liked = models.BooleanField()

    class Meta:
        verbose_name_plural = "comments_likes"




class comment_reply(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey(comments, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(Pin, null=True, on_delete=models.SET_NULL)
    reply_content = models.TextField()

    class Meta:
        verbose_name_plural = "comments_reply"

