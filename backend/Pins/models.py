from django.db import models
from Users.models import User
from datetime import datetime
# Create your models here.


class Pin(models.Model):

    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Favourite(models.Model):

    date = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_id = models.ForeignKey(Pin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'pin_id',)

    def __str__(self):
        return f'{self.user_id.name} {self.pin_id.title}'
