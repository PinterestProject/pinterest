from django.contrib import admin

from .models import User, Invitation, User_board, Relationship
# Register your models here.
admin.site.register(User)
admin.site.register(Invitation)
admin.site.register(User_board)
admin.site.register(Relationship)

