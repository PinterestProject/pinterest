from django.contrib import admin
from Pins.models import Pin
from .models import *
# Register your models here.
admin.site.register(Favourite)
admin.site.register(Pin)


