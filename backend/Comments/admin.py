from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(comments)
admin.site.register(comments_likes)
admin.site.register(comment_reply)
